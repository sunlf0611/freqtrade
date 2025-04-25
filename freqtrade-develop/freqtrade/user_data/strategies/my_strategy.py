from pandas import DataFrame

from freqtrade.strategy import IStrategy, IntParameter

from technical import qtpylib
import talib.abstract as ta

class MyStrategy(IStrategy):

    INTERFACE_VERSION = 2

    timeframe = '1h'

    minimal_roi = {
        "0": 0.162,
        "69": 0.097,
        "229": 0.061,
        "566": 0
    }

    # Stoploss:
    stoploss = -0.345

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.058
    trailing_only_offset_is_reached = False


    buy_rsi = IntParameter(low=1, high=50, default=30, space="buy", optimize=True, load=True)
    sell_rsi = IntParameter(low=50, high=100, default=70, space="sell", optimize=True, load=True)
    short_rsi = IntParameter(low=51, high=100, default=70, space="sell", optimize=True, load=True)
    exit_short_rsi = IntParameter(low=1, high=50, default=30, space="buy", optimize=True, load=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        print("打印datafreme,", dataframe)
        dataframe['rsi'] = ta.RSI(dataframe)
        window = 20
        dataframe['SMA'] = dataframe['close'].rolling(window=window).mean()
        # 计算标准差
        dataframe['STD'] = dataframe['close'].rolling(window=window).std()
        # 计算上轨线
        dataframe['upper_band'] = dataframe['SMA'] + 2 * dataframe['STD']
        # 计算下轨线
        dataframe['lower_band'] = dataframe['SMA'] - 2 * dataframe['STD']

        dataframe['SMA_short'] = dataframe['close'].rolling(window=5).mean()
        dataframe['SMA_long'] = dataframe['close'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(
                # (qtpylib.crossed_above(dataframe["rsi"], self.buy_rsi.value)) &
                (dataframe['SMA_short'] >= dataframe['SMA_long']) &
                (dataframe['close'] < dataframe['lower_band']) &
                (dataframe['volume'] > 0)
        ), 'enter_long',] = 1

        # dataframe.loc[(
        #         (qtpylib.crossed_above(dataframe["rsi"], self.short_rsi.value)) &
        #         (dataframe['SMA_short'] < dataframe['SMA_long']) &
        #         (dataframe['close'] > dataframe['lower_band']) &
        #         (dataframe['volume'] > 0)
        # ), 'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[(
                # (qtpylib.crossed_above(dataframe["rsi"], self.sell_rsi.value)) &
                (dataframe['SMA_short'] <= dataframe['SMA_long']) &
                (dataframe['close'] > dataframe['lower_band']) &
                (dataframe['volume'] > 0)
        ), 'exit_long',] = 1

        # dataframe.loc[(
        #         (qtpylib.crossed_above(dataframe["rsi"], self.exit_short_rsi.value)) &
        #         (dataframe['SMA_short'] > dataframe['SMA_long']) &
        #         (dataframe['close'] < dataframe['lower_band']) &
        #         (dataframe['volume'] > 0)
        # ), 'exit_short'] = 1

        return dataframe

    import pandas as pd
    import numpy as np
