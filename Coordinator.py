import argparse

import Log as logging
from ZoneFileDownloader import ZoneFileDownloader


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--debug", action="store_true",
        help="Enable debugging"
    )
    argument_parser.add_argument(
        "--config", action="store",
        help="Path to config file"
    )
    argument_parser.add_argument(
        "--threads", action="store",
        help="Number of threads to use for resolving domains"
    )
    argument_parser.add_argument(
        "--timeout", action="store",
        help="Timeout to use for DNS requests"
    )
    arguments = argument_parser.parse_args()

    if arguments.debug:
        logger = logging.setup_custom_logger("root", debug=True)
    else:
        logger = logging.setup_custom_logger("root")

    # Download zone files and extract them
    if arguments.config:
        zone_downloader = ZoneFileDownloader(config_path=arguments.config)
    else:
        zone_downloader = ZoneFileDownloader()
    zone_downloader.build_download_urls()
    zone_downloader.download_zone_files()
    zone_downloader.write_zone_files()
    zone_downloader.extract_zone_files()
    zone_downloader.remove_compressed_files()



if __name__ == "__main__":
    main()
