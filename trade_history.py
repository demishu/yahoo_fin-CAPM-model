import pandas as pd
from yahoo_fin import stock_info as si
import datetime
from tqdm import tqdm
from collections.abc import Iterable
from typing import NewType
date = NewType("date", str)


class TradeHistory:
    def __init__(self, stocks_list: pd.DataFrame or Iterable, start_day: date, end_day: date = None):
        """
        stocks_list: pd.DataFrame or Iterable
        start_day: date
        end_day: date
        """
        _fmt = "%Y/%m/%d"

        '输入检查:stocks_list'
        if isinstance(stocks_list, pd.DataFrame):
            self._stocks = stocks_list.iloc[:, 0].unique().tolist()

        elif isinstance(stocks_list, Iterable):
            self._stocks = list(set(stocks_list))

        else:
            raise ValueError("输入的stocks_list异常，请检查。")

        "输入检查：start_day"
        if isinstance(start_day, datetime.datetime) or isinstance(start_day, datetime.date):
            self._start_day = start_day.strftime(_fmt)
        else:
            try:
                self._start_day = datetime.datetime.strptime(start_day, _fmt)
                self._start_day = self._start_day.strftime(_fmt)
            except TypeError:
                raise TypeError('输入的start_day应该为str格式的日期或者datetime.datetime, datetime.date')
            except ValueError:
                raise ValueError('输入的start_day日期格式应该为：%Y/%m/%d')

        "输入检查：end_day"
        if isinstance(end_day, datetime.datetime) or isinstance(end_day, datetime.date):
            self._end_day = end_day.strftime(_fmt)
        elif end_day is None:
            self._end_day = datetime.datetime.now().strftime(_fmt)
        else:
            try:
                self._end_day = datetime.datetime.strptime(end_day, _fmt).strftime(_fmt) or\
                                datetime.datetime.now().strftime(_fmt)
            except ValueError:
                raise ValueError('输入的end_day日期格式应该为：%Y/%m/%d')

        '创建需要维护的self._df'
        self._df = pd.DataFrame(columns=self._stocks)

        '初始化self._df'
        self._get_data()

    def _get_data(self):
        """
        从yahoo_fin获取交易数据[adjclose]
        """
        for stock in tqdm(self._stocks):
            df = si.get_data(stock, self._start_day, self._end_day, index_as_date=True)
            self._df[stock] = df.loc[:, "adjclose"]

    @property
    def df(self):
        return self._df.copy()

    @property
    def stocks(self):
        return self._stocks.copy()

    def __repr__(self):
        return f"start_day:{self._start_day}\nend_day:{self._end_day}\n" \
               f"stocks:{self._stocks}\nhead rows:\n{self._df.head(5)}"


if __name__ == '__main__':
    from stocks import stocks
    history_df = TradeHistory(stocks, "2022/01/01")
    print(history_df)

