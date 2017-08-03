import gzip
import logging
import os

import requests
import yaml
from requests import ConnectionError, Timeout
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

    def download_zone_files(self):
        """Downloads each zone file specified in the config file, the buffered is stored
        in a key:value dictionary so the data can be associated with the zone it is for

        Each zone file provided by the API is gzipped
        """
        self.zone_data = {}
        for key, value in self.download_urls.items():
            self.logger.debug("Downloading data for {} TLD".format(key))
            try:
                response = requests.get(value)
                if response.ok:
                    self.logger.debug("Downloaded {} zone data".format(key))
                    self.zone_data[key] = response.content
                else:
                    self.logger.debug("Got {} response while downloading {} zone data", response.status_code, key)
            except ConnectionError as connection_error:
                self.logger.error("Requests connection error {}".format(connection_error.errno))
            except Timeout as timeout:
                self.logger.error("Requests timeout {}".format(timeout.errno))
        return self.zone_data

    def write_zone_files(self):
        "Writes the gzipped files to disk storing their paths and zone name in a dict"
        self.filenames_compressed = {}
        for key, value in self.zone_data.items():
            self.filenames_compressed[key] = (os.path.join("zonedata", "{}.txt.gz".format(key)))
            with open(self.filenames_compressed[key], "wb") as file_handle:
                file_handle.write(value)
        return self.filenames_compressed

    def extract_zone_files(self):
        "Extracts the contents of each gzipped file and writes the decompressed data back to disk"
        self.filenames_decompressed = {}
        for key, value in self.filenames_compressed.items():
            file_handle_in = gzip.open(value)
            self.filenames_decompressed[key] = os.path.join("zonedata", "{}.txt".format(key))
            with open(self.filenames_decompressed[key], "wb") as file_handle_out:
                file_handle_out.write(file_handle_in.read())
            file_handle_in.close()
        return self.filenames_decompressed

    def remove_compressed_files(self):
        "Removes the gzipped file for each zone"
        for value in self.filenames_compressed.values():
            os.remove(value)
