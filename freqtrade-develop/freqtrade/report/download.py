import logging
import sys
from typing import Any

from freqtrade.commands.data_commands import _check_data_config_download_sanity
from freqtrade.commands.optimize_commands import setup_optimize_configuration
from freqtrade.enums import RunMode

logger = logging.getLogger(__name__)

def start_download_data(args: dict[str, Any]) -> None:
    """
    Download data (former download_backtest_data.py script)
    """
    from freqtrade.configuration import setup_utils_configuration
    from freqtrade.data.history import download_data_main

    config = setup_utils_configuration(args, RunMode.UTIL_EXCHANGE)

    _check_data_config_download_sanity(config)

    try:
        download_data_main(config)

    except KeyboardInterrupt:
        sys.exit("SIGINT received, aborting ...")



def start_backtesting(args: dict[str, Any]) -> None:
    """
    Start Backtesting script
    :param args: Cli args from Arguments()
    :return: None
    """
    # Import here to avoid loading backtesting module when it's not used
    from freqtrade.optimize.backtesting import Backtesting

    # Initialize configuration
    config = setup_optimize_configuration(args, RunMode.BACKTEST)

    logger.info("Starting freqtrade in Backtesting mode")

    # Initialize backtesting object
    backtesting = Backtesting(config)
    backtesting.start()

