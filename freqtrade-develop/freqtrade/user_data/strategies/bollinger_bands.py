

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# 1. 数据获取
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# 2. 计算布林带
def calculate_bollinger_bands(data, window=20, std_dev=2):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper_Band'] = data['SMA'] + (data['STD'] * std_dev)
    data['Lower_Band'] = data['SMA'] - (data['STD'] * std_dev)
    return data

# 3. 生成交易信号
def generate_signals(data):
    signals = []
    position = 0  # 0: 无持仓, 1: 持有多头

    for i in range(len(data)):
        if data['Close'][i] < data['Lower_Band'][i] and position == 0:
            signals.append(1)  # 买入信号
            position = 1
        elif data['Close'][i] > data['Upper_Band'][i] and position == 1:
            signals.append(-1)  # 卖出信号
            position = 0
        else:
            signals.append(0)  # 无信号

    data['Signal'] = signals
    return data

# 4. 回测策略
def backtest(data):
    initial_capital = 100000  # 初始资金
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    positions['Stock'] = data['Signal']

    portfolio = positions.multiply(data['Close'], axis=0)
    pos_diff = positions.diff()

    portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

    return portfolio

# 主函数
def main():
    ticker = 'BA'  # 股票代码
    start_date = '2025-01-01'
    end_date = '2025-03-01'

    # 获取数据
    data = get_stock_data(ticker, start_date, end_date)
    # 计算布林带
    data = calculate_bollinger_bands(data)
    # 生成交易信号
    data = generate_signals(data)
    # 回测策略
    portfolio = backtest(data)

    # 绘制图表
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['SMA'], label='SMA')
    plt.plot(data['Upper_Band'], label='Upper Band')
    plt.plot(data['Lower_Band'], label='Lower Band')
    plt.scatter(data[data['Signal'] == 1].index, data[data['Signal'] == 1]['Close'], marker='^', color='g', label='Buy Signal')
    plt.scatter(data[data['Signal'] == -1].index, data[data['Signal'] == -1]['Close'], marker='v', color='r', label='Sell Signal')
    plt.title('Bollinger Bands Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    # 打印最终资产
    # final_capital = portfolio['total'].iloc[-1]
    # print(f"初始资金: {100000}")
    # print(f"最终资产: {final_capital}")
    # print(f"收益率: {(final_capital - 100000) / 100000 * 100:.2f}%")

if __name__ == "__main__":
    main()