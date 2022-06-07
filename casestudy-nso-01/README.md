# Creating a service to manage Access Lists
A network service is being created to manage access control lists on CPE routers at branch locations using NSO. CRUD requests of this service will come from multiple systems including web applications, service catalogs, and orchestrators.

Given the below desired final configuration for an example service instance, you are to: 

* Complete the XML configuration template that will be used by the service to render final device configurations
    * TODOs have been included in the XML template to align to requirements
* Update the YANG model for the service match the service definition resources and requirements below
    * TODOs have been included in YANG model to align to requirements
    * Be sure to compile and include the final YANG model in your solution
* Apply the XML configuration template in the Python script passing in the variables that are created from YANG data.
    * TODOs have been included in the Python file to align to requirements

The following requirements have been provided by the network architect: 

* Every rule will include a `LABEL` and `DESCRIPTION` remark directly before the rule entry in the configured access-list 
    * See below examples for formating details
* Variable names and values for the XML template have been defined in Python already. Use these names in the XML template.
* Access list and rule names cannot contain any white spaces. This must be enforced in the YANG model.
    * The regex pattern `[\S]*` can be used to match valid names
* Valid actions for a rule are "deny" or "permit" only. This must be enforced in the YANG model.
* Valid protocols for a rule are "tcp" or "udp" only. This must be enforced in the YANG model.
* Source and Destination address leafs should support either IPv4 address or prefixes using the `ietf-inet-types`. This must be enforced in the YANG model.
* Source ports can be any valid port number, however destination ports must be limited to well known ports (1 - 1024). This must be enforced in YANG. 
* The log attribute of a rule should be a leaf that is either present or not. 
* The default rule action, rule description, source port, and log flag are the only optional leafs in the model

## Configurations and Resources 
### pyang Tree representation of model 

```text
module: acl-service
  +--rw access-list* [name]
     +--rw name                        string
     +--rw device*                     -> /ncs:devices/device/name
     +--rw default
     |  +--rw rule?   enumeration
     +--rw rule* [name]
        +--rw name           string
        +--rw description?   string
        +--rw action         enumeration
        +--rw protocol       enumeration
        +--rw source
        |  +--rw address    union
        |  +--rw port?      uint16
        +--rw destination
        |  +--rw address    union
        |  +--rw port       uint16
        +--rw log?           empty
```

### Example service configuration and rendered device configuration
#### Service Configuration

> Note: This configuration available in [validations/PASS-basic-acl.xml](validations/PASS-basic-acl.xml).
> 
> Apply with `ncs_load -u admin -lm validations/PASS-basic-acl.xml` or `load merge validation-files/PASS-basic-acl.xml` from `ncs_cli` config mode.

```
access-list web-servers
 device [ ios-1 ]
 rule https-web1
  description "Allow inbound https access"
  action      permit
  protocol    tcp
  source address 0.0.0.0/0
  destination address 192.168.10.11
  destination port 443
 !
!
```

#### Resulting Configuration 

> Note: Generated with a `commit dry-run`

```
cli {
    local-node {
        data +access-list web-servers {
             +    device [ ios-1 ];
             +    rule https-web1 {
             +        description "Allow inbound https access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 0.0.0.0/0;
             +        }
             +        destination {
             +            address 192.168.10.11;
             +            port 443;
             +        }
             +    }
             +}
              devices {
                  device ios-1 {
                      config {
                          ip {
                              access-list {
                                  extended {
             +                        ext-named-acl web-servers {
             +                            ext-access-list-rule "10 remark Rule https-web1 in ACL Service web-servers";
             +                            ext-access-list-rule "11 remark Description Allow inbound https access";
             +                            ext-access-list-rule "12 permit tcp any host 192.168.10.11 eq 443";
             +                            ext-access-list-rule "100 remark Default Rule in ACL Service web-servers";
             +                            ext-access-list-rule "101 remark Description deny all";
             +                            ext-access-list-rule "102 deny ip any any log";
             +                        }
                                  }
                              }
                          }
                      }
                  }
              }
    }
}
```

> Note: The above is an example and doesn't represent the full extent of requirements for this question.


## Preperation and Setup Instructions
### Installing NSO 
To prepare the CWS to work on this question you must first perform a local installation of NSO on the CWS.  The files can be downloaded from [DevNet](https://developer.cisco.com/docs/nso/#!getting-and-installing-nso). You will need the Linux installer as well as the IOS XE NED.  Assuming you download these files onto the CWS into the `~/Downloads` directory, you can install it with these commands: 

```bash
# Delete the placeholder ~/nso directory on the CWS 
rm -rf ~/nso

cd ~/Downloads

# Make the signed download executable and run it 
chmod +x nso-5.7.1.linux.x86_64.signed.bin 
./nso-5.7.1.linux.x86_64.signed.bin 

# Make the installer file executable 
chmod +x nso-5.7.1.linux.x86_64.installer.bin

# Perform a local installation of nso
./nso-5.7.1.linux.x86_64.installer.bin --local-install ~/nso

# Change into the NEDs directory for the newly installed NSO
cd ~/nso/packages/neds

# Extract the IOS NED into the local installation directory 
tar -zxvf ~/Downloads/ncs-5.7-cisco-ios-6.77.10.tar.gz 

# Add sourcing ~/nso/ncsrc to the bashrc file 
echo "source ~/nso/ncsrc" >> ~/.bashrc 
```

### Starting up the NSO instance for the question
To make it easier to get right into the question, a [`Makefile`](Makefile) has been included with several targets that handle the details of preparing the CWS for this question. 

* `make start` 
    - uses `ncs-netsim` to create a small network with 2 IOS CLI devices for development and testing
    - uses `ncs-setup` to create a local NSO instance with the NEDs and package for the question
    - starts the `ncs-netsim` network 
    - starts nso and verifies it is fully up and operational 
    - performs a sync-from on the netsim devices to nso 
* `make clean` 
    - shutdown nso and delete all files from the local instance 
    - shutdown the netsim network and delete all files from the project

> There are other targets in the Makefile that can be useful if diving deeper into the demo. Feel free to explore for details

## Documentation for Question 
During the DevNet Expert Lab Exam candidates have access to relevant documentation to complete tasks.  While working on this sample question you should make use of the NSO documentation that is included with the application and available under `~/nso/docs`

## Validating your answer 
The directory [`validation-files`](validation-files) includes several XML files that can be loaded into NSO to verify your solution.  Files that start with `PASS` should load and apply configurations to the network. Files that start with `FAIL` should generate some error upon loading.  These are there to test constraints have been properly applied in the solution. 

> Note: These validation files are provided to help with studying.  They are not a full grading service and it is possible that your solution may not fully meet the requirements if these work. Efforts have been made to provide robust examples for validation, but some elements may have been missed.

## Solution
A fully working version of the NSO service is included in the director [`solution`](solution). You are encouraged to try to work through the question on your own before checking the solution.

Makefile targets have been created to startup an NSO instance using the solution. 

* `make start-solution` 

# Resources
For more details on Cisco NSO, see the [DevNet NSO Page](https://developer.cisco.com/site/nso/).
