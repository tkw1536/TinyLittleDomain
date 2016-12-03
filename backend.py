import typing
from urllib import request
from dns import resolver
import os.path
import json
import re


def _parse_json_file(*args: typing.List[str]) -> dict:
    """ Protected function to read json from a file.

    :param args: List of path segments to the file
    """

    fn = os.path.join(os.path.dirname(__file__), *args)

    with open(fn, 'r') as f:
        content = json.load(f)

    return content


def _read_tlds() -> typing.List[str]:
    """ Reads the list of top-level domains from IANA. """

    req = request.urlopen("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    lines = [line.decode('ascii').strip() for line in req]

    return [line.lower() for line in lines if not line.startswith('#')]


def does_domain_exist(name: str, servers: typing.List[str] = None) -> bool:
    """ Checks if a domain is registered by checking if there is an NS record
    for the given domain.

    :param name: Name of domain to lookup
    :param servers: Servers to use for lookup
    """

    if servers is None:
        servers = ["8.8.8.8", "8.8.4.4"]

    domain_resolver = resolver.Resolver()
    domain_resolver.nameservers = servers

    try:
        response = domain_resolver.query(name, 'NS')
        return True
    except resolver.NXDOMAIN:
        return False


RESOLVERS = _parse_json_file('static', 'data', 'resolvers.json')
TLDS = _read_tlds()

DOMAIN_REGEX = re.compile('^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$')


def get_resolver_list(name: str) -> typing.List[str]:
    """ Gets the list of resolvers for a given name.

    :raises: KeyError

    :param name: Name of resolver to get
    """

    return RESOLVERS[name]["ips"]


def is_valid_domainname(name: str) -> bool:
    """ Checks if a name is a given domain name

    :param name: Domain name to check
    """

    # split into labels
    labels = name.split(".")

    # Check if all the components are valid labels
    for l in labels:
        if DOMAIN_REGEX.match(l) is None:
            return False

    # get the top level domain name
    tld = labels[-1].lower()

    # and check if it is a valid TLD (from IANA)
    return tld in TLDS


def check_domains(server, domain):
    """ Checks a ing """

    if not is_valid_domainname(domain):
        return {
            'success': False, 'message': 'Invalid domain name'
        }

    try:
        servers = get_resolver_list(server)
    except KeyError:
        return {
            'success': False, 'message': 'Invalid server'
        }

    try:
        existence = does_domain_exist(domain, servers)
        return {
            'success': True, 'domain': domain, 'existence': existence
        }
    except:
        return {
            'success': False, 'message': 'Unknown error resolving domains'
        }
