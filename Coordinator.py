import Log as logging
from ZoneFileDownloader import ZoneFileDownloader


def main():
    logger = logging.setup_custom_logger("root")
    logger.debug("Init")
    zone_downloader = ZoneFileDownloader(config_path="config_prod.yaml")
    zone_downloader.build_download_urls()
    zone_downloader.download_zone_files()
    zone_downloader.write_zone_files()


if __name__ == "__main__":
    main()
