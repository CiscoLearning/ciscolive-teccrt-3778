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
To prepare the CWS to work on this question you must...

* `make start` 
* `make clean` 

> There are other targets in the Makefile that can be useful if diving deeper into the demo. Feel free to explore for details

## Documentation for Question 
During the DevNet Expert Lab Exam candidates have access to relevant documentation to complete tasks.  While working on this sample question you should make use of the NSO documentation that is included with the application and available under `~/nso/docs`

## Solution
A fully working version of the NSO service is included in the director [`solution`](solution). You are encouraged to try to work through the question on your own before checking the solution.

Makefile targets have been created to startup an NSO instance using the solution. 

* `make start-solution` 

# Resources and Thanks 
