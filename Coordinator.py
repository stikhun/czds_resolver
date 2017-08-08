import argparse

import Log as logging
from DomainResolver import DomainResolver
from PreProcessZoneFile import PreProcessZoneFile
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
        type=int,
        help="Number of threads to use for resolving domains"
    )
    argument_parser.add_argument(
        "--timeout", action="store",
        type=int,
        help="Timeout to use for DNS requests"
    )
    argument_parser.add_argument(
        "--clean", action="store_true",
        help="Format and sort zone files"
    )
    arguments = argument_parser.parse_args()

    if arguments.debug:
        logger = logging.setup_custom_logger("root", debug=True)
    else:
        logger = logging.setup_custom_logger("root")

    if arguments.config:
        zone_downloader = ZoneFileDownloader(config_path=arguments.config)
    else:
        zone_downloader = ZoneFileDownloader()
    zone_downloader.build_download_urls()
    zone_downloader.download_zone_files()
    zone_downloader.write_zone_files()
    zone_file_paths = zone_downloader.extract_zone_files()
    zone_downloader.remove_compressed_files()

    config_data = zone_downloader.get_config_data()
    zone_preprocessor = PreProcessZoneFile(config_data)
    zone_file_data = zone_preprocessor.read_zone_files(zone_file_paths)
    extracted_zone_data = zone_preprocessor.clean_zone_files(zone_file_data)
    cleaned_zone_data = zone_preprocessor.sort_uniq_zone_data(extracted_zone_data)
    zone_preprocessor.write_clean_zones_to_disk(cleaned_zone_data)
    if arguments.clean:
        logger.info("Finished cleaning")
        exit(0)

    domain_resolver = DomainResolver(config_data, threads=arguments.threads, timeout=arguments.timeout)
    domain_resolver.resolve_domains(cleaned_zone_data)


if __name__ == "__main__":
    main()
