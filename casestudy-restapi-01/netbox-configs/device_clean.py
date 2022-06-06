#! /usr/bin/env python 

"""
A script to delete all devices from NetBox server.
"""

import pynetbox


if __name__ == "__main__":
    print("Deleting all devices from NetBox")

    nb = pynetbox.api(
        "http://localhost:8000", token="0123456789abcdef0123456789abcdef01234567"
    )

    nb.dcim.devices.delete(nb.dcim.devices.all(0))
