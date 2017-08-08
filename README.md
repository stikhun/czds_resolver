## Still under development

# czds_resolver
Multi-threaded zone resolver for ICANN CZDS

This is a similar tool to https://github.com/fourkitchens/czdap-tools but it is multi threaded and allows you to specify
the zones you want to download instead of downloading every single zone.

# Install
```
git clone https://github.com/stacksmash3r/czds_resolver
cd czds_resolver
pip install -r requirements.txt
```

# Usage
```
usage: Coordinator.py [-h] [--debug] [--config CONFIG] [--threads THREADS]
                      [--timeout TIMEOUT] [--clean]

optional arguments:
  -h, --help         show this help message and exit
  --debug            Enable debugging
  --config CONFIG    Path to config file
  --threads THREADS  Number of threads to use for resolving domains
  --timeout TIMEOUT  Timeout to use for DNS requests
  --clean            Format and sort zone files
```
Before running you need to update the config with your API key

# clean parameter
This is useful if you just want to get a nice clean sorted and formatted list of zones.

```
(czds_resolver) stacksmasher@fancybear:~/PycharmProjects/czds_resolver$ python Coordinator.py --config prod_config.yaml --clean
2017-08-08 21:36:30,990 - INFO - ZoneFileDownloader - Downloading data for auto TLD
2017-08-08 21:36:33,187 - INFO - ZoneFileDownloader - Downloaded auto zone file
2017-08-08 21:36:33,188 - INFO - ZoneFileDownloader - Downloading data for game TLD
2017-08-08 21:36:35,540 - INFO - ZoneFileDownloader - Downloaded game zone file
2017-08-08 21:36:35,581 - INFO - PreProcessZoneFile - Cleaning auto zone file
2017-08-08 21:36:35,587 - INFO - PreProcessZoneFile - Cleaning game zone file
2017-08-08 21:36:35,617 - INFO - PreProcessZoneFile - Writing auto zone data to disk
2017-08-08 21:36:35,621 - INFO - PreProcessZoneFile - Writing game zone data to disk
2017-08-08 21:36:35,636 - INFO - Coordinator - Finished cleaning
```

Converting data like below
```
1.auto.	900	in	ns	ns1.uniregistry-dns.com.
1.auto.	900	in	ns	ns1.uniregistry-dns.net.
1.auto.	900	in	ns	ns2.uniregistry-dns.com.
1.auto.	900	in	ns	ns2.uniregistry-dns.net.
aci.auto.	86400	in	nsec	ad.auto. NS NSEC RRSIG
aci.auto.	86400	in	rrsig	nsec	5	2	86400	20170831232020	20170801232020	4068	auto.	TWCbYA7oxpSjWIn9yUq1mCkE0Z61prvYu5OoC4n1ydX1T9VnE2y/P3vZmEN9BvID1C3uTwuZPpRQzMiKxTVC0gvPjL1v4rPzH/Nj/JK/J20eFFBWz9PYteYZ6C1tnRViXcEodpH8svsBDfN10fW3ZyP6LcldTQWZZnsZ7JO8UgyGeOQBzz7fBzH0Ur7PtXafjFq6nwgs35C5qTDMrxNHCQXKrWZXm74o8iOmmvCLkL/Y1xztjFeIJZtYNd1gSw4CjCrtIeu/ujwenvEP41GXFkewDPKlRYC7S7Kj4HEbGUWC6FR8rO3xm+f24qVR8/eRW6/D5FHPLcSUfXWdA8yiUQ==
aci.auto.	900	in	ns	ns-a.aci.it.
aci.auto.	900	in	ns	ns-b.aci.it.
ad.auto.	86400	in	nsec	adient.auto. NS NSEC RRSIG
ad.auto.	86400	in	rrsig	nsec	5	2	86400	20170831232020	20170801232020	4068	auto.	cTivPqzBKxwG4nbK/OliM6t/4cKXSGI5ysCagOH4uWjpJDYoA0BkhFWFLbUroOgu1ilF+i543cUKYIIWiGDdyowIvKbdjH5yWc28OB7ee64nvHKZ44MSfGme6tnt8WU1wvQebC2ri4WE0kfxFFYRl1oEt4WMYgDDbw59uXDUgTfVAeJgduE04oWVETRrcG6Yd8qeZZ/LUizcns4cw9KW/2/yrqT6O7h1+IlNIlg15OhqMUM9cp+eg4QBxVEYMC3B+IGLDZVS/pBO5ixTypsA/vVCgSLmT0FGBeUHjyL6b6fHKHt4wTb+rRcI8EnREBtZyCd64GFSCYYFRYB6BzMjJQ==
ad.auto.	900	in	ns	ns2.observatoiredesmarques.fr.
ad.auto.	900	in	ns	ns3.nameshield.net.
```
into this
```
1.auto.
aci.auto.
ad.auto.
```

