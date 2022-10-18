#! /usr/bin/env python
import ipaddress
import argparse
import os
import requests


class AddressAction(argparse.Action):
    """Convert an IP address string to IPNetwork or IPAddress object"""

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            address = ipaddress.ip_network(values)
            if address.num_addresses == 1:
                address = ipaddress.ip_address(address.network_address)
        except ValueError:
            raise ValueError(
                f"The value provided '{values}' is invalid. Must be either 'any' or an address in CIDR format ('192.168.1.0/24')"
            )

        setattr(namespace, self.dest, address)


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


def build_payload(args: argparse.Namespace) -> dict:
    """Create a dictionary payload for the new rule"""

    # TODO (alt): Create a Python object representing the payload for creating a new rule
    #             Be sure that the payload supports all possible input variations for 
    #             mandatory and optional parameters
    # Notes: 
    #   - The following arguments are available from the `args` parameter
    #     args.acl > access-list name 
    #     args.rule > rule name 
    #     args.action > permit/deny value 
    #     args.protocol > tcp/udp 
    #     args.source > source address as ipaddress.IPv4Address or IPv4.Network object
    #     args.destination > destination address as ipaddress.IPv4Address or IPv4.Network object
    #     args.sport / args.dport > source/destionation ports 
    #     args.description > optional description for rule entry 
    #     args.log > true/false on whether to log hits to rule 
    payload = {
        "acl-service:rule": [
            {
                "name": args.rule,
                "action": args.action,
                "protocol": args.protocol,
                "source": {
                    "address": args.source.exploded,
                },
                "destination": {
                    "address": args.destination.exploded,
                    "port": args.dport,
                },
            }
        ]
    }

    # The description needs to be omitted if not configured
    if args.description:
        payload["acl-service:rule"][0]["description"] = args.description

    # The source port needs to be omitted if not configured
    if args.sport:
        payload["acl-service:rule"][0]["source"]["port"] = args.sport

    # The log leaf is either present or not
    if args.log:
        payload["acl-service:rule"][0]["log"] = [None]

    # sport remove if None

    return payload


def test_nso(server: str, username, password):
    """Verify NSO server address is reachable."""
    url = f"{server}/.well-known/host-meta"
    headers = {
        "Accept": "application/yang-data+json",
    }
    response = requests.get(url, headers=headers, auth=(username, password))
    response.raise_for_status()


def add_rule(
    server: str, username: str, password: str, args: argparse.Namespace
) -> bool:
    """Add a new rule to an ACL Service on an NSO Server"""
    test_nso(server, username, password)

    # TODO: Set the value of URL to the correct path to add a new rule to an ACL
    # Notes: 
    #   - the variable `server` is equal to the NSO address including the protocol and port
    #     for example: http://127.0.0.1:8080
    #   - The following arguments are available from the `args` parameter
    #     args.acl > access-list name 
    #     args.rule > rule name 
    #     args.action > permit/deny value 
    #     args.protocol > tcp/udp 
    #     args.source > source address as ipaddress.IPv4Address or IPv4.Network object
    #     args.destination > destination address as ipaddress.IPv4Address or IPv4.Network object
    #     args.sport / args.dport > source/destionation ports 
    #     args.description > optional description for rule entry 
    #     args.log > true/false on whether to log hits to rule 
    url = f""

    headers = {
        "Content-type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
    }
    body = build_payload(args)

    response = requests.post(url, json=body, headers=headers, auth=(username, password))

    # Check response status code for expected values for conditions
    # TODO: Leverage the response status code to determine results based on comments for each test
    # 1. A successful creation of new rule 
    if True == True:
        return True
    # 2. An error due to the rule already existing 
    elif True == True:
        raise ValueError(f"rule {args.rule} already exists on access-list {args.acl}")
    # 3. An error due to the named access-list not existing
    elif True == True:
        raise ValueError(f"access-list {args.acl} not found.")
    # 4. An error due to the access-list service not being available in NSO 
    elif True == True:
        raise ValueError(f"The acl-service:access-list not found on the NSO server.")
    else:
        return False


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
        "action",
        choices=["permit", "deny"],
        help="The permit / deny action to take on the rule",
    )
    parser.add_argument(
        "protocol",
        choices=["tcp", "udp"],
        help="Which protocol TCP / UDP the rule applies to",
    )
    parser.add_argument(
        "source",
        action=AddressAction,
        help="The source address for the access-list. Format in CIDR format (ie 192.168.1.0/24)",
    )
    parser.add_argument(
        "destination",
        action=AddressAction,
        help="The destination address for the access-list. Format in CIDR format (ie 192.168.1.0/24)",
    )
    parser.add_argument(
        "dport",
        type=int,
        help="The destination port for the access-list.",
    )
    parser.add_argument(
        "--sport",
        type=int,
        help="The source port for the access-list.",
    )
    parser.add_argument(
        "--description",
        type=str,
        help="The description for the rule",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Whether to log hits to the rule.",
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
    result = add_rule(server, username, password, arguments)
