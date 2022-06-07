# Troubleshoot YANG XPath for Telemetry Subscription

This case study deals with using YANG-based model-driven telemetry.  In the setup for this task, a subscription has been created to monitor DHCP pool capacity, but the subscription is being reported as "Invalid".  One must use tools such as `pyang` or YANG Suite to determine the correct XPath and fix the telemetry subscription.

The telemetry data will be processed by Telegraf, which will be running within a Docker container on the Candidate Workstation image.  The element sending the telemetry is a Catalyst 8000v, which is acting as the default gateway for a remote branch office.  Cisco Modeling Labs (CML) is required for this task.  A topology file is provided in `Case Study Telemetry.yaml`, which can be imported into a CML Personal, Enterprise, or Education server.  CML 2.3 or higher is required.

## Starting the Task

First, import the `Case Study Telemetry.yaml` file into a CML server, and then start the lab.  Wait until all nodes are fully started.

You will need to download the CWS [QCOW2 image](https://learningcontent.cisco.com/images/2022-04-08_DevNetExpert_CWS_Example.qcow2) and the corresponding [node definition](https://github.com/CiscoDevNet/cml-community/tree/master/node-definitions/cisco/cws) and load them into your CML server.  The CWS is part of this topology so that the whole task is self-contained.

Login to the `cws` node in the CML topology with the credentials:

**Username:** expert

**Password:** 1234QWer!

Then run the following commands:

```sh
su -c "sudo ip addr add 192.168.4.27/23 dev ens4"
su -c "sudo ip link set up ens4"
```

When prompted for a password, use 1234QWer! again.

Clone this git repo onto the CWS within the CML lab topology.  Then change directory to `casestudy-telemetry-01` and run the following command:

```sh
docker-compose up -d
```

This will start Telegraf on the CWS listening on the correct port.
