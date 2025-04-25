import logging
from configparser import ConfigParser
from typing import Any

import ccxt
from ccxt import Exchange

from constant import Config, ExchangeConfig
from crypto.common import retrier

logger = logging.getLogger(__name__)


class ExchangeWS:
    pass


class Exchange:
    def __init__(self, config: ConfigParser,exchange_config: ExchangeConfig | None = None,) -> None:
        self._api = None
        self.config = config
        self._api_async: config.Exchange
        self._markets: dict = {}
        self._last_markets_refresh: int = 0
        self._api: ccxt.Exchange

        exchange_conf: dict[str, Any] = exchange_config if exchange_config else config["exchange"]

        self.markets_refresh_interval: int = (
            exchange_conf.get("markets_refresh_interval", 60) * 60 * 1000
        )

    @property
    def name(self) -> str:
        """exchange Name (from ccxt)"""
        return self._api.name

    @property
    def id(self) -> str:
        """exchange ccxt id"""
        return self._api.id

    @property
    def markets(self) ->  dict[str, Any]:
        """exchange ccxt markets"""
        if not self._markets:
            logger.info("Markets were not loaded. Loading them now..")
            self.reload_markets(True)
        return self._markets


    @staticmethod
    def load_exchange(
            config: Config,
            *,
            exchange_config: ExchangeConfig | None = None,
            validate: bool = True,
            load_leverage_tiers: bool = False,
    ) -> Exchange:
        """
        Load the custom class from config parameter
        :param exchange_name: name of the Exchange to load
        :param config: configuration dictionary
        """
        exchange_name: str = config["exchange"]["name"]
        # Map exchange name to avoid duplicate classes for identical exchanges
        exchange_name = exchange_name.title()
        exchange = None
        try:
            exchange = Exchange._load_exchange(
                exchange_name,
                kwargs={
                    "config": config,
                    "validate": validate,
                    "exchange_config": exchange_config,
                    "load_leverage_tiers": load_leverage_tiers,
                },
            )
        except ImportError:
            logger.info(
                f"No {exchange_name} specific subclass found. Using the generic class instead."
            )
        if not exchange:
            exchange = Exchange(
                config,
                validate=validate,
                exchange_config=exchange_config,
            )
        return exchange


    @staticmethod
    def _load_exchange(exchange_name: str, kwargs: dict) -> Exchange:
        """
        Loads the specified exchange.
        Only checks for exchanges exported in freqtrade.exchanges
        :param exchange_name: name of the module to import
        :return: Exchange instance or None
        """

        try:
            ex_class = getattr(exchanges, exchange_name)

            exchange = ex_class(**kwargs)
            if exchange:
                logger.info(f"Using resolved exchange '{exchange_name}'...")
                return exchange
        except AttributeError:
            # Pass and raise ImportError instead
            pass

        raise ImportError(
            f"Impossible to load Exchange '{exchange_name}'. This class does not exist "
            "or contains Python code errors."
        )


    def check_exchange(config: Config) -> bool:
        exchange = config.get("exchange", {}).get("name", "").lower()
        if not exchange:
            logger.error("Exchange Name not configured")
            return False
        return True


    def reload_markets(self, force: bool = False, *, load_leverage_tiers: bool = True) -> None:
        """
        Reload / Initialize markets both sync and async if refresh interval has passed

        """
        # Check whether markets have to be reloaded
        is_initial = self._last_markets_refresh == 0
        from datehelper import dt_ts
        if (
            not force
            and self._last_markets_refresh > 0
            and (self._last_markets_refresh + self.markets_refresh_interval > dt_ts())
        ):
            return None
        logger.debug("Performing scheduled market reload..")
        try:
            # on initial load, we retry 3 times to ensure we get the markets
            retries: int = 3 if force else 0
            # Reload async markets, then assign them to sync api
            self._markets = retrier(self._load_async_markets, retries=retries)(reload=True)
            self._api.set_markets(self._api_async.markets, self._api_async.currencies)
            # Assign options array, as it contains some temporary information from the exchange.
            self._api.options = self._api_async.options
            if self._exchange_ws:
                # Set markets to avoid reloading on websocket api
                self._ws_async.set_markets(self._api.markets, self._api.currencies)
                self._ws_async.options = self._api.options
            self._last_markets_refresh = dt_ts()

            if is_initial and self._ft_has["needs_trading_fees"]:
                self._trading_fees = self.fetch_trading_fees()

            if load_leverage_tiers and self.trading_mode == TradingMode.FUTURES:
                self.fill_leverage_tiers()
        except (ccxt.BaseError, TemporaryError):
            logger.exception("Could not load markets.")
