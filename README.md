## Exchange Util
Консольная утилита расчета обмена валют на основе данных с сайта https://exchangerate.host/#/#docs.

### При разработки использовал
Python, Asyncio, AioHTTP, ArgParser

### Аргументы
usage: cmd_async.py [-h] [-from C_FROM] [-to C_TO] [-volume VOLUME] [-data_from DATA_FROM] [-data_to DATA_TO] [-max_req MAX_REQ] {symbols,convert,history}

Command line arguments

positional arguments:
* {symbols,convert,history}     command
                    
options:
* -h, --help            show this help message and exit
* -from C_FROM          convert currency from
* -to C_TO              convert currency to
* -volume VOLUME        volume to be converted
* -data_from DATA_FROM  start date history period
* -data_to DATA_TO      end date history period
* -max_req MAX_REQ      max requests simultaneously

### Примеры использования
$cmd_async.py symbols

SYMBOLS

AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BRL BSD BTC BTN BWP BYN BZD CAD CDF CHF CLF CLP CNH CNY COP CRC CUC CUP CVE CZK DJF DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL GGP GHS GIP GMD GNF GTQ GYD HKD HNL HRK HTG HUF IDR ILS IMP INR IQD IRR ISK JEP JMD JOD JPY KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LYD MAD MDL MGA MKD MMK MNT MOP MRO MRU MUR MVR MWK MXN MYR MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP SLL SOS SRD SSP STD STN SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD UYU UZS VEF VES VND VUV WST XAF XAG XAU XCD XDR XOF XPD XPF XPT YER ZAR ZMW ZWL

$cmd_async.py convert -v 99.3 -from USD -to EUR

CONVERT

99.30 USD = 93.49 EUR

$cmd_async.py history -v 99.3 -from USD -to EUR -data_from 20221222 -max_req 2

Running 5 tasks with 2 requests at the same time.

HISTORY

2022-12-22 99.30 USD = 93.65 EUR

2022-12-23 99.30 USD = 93.14 EUR

2022-12-24 99.30 USD = 93.11 EUR

2022-12-25 99.30 USD = 93.54 EUR

2022-12-26 99.30 USD = 93.49 EUR


