# Fix A Model-Driven Telemetry Subscription

This case study deals with using YANG-based model-driven telemetry.  In the setup for this task, a subscription has been created to monitor memory allocation utilization of a known-problematic process, but the subscription is being reported as "Invalid".  One must use tools such as `pyang` or YANG Suite to determine the correct XPath and fix the telemetry subscription.

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
make all
```

This will start Telegraf on the CWS listening on the correct port.

Note that the CWS is also connected to the external network via the default bridge0.  This means that if you have a DHCP server on your CML server's network, the CWS will get an address from that, and then be reachable via SSH and RDP using the "expert" credentials shown above.

## Documentation for the Question

The router servicing Branch Office 003 has been experiencing a memory leak in the “IP ARP Retry Ager” process.  Regular tracking of allocated and freed memory needs to be done to isolate when the leak begins to occur.  In order to reduce overhead from polling, model-driven telemetry is being used.  However, the configuration is not working.  

The subscription is reporting that the YANG filter path is **Invalid**.

* On `rtr-br003-01` (192.168.5.150):

  * Correct the XPath filter so that the telemetry subscription properly delivers memory data for the IP ARP Retry Ager process to the Telegraf server
  * Provide the corrected path in the `rtr-br003-01.txt` file in your code directory

> Note: The desired YANG module, `Cisco-IOS-XE-process-memory-oper.yang` is available in your code directory and `pyang` and YANG Suite are available on your workstation for exploring this module.  YANG Suite is available at <http://localhost:8480>.

A convenience script, `deploy-telemetry.py` is available in your code directory to do the deployment of the configuration.  Once you have the configuration correct in the `rtr-br003.txt` file, run `./deploy-telemetry.py` to push the changes to the device.

Once telemetry is properly configured, you will see output written to the `telegraf/metrics/metrics.json` file.

## Resources

YANG Suite can be accessed using the following credentials:

**Username:** expert

**Password:** 1234QWer!

The device sending the telemetry stream, rtr-br003-01, can be accessed via SSH with the following credentials:

**Username:** expert

**Password:** 1234QWer!

## Solution

The solution is provided in the `code_solution` directory with some comments in the `rtr-br003-01.txt` file as to what was done.
