import os
from unittest import TestCase

import requests_mock

from ZoneFileDownloader import ZoneFileDownloader


class TestZoneFileDownloader(TestCase):
    def setUp(self):
        self.config_data = {'download_path': '/en/download-zone-data/', 'tlds': {'bid': '723', 'zone': '469'},
                            'base_url': 'https://czdap.icann.org', 'zone_data_path': 'zonedata',
                            'api_token': 'REPLACE_WITH_API_KEY'}

        self.download_urls = {
            'bid': 'https://czdap.icann.org/en/download-zone-data/723?token={}'.format(self.config_data["api_token"]),
            'zone': 'https://czdap.icann.org/en/download-zone-data/469?token={}'.format(self.config_data["api_token"])}

        self.successful_zone_fetch = {"Content-disposition": " attachment;"}

        self.zone_data = {"test": "thing"}

        self.zone_file_downloader = ZoneFileDownloader(config_path=os.path.join("..", "config.yaml"))

    def test_config_loads(self):
        """Tests if the YAML config file is being parsed correctly
        and if all key:value pairs are present
        """
        self.assertEqual(self.zone_file_downloader.config_data, self.config_data)

    def test_download_urls_built(self):
        """Checks if the download URL for each zone file is created without
        errors
        """
        self.zone_file_downloader.build_download_urls()
        self.assertEqual(self.zone_file_downloader.download_urls, self.download_urls)

    @requests_mock.mock()
    def test_fetch_zone_data(self, m):
        self.zone_file_downloader.build_download_urls()
        m.get("https://czdap.icann.org/en/download-zone-data/723?token=REPLACE_WITH_API_KEY",
              text='{"Content-disposition":"attachment;"}')
        m.get("https://czdap.icann.org/en/download-zone-data/469?token=REPLACE_WITH_API_KEY",
              text='{"Content-disposition":"attachment;"}')
        zone_data = self.zone_file_downloader.download_zone_files()
        for key in zone_data.keys():
            self.assertEqual(zone_data[key], '{"Content-disposition":"attachment;"}')
