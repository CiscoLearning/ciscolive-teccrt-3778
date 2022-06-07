"""Utility functions and resources for the service"""

import ipaddress

# IOS converts well known ports to names in configuration
ios_acl_port_map = {
    179: {"name": "bgp", "description": "Border Gateway Protocol (179)"},
    19: {"name": "chargen", "description": "Character generator (19)"},
    514: {"name": "cmd", "description": "Remote commands (rcmd, 514)"},
    13: {"name": "daytime", "description": "Daytime (13)"},
    9: {"name": "discard", "description": "Discard (9)"},
    53: {"name": "domain", "description": "Domain Name Service (53)"},
    7: {"name": "echo", "description": "Echo (7)"},
    512: {"name": "exec", "description": "Exec (rsh, 512)"},
    79: {"name": "finger", "description": "Finger (79)"},
    21: {"name": "ftp", "description": "File Transfer Protocol (21)"},
    20: {"name": "ftp-data", "description": "FTP data connections (20)"},
    70: {"name": "gopher", "description": "Gopher (70)"},
    101: {"name": "hostname", "description": "NIC hostname server (101)"},
    113: {"name": "ident", "description": "Ident Protocol (113)"},
    194: {"name": "irc", "description": "Internet Relay Chat (194)"},
    543: {"name": "klogin", "description": "Kerberos login (543)"},
    544: {"name": "kshell", "description": "Kerberos shell (544)"},
    513: {"name": "login", "description": "Login (rlogin, 513)"},
    515: {"name": "lpd", "description": "Printer service (515)"},
    135: {"name": "msrpc", "description": "MS Remote Procedure Call (135)"},
    119: {"name": "nntp", "description": "Network News Transport Protocol (119)"},
    15001: {"name": "onep-plain", "description": "Onep Cleartext (15001)"},
    15002: {"name": "onep-tls", "description": "Onep TLS (15002)"},
    496: {"name": "pim-auto-rp", "description": "PIM Auto-RP (496)"},
    109: {"name": "pop2", "description": "Post Office Protocol v2 (109)"},
    110: {"name": "pop3", "description": "Post Office Protocol v3 (110)"},
    25: {"name": "smtp", "description": "Simple Mail Transport Protocol (25)"},
    111: {"name": "sunrpc", "description": "Sun Remote Procedure Call (111)"},
    514: {"name": "syslog", "description": "Syslog (514)"},
    49: {"name": "tacacs", "description": "TAC Access Control System (49)"},
    517: {"name": "talk", "description": "Talk (517)"},
    23: {"name": "telnet", "description": "Telnet (23)"},
    37: {"name": "time", "description": "Time (37)"},
    540: {"name": "uucp", "description": "Unix-to-Unix Copy Program (540)"},
    43: {"name": "whois", "description": "Nicname (43)"},
    80: {"name": "www", "description": "World Wide Web (HTTP, 80)"},
}


def acl_address(address: str) -> str:
    """Convert a YANG address or network to ACL format"""
    address = ipaddress.ip_network(address)
    if address.netmask == ipaddress.IPv4Address("255.255.255.255"):
        acl_address = f"host {address.network_address}"
    elif address.netmask == ipaddress.IPv4Address(
        "0.0.0.0"
    ) and address.network_address == ipaddress.IPv4Address("0.0.0.0"):
        acl_address = f"any"
    else:
        acl_address = f"{address.network_address} {address.hostmask}"

    return acl_address
