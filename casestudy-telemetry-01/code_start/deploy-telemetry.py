#!/usr/bin/env python

from scrapli.driver.core import IOSXEDriver, NXOSDriver
import logging

DEVICE_USERNAME = "expert"
DEVICE_PASSWORD = "1234QWer!"

RTR_DEVICE = {
    "host": "192.168.5.150",
    "auth_username": DEVICE_USERNAME,
    "auth_password": DEVICE_PASSWORD,
    "auth_strict_key": False,
}

RTR_CONFIG = "rtr-br003-01.txt"


def deploy_rtr_config() -> bool:
    """Deploy router config.

    Returns:
        result (bool): True if config was deployed successfully, False otherwise.
    """
    with IOSXEDriver(**RTR_DEVICE) as conn:
        responses = conn.send_configs_from_file(RTR_CONFIG)
        for response in responses:
            try:
                response.raise_for_status()
            except Exception as e:
                logging.exception(
                    f"ERROR: Failed to deploy config to {RTR_DEVICE['host']}: {e}"
                )
                return False

    return True


def main() -> None:
    """Initial entry point."""

    result = deploy_rtr_config()

    if not result:
        exit(1)


if __name__ == "__main__":
    main()
