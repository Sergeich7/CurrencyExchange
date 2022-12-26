"""Парсим аргументы командной строки и задаем значения по умолчанию."""

import datetime

import argparse


def valid_data(data: str) -> datetime:
    """Проверка валидности даты."""
    try:
        data = datetime.datetime.strptime(data, '%Y%m%d')
    except ValueError:
        raise argparse.ArgumentTypeError('%s is not a valid data' % (data,))
    return data


def valid_currency(cur: str) -> str:
    """Проверка валидности валюты."""
    if len(cur) == 3:
        return cur
    raise argparse.ArgumentTypeError(
        '%s is not a valid data. Must be 3 chars.' % (cur,))


def valid_volume(volume: str) -> float:
    """Проверка валидности объема обмена."""
    try:
        volume = float(volume)
    except ValueError:
        raise argparse.ArgumentTypeError('%s is not a valid data' % (volume,))
    if volume < 0:
        raise argparse.ArgumentTypeError('%s is not a valid data' % (volume,))
    return volume


def valid_req(volume: str) -> int:
    """Проверка валидности количества запросов в мин."""
    try:
        volume = int(volume)
    except ValueError:
        raise argparse.ArgumentTypeError('%s is not a valid data' % (volume,))
    if volume < 0:
        raise argparse.ArgumentTypeError('%s is not a valid data' % (volume,))
    return volume


def get_args():
    """Парсим аргументы."""
    parser = argparse.ArgumentParser(description='Command line arguments')

    parser.add_argument(
        'cmd',
        choices=['symbols', 'convert', 'history'],
        help='command'
    )

    parser.add_argument(
        '-from',
        dest='c_from',
        type=valid_currency,
        default='USD',
        help='convert currency from'
    )

    parser.add_argument(
        '-to',
        dest='c_to',
        type=valid_currency,
        default='EUR',
        help='convert currency to'
    )

    parser.add_argument(
        # Не получается сделать позиционным. Иначе придется вызывать
        # symbols 100
        '-volume',
        type=valid_volume,
        default=100,
        help='volume to be converted'
    )

    data_today = datetime.date.today().strftime("%Y%m%d")
    parser.add_argument(
        '-data_from',
        type=valid_data,
        default=data_today,     # если не задано, то берем за сегодня
        help='start date history period'
    )

    parser.add_argument(
        '-data_to',
        type=valid_data,
        default=data_today,     # если не задано, то берем за сегодня
        help='end date history period'
    )

    parser.add_argument(
        '-max_req',
        type=valid_req,
        default=5,             # Максимальное число запросов одновременно
        help='max requests simultaneously'
    )

    return parser.parse_args()
