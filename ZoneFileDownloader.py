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

    def build_download_urls(self):
        """Creates the URLs required to download each zone file"""
        tlds = self.config_data.get("tlds")
        self.logger.debug("TLDs {}".format(tlds))
        self.logger.debug("# TLDs {}".format(len(tlds)))
        self.download_urls = {}
        # tld, code api expects
        for key, value in tlds.items():
            self.logger.debug("TLD:CODE {0}:{1}".format(key, value))
            # base url + download path + tld code + api token
            self.download_urls[key] = "{0}{1}{2}?token={3}".format(self.config_data.get("base_url"),
                                                                   self.config_data.get("download_path"), value,
                                                                   self.config_data.get("api_token"))
            self.logger.debug("built url {}".format(self.download_urls))
