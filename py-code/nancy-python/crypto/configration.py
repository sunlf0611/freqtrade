import json
import logging
from configparser import ConfigParser

from crypto.constant import Config

logger = logging.getLogger(__name__)

class Configration:
    def __init__(self, config: ConfigParser,file_path: str) -> None:
        self.config = config
        self.config_path = file_path


    def get_config(self) -> Config:
        """
        Return the config. Use this method to get the bot config
        :return: Dict: Bot config
        """
        if self.config is None:
            self.config = self.load_config()
        return self.config

    def load_config(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
                return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path} ")
        except json.decoder.JSONDecodeError:
            logger.error("Load config file not valid json")



