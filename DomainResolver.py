import logging
import multiprocessing
from functools import partial

import dns.resolver


def has_a_record(timeout, domain):
    """Performs an A record lookup for the specified
    domain

    Args:
    timeout (int) representing the number of seconds to
    wait for each DNS request before moving on

    domain (str) containing a domain to check the presence
    of an A record for

    Return:
    domain (str) containing the domain that has an
    A record
    """
    retval = None
    resolves = False
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8", "8.8.4.4", "208.67.222.222", "208.67.220.220"]
        resolver.timeout = timeout
        resolver.lifetime = timeout
        reply = resolver.query(domain, "A")
        resolves = True
    except dns.resolver.NXDOMAIN as nxdomain:
        print "{}".format(nxdomain)
    except dns.resolver.NoNameservers as no_nameservers:
        print "{}".format(no_nameservers)
    except dns.exception.Timeout as timeout:
        print "{}".format(timeout)
    except dns.resolver.NoAnswer as no_answer:
        print "{}".format(no_answer)
    if resolves:
        retval = domain
    return domain

class DomainResolver(object):
    def __init__(self, config_data, threads=5, timeout=1):
        """
        Args:
        config_data (dictonary) containing parsed YAML configuration
        data

        threads (int) containing the number of sub processes to create

        timeout (int) containing the number of seconds to wait for each
        DNS request
        """
        self.logger = logging.getLogger("root")
        self.logger.debug("Init")
        self.config_data = config_data
        self.number_of_processes = threads
        self.dns_request_timeout = timeout
        self.logger.debug(self.config_data)
        self.logger.debug("Threads {}, Timeout {}".format(threads, timeout))

    def resolve_domains(self, zone_data):
        """Sets up multi processing and begins resolving domains

        Args:
        zone_data (dictonary) containing a TLD to data mapping of domains
        to be resolved
        """
        pool = multiprocessing.Pool(self.number_of_processes)
        func = partial(has_a_record, self.dns_request_timeout)
        for tld, domain_list in zone_data.items():
            for domain in pool.imap_unordered(func, domain_list):
                self.logger.info("LIVE {}".format(domain))
