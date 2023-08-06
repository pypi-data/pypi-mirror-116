"""

"""
from notecoin.huobi.history.utils import *
from notetool.log import log

pre_url = "https://futures.huobi.com/data"
logger = log()


def b_download(data_type: str, all_period: list = None, start: datetime = None, end: datetime = None,
               all_symbols: list = None, spot="spot", freq="daily"):
    """return date is: [start, end)"""

    global pre_url
    for symbol in all_symbols:
        for period in all_period:
            if period in ['trades', ]:
                path_url = f'{pre_url}/{data_type}/{spot}/{freq}/{symbol}'
            else:
                path_url = f'{pre_url}/{data_type}/{spot}/{freq}/{symbol}/{period}'
            all_oks, all_errs = download_daily(path_url, symbol, period, start, end)
            logger.warning(f'success:{all_oks}')
            logger.warning(f'failed:{all_errs}')
    logger.info('done')


def b_download_daily_spot(data_type: str, all_period: list = None, start: datetime = None, end: datetime = None,
                          all_symbols: list = None):
    """return date is: [start, end)"""

    global pre_url
    if all_period is None:
        all_period = ALL_PERIODS
    if start is None:
        start = SPOT_START_DATE
    if end is None:
        end = END_DATE

    if all_symbols is None:
        ok, all_symbols = get_all_spot_symbols()
        if not ok:
            logger.warning(all_symbols)
            return

    b_download(data_type, all_period, start, end, all_symbols, spot='spot', freq='daily')


def b_download_daily_future(data_type: str, all_period: list = None, start: datetime = None, end: datetime = None,
                            all_symbols: list = None):
    """return date is: [start, end)"""

    global pre_url
    if all_period is None:
        all_period = ALL_PERIODS
    if start is None:
        start = SPOT_START_DATE
    if end is None:
        end = END_DATE

    if all_symbols is None:
        ok, all_symbols = get_all_future_symbols()
        if not ok:
            logger.warning(all_symbols)
            return

    b_download(data_type, all_period, start, end, all_symbols, spot='future', freq='daily')


def b_download_daily_swap(data_type: str, all_period: list = None, start: datetime = None, end: datetime = None,
                          all_symbols: list = None):
    """return date is: [start, end)"""

    global pre_url
    if all_period is None:
        all_period = ALL_PERIODS
    if start is None:
        start = SPOT_START_DATE
    if end is None:
        end = END_DATE

    if all_symbols is None:
        ok, all_symbols = get_all_swap_symbols()
        if not ok:
            logger.warning(all_symbols)
            return

    b_download(data_type, all_period, start, end, all_symbols, spot='swap', freq='daily')


def b_download_daily_linearswap(data_type: str, all_period: list = None, start: datetime = None, end: datetime = None,
                                all_symbols: list = None):
    """return date is: [start, end)"""

    global pre_url
    if all_period is None:
        all_period = ALL_PERIODS
    if start is None:
        start = SPOT_START_DATE
    if end is None:
        end = END_DATE

    if all_symbols is None:
        ok, all_symbols = get_all_linearswap_symbols()
        if not ok:
            logger.warning(all_symbols)
            return

    b_download(data_type, all_period, start, end, all_symbols, spot='linear-swap', freq='daily')


def b_download_daily_option(data_type: str, all_period: list = None, start: datetime = None, end: datetime = None,
                            all_symbols: list = None):
    """return date is: [start, end)"""

    global pre_url
    if all_period is None:
        all_period = ALL_PERIODS
    if start is None:
        start = SPOT_START_DATE
    if end is None:
        end = END_DATE

    if all_symbols is None:
        ok, all_symbols = get_all_option_symbols()
        if not ok:
            logger.warning(all_symbols)
            return

    b_download(data_type, all_period, start, end, all_symbols, spot='option', freq='daily')


"""
line
"""


def download_daily_line_spot(all_period: list = None, start: datetime = None, end: datetime = None,
                             all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'klines'
    b_download_daily_spot(data_type, all_period, start, end, all_symbols)


def download_daily_line_future(all_period: list = None, start: datetime = None, end: datetime = None,
                               all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'klines'
    b_download_daily_future(data_type, all_period, start, end, all_symbols)


def download_daily_line_swap(all_period: list = None, start: datetime = None, end: datetime = None,
                             all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'klines'
    b_download_daily_swap(data_type, all_period, start, end, all_symbols)


def download_daily_line_linearswap(all_period: list = None, start: datetime = None, end: datetime = None,
                                   all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'klines'
    b_download_daily_linearswap(data_type, all_period, start, end, all_symbols)


def download_daily_line_option(all_period: list = None, start: datetime = None, end: datetime = None,
                               all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'klines'
    b_download_daily_option(data_type, all_period, start, end, all_symbols)


"""
trades
"""


def download_daily_trades_spot(start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'trades'
    b_download_daily_spot(data_type, ['trades'], start, end, all_symbols)


def download_daily_trades_future(start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'trades'
    b_download_daily_future(data_type, ['trades'], start, end, all_symbols)


def download_daily_trades_swap(start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'trades'
    b_download_daily_swap(data_type, ['trades'], start, end, all_symbols)


def download_daily_trades_linearswap(start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'trades'
    b_download_daily_linearswap(data_type, ['trades'], start, end, all_symbols)


def download_daily_trades_option(start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""
    data_type = 'trades'
    b_download_daily_option(data_type, ['trades'], start, end, all_symbols)


if __name__ == "__main__":
    download_daily_line_spot(all_symbols=['BTCUSDT', 'ADAUSDT'],
                             start=datetime(2021, 5, 21),
                             end=datetime(2021, 5, 23),
                             all_period=['1min', '15min'])
    # download_daily_future()
    # download_daily_swap()
    # download_daily_linearswap()
    # download_daily_option(all_period=['1min'])

    download_daily_trades_spot(all_symbols=['btcusdt', 'ltcusdt'],
                               start=datetime(2021, 1, 1),
                               end=datetime(2021, 2, 1))
    # download_daily_future()
    # download_daily_swap()
    # download_daily_linearswap()
    # download_daily_option()
