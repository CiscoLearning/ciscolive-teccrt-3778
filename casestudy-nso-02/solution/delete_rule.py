import ipaddress
import argparse
import os
import requests


def nso_details(args: argparse.Namespace) -> tuple[str, str, str]:
    """Return the server, username, and password for NSO from arguments or ENV"""

    details = {"server": None, "username": None, "password": None}
    for key in details:
        details[key] = (
            args.__dict__[f"nso_{key}"]
            if args.__dict__[f"nso_{key}"] is not None
            else os.getenv(f"NSO_{key.upper()}")
        )

    if None in details.values():
        raise ValueError(
            "Values for NSO Server, Username, and Password must be provided as arguments or ENVs"
        )

    return details["server"], details["username"], details["password"]


def test_nso(server: str):
    """Verify NSO server address is reachable."""
    url = f"{server}/.well-known/host-meta"
    response = requests.get(url)
    response.raise_for_status()


def delete_rule(server: str, username: str, password: str, args: argparse.Namespace):
    """Delete a rule from an ACL Service on an NSO Server"""
    test_nso(server)

    url = f"{server}/restconf/data/acl-service:access-list={args.acl}/rule={args.rule}"

    response = requests.delete(url, auth=(username, password))
    response.raise_for_status()

    return response


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Add a rule to an ACL Service in NSO.")
    parser.add_argument(
        "acl",
        type=str,
        help="The name of the access-list",
    )
    parser.add_argument(
        "rule",
        type=str,
        help="The name of the rule",
    )
    parser.add_argument(
        "--nso-server",
        type=str,
        help="The address of the NSO server. If not provided an ENV of 'NSO_SERVER' must be set",
    )
    parser.add_argument(
        "--nso-username",
        type=str,
        help="The username for the NSO server. If not provide an ENV of 'NSO_USERNAME' must be set",
    )
    parser.add_argument(
        "--nso-password",
        type=str,
        help="The password for the NSO server. If not provide an ENV of 'NSO_USERNAME' must be set",
    )

    arguments = parser.parse_args()

    # Determine NSO Server Connection Details
    server, username, password = nso_details(arguments)

    # Attempt to add the rule to NSO
    result = delete_rule(server, username, password, arguments)
