#!/usr/bin/env python3
"""
Main Freqtrade bot script.
Read the documentation to know what cli arguments you need.
"""

import threading
import time
import logging

from pandas import DataFrame

from freqtrade.main import main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_trade():
    try:
        args = [
            'trade',
            '--config', '/Users/sunlongfei/Desktop/code/freqtrade-develop/config_examples/config.json',
            '--strategy', 'SampleStrategy'
        ]
        main(args)
    except Exception as e:
        logger.error(f"Trade error: {e}")


def run_webserver():
    try:
        args = [
            'webserver',
            '--config', '/Users/sunlongfei/Desktop/code/freqtrade-develop/config_examples/config.json'
        ]
        main(args)
    except Exception as e:
        logger.error(f"Webserver error: {e}")


def run_back_testing():
    try:
        args = [
            'backtesting',
            '--config', 'user_data/config.json',
            '--strategy', 'SampleStrategy',
        ]
        main(args)
    except Exception as e:
        logger.error(f"Back testing error: {e}")


def download_data():
    try:
        args = [
            'download-data',
            '--config', 'user_data/config.json',
            '--exchange', 'binance'
        ]
        main(args)
    except Exception as e:
        logger.error(f"Back testing error: {e}")


def report():
    try:
        args = [
            'download-data',
            '--config', 'user_data/config.json',
            '--exchange', 'binance'
        ]
        main(args)
    except Exception as e:
        logger.error(f"Back testing error: {e}")


if __name__ == "__main__":
    logger.info('启动 webserver')
    webserver_thread = threading.Thread(target=run_webserver)
    webserver_thread.daemon = True
    webserver_thread.start()

    logger.info('启动交易机器人')
    # run_back_testing()
    # logger.info('启动backtesting机器人')
    download_data()




from pandas.core.frame import DataFrame

def advise_all_indicators( data: dict[str, DataFrame]) -> dict[str, dict[str, DataFrame]]:
    """
    Populates indicators for given candle (OHLCV) data (for multiple pairs)
    Does not run advise_entry or advise_exit!
    Used by optimize operations only, not during dry / live runs.
    Using .copy() to get a fresh copy of the dataframe for every strategy run.
    Also copy on output to avoid PerformanceWarnings pandas 1.3.0 started to show.
    Has positive effects on memory usage for whatever reason - also when
    using only one strategy.
    """
    return {
        pair: advise_indicators(pair_data.copy(), {"pair": pair}).copy()
        for pair, pair_data in data.items()
    }

def advise_indicators( data: dict[str, DataFrame],pair:dict[str,str]) -> dict[str, DataFrame]:
    print(data)
    return data