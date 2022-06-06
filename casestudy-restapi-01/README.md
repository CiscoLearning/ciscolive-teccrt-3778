# Integrating Network Source of Truth into Change Control
After numerous human error issues with change control submissions involving devices and IP addressing, the decision has been made to integrate the systems together. The developers for the change control system have asked for the following information.

A curl command for each of the following targeting the NetBox API: 

* Generation of a new authentication token for a user
* A listing of all managment switches currently in inventory at site “DC1” unassigned to any tenant
    * Note: management switches are indicated by the inclusion of `mgmt` in the device name
* A list of all possible device interface type options

> Note: The NetBox server is available at address http://0.0.0.0:8000 when running on CWS using the setup instructions. 
>  Credentials: 
>    * Username: `expert`
>    * Password: `1234QWer!`


## Preperation and Setup Instructions
To prepare the CWS to work on this question you must first startup a NetBox instance.  This is easily done using the [netbox-docker](https://github.com/netbox-community/netbox-docker) project.  To make things easy to prepare for this demo a [`Makefile`](Makefile)  has been provided in this case study that includes the following targets for use.  

* `make start` 
    - Clones down the `netbox-docker` project from GitHub 
    - Uses customizations from [`netbox-configs`](netbox-configs) to get it ready for this demo
    - Adds all Cisco device types from the `device-types-library` project
    - Creates 1000 devices in NetBox that are a mixture of Nexus and Catlyst switches with different status, site and tenant values 
* `make clean` 
    - Shutdown and delete the NetBox server from the system 

> There are other targets in the Makefile that can be useful if diving deeper into the demo. Feel free to explore for details

## Documentation for Question 
During the DevNet Expert Lab Exam candidates have access to relevant documentation to complete tasks.  While working on this sample question you should make use of the NetBox documentation that is included with the application and available through links at the bottom of any NetBox web screen.  These include: 

* Docs - Full application documentation including details on REST API usage 
* REST API - a web browser API client 
* REST API Docs - an OpenAPI/Swagger browser for the API

## Solution
The file [`solution.md`](solution.md) walks through the process of solving this case study.  You are encouraged to try to work through the question on your own before checking the solution.

# Resources and Thanks 
Several open source projects were used in building this demonstration and example case study.  I wanted to call them out and say thanks for their great work. 

* First and most obviously, the [NetBox](https://github.com/netbox-community/netbox) project
* The [netbox-docker](https://github.com/netbox-community/netbox-docker) project makes running NetBox via docker very simple 
* The [NetBox device-types-library](https://github.com/netbox-community/device-types-library) project that has provided a simple and standard way for NetBox users to share device types for all the network devices we use 
* The [Netbox-Device-Type-Library-Import](https://github.com/minitriga/Netbox-Device-Type-Library-Import) project that makes importing the 500+ Cisco device types in the library easy and complete in 4 minutes 