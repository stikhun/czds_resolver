import logging

import yaml
from yaml import YAMLError


class ZoneFileDownloader(object):
    config_file_path = None

    def __init__(self, config_path=None):
        """Gets global logger and sets config file path

        Keyword Arguments:
            config_path -- path to the config file including
            the config file itself
        """
        self.logger = logging.getLogger("root")
        if config_path:
            self.config_file_path = config_path
        else:
            self.config_file_path = "config.yaml"
        self.__load_config_file()

    def __load_config_file(self):
        """Loads config data including which zones to download

        Returns:
            self.config_data -- containing a dictionary of config values
        """
        with open(self.config_file_path, "r") as file_handle:
            try:
                self.config_data = yaml.load(file_handle)
            except YAMLError as yaml_error:
                print yaml_error
        self.logger.debug("Config data {}".format(self.config_data))
        return self.config_data
