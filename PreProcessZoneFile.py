import logging
import os
import re


class PreProcessZoneFile(object):
    def __init__(self, config_data):
        self.logger = logging.getLogger("root")
        self.logger.debug("Init")
        self.config_data = config_data
        self.logger.debug(self.config_data)

    def read_zone_files(self, zone_files):
        """Reads uncompressed zone files
        Args:
        zone_files contains the path to each zone file (dictionary)

        Returns:
        self.zone_file_data containing zone data for each zone (dictionary)
        """
        self.zone_file_data = {}
        for key, value in zone_files.items():
            with open(value, "r") as file_handle:
                self.zone_file_data[key] = file_handle.readlines()
        return self.zone_file_data

    def sort_uniq_zone_data(self, zone_file_data):
        """Unique filters and then sorts zone file data

        Args:
        zone_file_data (dictionary) containing zone file data for each
        downloaded zone file unsorted and with duplicates

        Returns:
        __zone_file_data (dictionary) containing uniqued and sorted
        zone data for each zone downloaded
        """
        __zone_file_data = {}
        for tld, domain_list in zone_file_data.items():
            __zone_file_data[tld] = list(sorted(set(domain_list)))
        return __zone_file_data

    def clean_zone_files(self, zone_file_data):
        """Extracts the second level domain and top level domain for
        each entry in the zone file

        Args:
        zone_file_data (dictionary) containing unsorted and duplicate zone data
        with extra information such as name servers for each zone

        Returns:
        self.cleaned_domains (dictionary) containing cleaned zone data such that
        nameserver entries and TTL are removed leaving only the second level domain
        and top level domain intact
        """
        self.cleaned_domains = {}
        for tld in zone_file_data.keys():
            self.logger.info("Cleaning {} zone file".format(tld))
            """Extract SLD + TLD for each entry, https://regex101.com/r/DBOckN/1"""
            regex_pattern = re.compile('^(.+?\.{})\..'.format(tld))
            # Create a TLD to list mapping
            self.cleaned_domains[tld] = []
            for domain in zone_file_data[tld]:
                domain = domain.strip("\n\t")
                result = re.match(regex_pattern, domain)
                if result:
                    domain = result.group(0).strip("\t")
                    self.cleaned_domains[tld].append(domain)
                else:
                    self.logger.debug("No match {}".format(domain))
        return self.cleaned_domains

    def write_clean_zones_to_disk(self, clean_zones):
        """Write cleaned zone file data back to disk
        Args:
        clean_zones (dictionary) containing a TLD to list mapping where
        the list contains a every SLD for that TLD
        """
        for tld, domain_list in clean_zones.items():
            self.logger.info("Writing {} zone data to disk".format(tld))
            filename = "{}_clean.txt".format(tld)
            for domain in domain_list:
                with open(os.path.join(self.config_data["zone_data_path"], filename), "a") as file_handle:
                    file_handle.write("{}\n".format(domain))
