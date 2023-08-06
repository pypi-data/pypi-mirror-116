"""

"""

from notecoin.huobi.history.utils import *
from notetool.log import log

ALL_PERIODS = ['1min', '5min', '15min', '30min', '60min', '4hour', '1day']
pre_url = "https://futures.huobi.com/data"
logger = log()

_SWAP = "swap"
_SPOT = "spot"
_FUTURE = "future"
_OPTION = "option"
_LINEARSWAP = "linear-swap"


class HistoryDownload:
    def __init__(self, _pre_url=None,
                 data_type: str = None,
                 all_period: list = None,
                 _type: str = 'spot',
                 freq: str = None,
                 start_date=None,
                 end_date=None):
        self.freq = freq or "daily"
        self.type = _type or 'spot'
        self.data_type = data_type or 'klines'
        self.pre_url = _pre_url or "https://futures.huobi.com/data"
        self.all_period = all_period or ALL_PERIODS
        self.start_date = start_date or datetime(2017, 10, 27)
        self.end_date = end_date or datetime(2021, 7, 27)
        self.all_symbols = None

    def init(self):
        if self.all_symbols is None:
            ok, all_symbols = False, []
            if self.type == _SPOT:
                ok, all_symbols = get_all_spot_symbols()
            elif self.type == _FUTURE:
                ok, all_symbols = get_all_future_symbols()
            elif self.type == _SWAP:
                ok, all_symbols = get_all_swap_symbols()
            elif self.type == _OPTION:
                ok, all_symbols = get_all_option_symbols()
            elif self.type == _LINEARSWAP:
                ok, all_symbols = get_all_linearswap_symbols()

            if not ok:
                logger.warning(all_symbols)
                return
            self.all_symbols = all_symbols

    def _download_daily(self, path_url, symbol, period) -> tuple:
        self.init()
        all_oks = []
        all_errs = []
        interval = self.end_date - self.start_date
        for index in range(interval.days):
            current = self.start_date + timedelta(days=index)
            url = f'{path_url}/{symbol.upper()}-{period}-{current.year}-{current.month:02}-{current.day:02}'
            zip_file = f'{url}.zip'
            # print(zip_file)
            check_file = f'{url}.CHECKSUM'
            ok, msg = http_download(zip_file)
            if not ok:
                all_errs.append({'url': url, 'msg': msg})
            else:
                all_oks.append(zip_file)
            ok, msg = http_download(check_file)
            if not ok:
                all_errs.append({'url': url, 'msg': msg})
            else:
                all_oks.append(url)
        return all_oks, all_errs

    def b_download(self, all_symbols: list = None, freq="daily"):
        """return date is: [start, end)"""
        for symbol in all_symbols:
            for period in self.all_period:
                if period in ['trades', ]:
                    path_url = f'{self.pre_url}/{self.data_type}/{self.type}/{freq}/{symbol}'
                else:
                    path_url = f'{self.pre_url}/{self.data_type}/{self.type}/{freq}/{symbol}/{period}'
                all_oks, all_errs = self._download_daily(path_url, symbol, period)
                logger.warning(f'success:{all_oks}')
                logger.warning(f'failed:{all_errs}')
        logger.info('done')

    def b_download_daily_spot(self, all_symbols: list = None):
        """return date is: [start, end)"""
        if all_symbols is None:
            ok, all_symbols = get_all_spot_symbols()
            if not ok:
                logger.warning(all_symbols)
                return
        self.b_download(all_symbols, freq='daily')

    def b_download_daily_future(self, all_symbols: list = None):
        """return date is: [start, end)"""
        self.type = _FUTURE
        self.b_download(all_symbols, freq='daily')

    def b_download_daily_swap(self, all_symbols: list = None):
        """return date is: [start, end)"""
        self.type = _SWAP
        self.b_download(all_symbols, freq='daily')

    def b_download_daily_linearswap(self, all_symbols: list = None):
        """return date is: [start, end)"""
        self.type = _LINEARSWAP
        self.b_download(all_symbols, freq='daily')

    def b_download_daily_option(self, all_symbols: list = None):
        """return date is: [start, end)"""
        self.type = _OPTION
        self.b_download(all_symbols, freq='daily')


