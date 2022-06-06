#! /usr/bin/env python

"""
A script to generate a large number of random switches into 
the NetBox server.
"""

import pynetbox
import random


if __name__ == "__main__":
    print("Looking up details from NetBox")

    nb = pynetbox.api(
        "http://localhost:8000", token="0123456789abcdef0123456789abcdef01234567"
    )

    sites = list(nb.dcim.sites.all())
    tenants = list(nb.tenancy.tenants.all())
    tenants.append(None)
    switch_role = nb.dcim.device_roles.get(name="switch")
    device_types = nb.dcim.device_types.all()
    device_status = nb.dcim.devices.choices()["status"]
    switch_types = [
        dtype
        for dtype in device_types
        if "Nexus 9" in dtype.model or "Catalyst 93" in dtype.model
    ]

    for i in range(0, 1000):
        site = random.choice(sites)
        tenant = random.choice(tenants)
        print(f"Creating device {site.slug}-switch-{i}")
        device = nb.dcim.devices.create(
            name=f"{site.slug}-switch-{i}",
            site=site.id,
            tenant=tenant.id if tenant is not None else None,
            device_role=switch_role.id,
            device_type=random.choice(switch_types).id,
            status=random.choice(device_status)["value"],
        )
