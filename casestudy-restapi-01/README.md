# Integrating Network Source of Truth into Change Control
After numerous human error issues with change control submissions involving devices and IP addressing, the decision has been made to integrate the systems together. The developers for the change control system have asked for the following information.

A curl command for each of the following targeting the NetBox API: 

* Generation of a new authentication token for a user
* A listing of all managment switches currently in inventory at site “DC1” unassigned to any tenant
    * Note: management switches are indicated by the inclusion of `mgmt` in the device name
* A list of all possible device interface type options

## Preperation and Setup Instructions
To prepare the CWS to work on this question you must first startup a NetBox instance.  This is easily done using the [netbox-docker](https://github.com/netbox-community/netbox-docker) project.  For 


# Resources and Thanks 
Several open source projects were used in building this demonstration and example case study.  I wanted to call them out and say thanks for their great work. 

* First and most obviously, the [NetBox](https://github.com/netbox-community/netbox) project
* The [netbox-docker](https://github.com/netbox-community/netbox-docker) project makes running NetBox via docker very simple 
* The [NetBox device-types-library](https://github.com/netbox-community/device-types-library) project that has provided a simple and standard way for NetBox users to share device types for all the network devices we use 
* The [Netbox-Device-Type-Library-Import](https://github.com/minitriga/Netbox-Device-Type-Library-Import) project that makes importing the 500+ Cisco device types in the library easy and complete in 4 minutes 