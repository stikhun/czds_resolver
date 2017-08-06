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
        __zone_file_data = {}
        for tld, domain_list in zone_file_data.items():
            __zone_file_data[tld] = list(sorted(set(domain_list)))
        return __zone_file_data

    def clean_zone_files(self, zone_file_data):
        self.cleaned_domains = {}
        for tld in zone_file_data.keys():
            self.logger.info("Cleaning {} zone file".format(tld))
            # regex substituting in the TLD to further restrict the match
            regex_pattern = re.compile('^(.+?\.{})\..'.format(tld))
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
        for tld, domain_list in clean_zones.items():
            self.logger.info("Writing {} zone data to disk".format(tld))
            filename = "{}_clean.txt".format(tld)
            for domain in domain_list:
                with open(os.path.join(self.config_data["zone_data_path"], filename), "a") as file_handle:
                    file_handle.write("{}\n".format(domain))
