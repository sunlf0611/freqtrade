



class LoadData:
    def __init__(self):
        pass


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