def b_download(data_type: str, all_period: list = None, all_symbols: list = None,
               start: datetime = None,
               end: datetime = None,
               spot="spot", freq="daily"):
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


def b_download_daily_spot(data_type: str,
                          all_period: list = None,
                          start: datetime = None,
                          end: datetime = None,
                          all_symbols: list = None):
    """return date is: [start, end)"""
    history = HistoryDownload(_pre_url=pre_url, data_type=data_type, all_period=all_period, start_date=start,
                              end_date=end)
    history.b_download_daily_spot(all_symbols)


def b_download_daily_future(data_type: str,
                            all_period: list = None,
                            start: datetime = None,
                            end: datetime = None,
                            all_symbols: list = None):
    """return date is: [start, end)"""
    history = HistoryDownload(_pre_url=pre_url, data_type=data_type, all_period=all_period, start_date=start,
                              end_date=end)
    history.b_download_daily_future(all_symbols)


def b_download_daily_swap(data_type: str,
                          all_period: list = None,
                          start: datetime = None,
                          end: datetime = None,
                          all_symbols: list = None):
    """return date is: [start, end)"""
    history = HistoryDownload(_pre_url=pre_url, data_type=data_type, all_period=all_period, start_date=start,
                              end_date=end)
    history.b_download_daily_swap(all_symbols)


def b_download_daily_linearswap(data_type: str,
                                all_period: list = None,
                                start: datetime = None,
                                end: datetime = None,
                                all_symbols: list = None):
    """return date is: [start, end)"""
    history = HistoryDownload(_pre_url=pre_url, data_type=data_type, all_period=all_period, start_date=start,
                              end_date=end)
    history.b_download_daily_linearswap(all_symbols)


def b_download_daily_option(data_type: str,
                            all_period: list = None,
                            start: datetime = None,
                            end: datetime = None,
                            all_symbols: list = None):
    """return date is: [start, end)"""
    history = HistoryDownload(_pre_url=pre_url, data_type=data_type, all_period=all_period, start_date=start,
                              end_date=end)
    history.b_download_daily_option(all_symbols)


def download_kline_daily_spot(all_period: list = None, start: datetime = None, end: datetime = None,
                              all_symbols: list = None):
    """return date is: [start, end)"""

    data_type = 'klines'
    b_download_daily_spot(data_type, all_period, start, end, all_symbols)


def download_kline_daily_future(
        all_period: list = None, start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""

    data_type = 'klines'
    b_download_daily_future(data_type, all_period, start, end, all_symbols)


def download_kline_daily_swap(all_period: list = None, start: datetime = None, end: datetime = None,
                              all_symbols: list = None):
    """return date is: [start, end)"""

    data_type = 'klines'
    b_download_daily_swap(data_type, all_period, start, end, all_symbols)


def download_kline_daily_linearswap(
        all_period: list = None, start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""

    data_type = 'klines'
    b_download_daily_linearswap(data_type, all_period, start, end, all_symbols)


def download_kline_daily_option(
        all_period: list = None, start: datetime = None, end: datetime = None, all_symbols: list = None):
    """return date is: [start, end)"""

    data_type = 'klines'
    b_download_daily_option(data_type, all_period, start, end, all_symbols)


if __name__ == "__main__":
    download_kline_daily_spot(all_symbols=['BTCUSDT', 'ADAUSDT'],
                              start=datetime(2021, 5, 21),
                              end=datetime(2021, 5, 23),
                              all_period=['1min', '15min'])
    # download_daily_future()
    # download_daily_swap()
    # download_daily_linearswap()
    # download_daily_option(all_period=['1min'])
