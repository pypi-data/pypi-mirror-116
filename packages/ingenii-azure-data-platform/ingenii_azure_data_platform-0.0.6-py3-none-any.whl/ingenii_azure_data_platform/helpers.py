import os
from ipaddress import ip_network
from typing import Any


def ensure_type(value, types):
    """
    This function checks if a value is of certain type.
    """
    if isinstance(value, types):
        return value
    else:
        raise TypeError(f"Value {value} is {type(value),}, but should be {types}!")


def get_os_root_path() -> str:
    """
    Returns the root path of the current operating system.
    Unix/MacOS = "/"
    Windows = "c:"
    """
    return os.path.abspath(os.sep)


def cidrsubnet(cidr_subnet: str, new_prefix: int, network_number: int) -> Any:
    """
    Calculates a new subnet number based on the inputs provided.
    """
    return list(ip_network(cidr_subnet).subnets(new_prefix=new_prefix))[
        network_number
    ].exploded
