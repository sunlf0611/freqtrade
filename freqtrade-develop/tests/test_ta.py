import talib
import numpy as np


def test_talib():
    # 生成示例数据
    close_prices = np.random.rand(100)

    # 计算 5 日简单移动平均线
    sma_5 = talib.SMA(close_prices, timeperiod=5)

    print(sma_5)