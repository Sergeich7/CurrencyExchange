"""Асинхронная версия."""

from datetime import timedelta

from argparse import ArgumentParser

import asyncio
import aiohttp

import parse_args


async def get_exch_json(
            session: aiohttp.ClientSession, semaphore: asyncio.Semaphore,
            util_args: ArgumentParser, url: str) -> str:
    """Получаем данные и возвращаем уже конечную строку."""
    async with semaphore:
        async with session.get(url) as resp:
            resp_json = await resp.json()

            if not resp_json['success']:
                # запрос выполнился неудачно
                raise ConnectionError('Something gone wrong')

            # Сразу и форматируем в строку
            resp_json_to_str = {
                'symbols': lambda data_json: ' '.join(
                    [k for k in data_json['symbols'].keys()]),

                'convert': lambda data_json: ' '.join((
                    f'{util_args.volume:.2f}', util_args.c_from, '=',
                    f'{data_json["result"]:.2f}', util_args.c_to)),

                'history': lambda data_json: ' '.join((
                    data_json['date'],
                    f'{util_args.volume:.2f}', util_args.c_from, '=',
                    f'{data_json["rates"][util_args.c_to]:.2f}',
                    util_args.c_to)),
            }
            return resp_json_to_str[util_args.cmd](resp_json)


async def make_tasks(util_args: ArgumentParser) -> dict:
    """Создаем задачи на скачивание."""
    semaphore = asyncio.Semaphore(util_args.max_req)

    async with aiohttp.ClientSession() as session:
        tasks = []

        # Формируем задачи
        if util_args.cmd == 'symbols':
            tasks.append(asyncio.ensure_future(get_exch_json(
                    session, semaphore, util_args,
                    'https://api.exchangerate.host/symbols',
                )))

        elif util_args.cmd == 'convert':
            tasks.append(asyncio.ensure_future(get_exch_json(
                    session, semaphore, util_args,
                    f'https://api.exchangerate.host/convert?from={util_args.c_from}&to={util_args.c_to}&amount={util_args.volume}',
                )))

        elif util_args.cmd == 'history':
            # Дата начала не может быть больше даты окончания
            if util_args.data_from > util_args.data_to:
                raise ValueError('Start data greater finish data')

            tec_data = util_args.data_from
            while tec_data <= util_args.data_to:
                tec_data_str = tec_data.strftime("%Y-%m-%d")
                tasks.append(asyncio.ensure_future(get_exch_json(
                        session, semaphore, util_args,
                        f'https://api.exchangerate.host/{tec_data_str}?base={util_args.c_from}&symbols={util_args.c_to}&amount={util_args.volume}',
                    )))
                tec_data += timedelta(days=1)

        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    util_args = parse_args.get_args()
    result = asyncio.run(make_tasks(util_args))
    if len(result) > 1:
        result.sort()
        print(f'Running {len(result)} tasks with {util_args.max_req} requests at the same time.')
    print(util_args.cmd.upper())
    [print(st) for st in result]
