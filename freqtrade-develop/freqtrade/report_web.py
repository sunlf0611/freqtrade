#!/usr/bin/env python3
"""
Main Freqtrade bot script.
Read the documentation to know what cli arguments you need.
"""
import logging
import threading
import time

from freqtrade.main import main
from freqtrade.util.datetime_helpers import format_ms_time_str

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_webserver():
    try:
        args = [
            'webserver',
            '--config', '/Users/sunlongfei/Desktop/code/freqtrade-develop/config_examples/config.json'
        ]
        main(args)
    except Exception as e:
        logger.error(f"Webserver error: {e}")



def download_data():
    print("Downloading data")
    try:
        args = [
            'download-data',
            '--config', 'user_data/config.json',
            '--exchange', 'binance',
            '--days', '90', '-t', '1h'
        ]
        main(args)
    except Exception as e:
        logger.error(f"Back testing error: {e}")


def backtesting(date: str):
    print(f"Backtesting {date}")
    try:
        args = [
            'backtesting',
            '--config', 'user_data/config.json',
            '--strategy', 'MyStrategy',
            '--timerange', date, "-i", "1h"
        ]
        main(args)
    except Exception as e:
        logger.error(f"Back testing error: {e}")


def get_time() -> str:
    end = time.time()
    start = end - 90 * 24 * 60 * 60
    times = [format_ms_time_str(start), format_ms_time_str(end)]
    time_str = "-".join(times)
    return time_str


def scheduled_task():
    print("Scheduled task starting ")
    download_data()
    time_str = get_time()
    print(time_str)
    backtesting(time_str)


from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == "__main__":
    logger.info('启动 webserver')
    webserver_thread = threading.Thread(target=run_webserver)
    webserver_thread.daemon = True
    webserver_thread.start()

    backtesting("20250124-20250424")

    # scheduler = BackgroundScheduler()
    # # 每隔 10 秒执行一次任务
    # scheduler.add_job(scheduled_task, 'interval', seconds=20)
    # scheduler.start()
    # print("项目启动，定时任务已开始。")
    # try:
    #     while True:
    #         time.sleep(1)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
