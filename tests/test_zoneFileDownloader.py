import os
from unittest import TestCase

from ZoneFileDownloader import ZoneFileDownloader


class TestZoneFileDownloader(TestCase):
    def setUp(self):
        self.config_data = {'download_path': '/en/download-zone-data/', 'tlds': {'bid': '723', 'zone': '469'},
                            'base_url': 'https://czdap.icann.org', 'zone_data_path': 'zonedata', 'api_token': ''}

        self.zone_file_downloader = ZoneFileDownloader(config_path=os.path.join("..", "config.yaml"))

    def test_config_loads(self):
        """Tests if the YAML config file is being parsed correctly
        and if all key:value pairs are present
        """
        self.assertEqual(self.zone_file_downloader.config_data, self.config_data)
