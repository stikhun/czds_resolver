import Log as logging
from ZoneFileDownloader import ZoneFileDownloader


def main():
    logger = logging.setup_custom_logger("root")
    logger.debug("Init")
    zone_downloader = ZoneFileDownloader()


if __name__ == "__main__":
    main()
