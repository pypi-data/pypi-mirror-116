import json
import re
import time
import xmltodict

from datetime import datetime, timedelta
from shutil import which
from tld import get_fld

from pyoti.exceptions import PyOTIError


HASH_TYPE = {
    re.compile(r"^[a-f0-9]{32}(:.+)?$", re.IGNORECASE): "MD5",
    re.compile(r"^[a-f0-9]{40}(:.+)?$", re.IGNORECASE): "SHA-1",
    re.compile(r"^[a-f0-9]{64}(:.+)?$", re.IGNORECASE): "SHA-256",
    re.compile(r"^[a-f0-9]{128}(:.+)?$", re.IGNORECASE): "SHA-512",
}


def get_hash_type(file_hash):
    """Determines File Hash type"""

    for regex, algorithm in HASH_TYPE.items():
        if regex.match(file_hash):

            return algorithm


def pypkg_exists(pypkg):
    """Checks if python package is installed"""

    if not which(pypkg):
        raise PyOTIError(f"{pypkg} not installed!")


def split_eml_domain(email):
    """Splits Domain from an Email Address"""

    domain = email.split("@")[1]

    return domain


def split_url_domain(url):
    """Splits first level domain from an URL"""

    return get_fld(url)


def time_check_since_epoch(epoch):
    seconds = epoch - int(time.time())
    hours = (seconds / 60) / 60
    if hours >= 1:
        return True
    else:
        return False


def time_since_epoch(epoch):
    return datetime.fromtimestamp(int(epoch)).strftime("%Y-%m-%d %H:%M:%S")


def time_since_seconds(seconds):
    return str(timedelta(seconds=seconds))


def xml_to_json(xml_object):
    """Convert XML to JSON"""

    xml_dict = xmltodict.parse(xml_object)
    dumps = json.dumps(xml_dict)
    json_data = json.loads(dumps)
    return json_data
