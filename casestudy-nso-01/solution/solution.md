# Solution: Creating a service to manage Access Lists
This is a walkthrough solution to this example question.  Where relevant, links to documentation are included. 

## Question Text
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

> Note: See the [Case Study README](../README.md) for the example configurations and resources that suppor the question text.

## Question Analysis
This question requires the candidate to complete an NSO Service that has already been partially created.  This will require updates to the three main parts of an NSO "python and template" service. 

1. The XML configuration template used to render device configurations
1. The YANG model that describes the service data model
1. The Python script that is called and ran for service creation and maintenance

For each of the three parts of the solution, `TODO` indications are included in the code that will help candidates focus their work and make sure all steps are completed. It is also important to cross-check the constraints/requirements that are included in the question.  Some of these constraints are "techincal", while others are more "architectural policy".  It doesn't matter whether you (the candidate) agree with the constraints, they must be followed to correctly solve this question.  

The question also includes several "validation-files" that can be used to test whether our solution works.  This will be helpful when we are complete. 

> Note: The order the three parts of this question are completed matter little.  All three components of the service work together so testing along the way would be difficult.  This is different from develping a service from scratch where it is common to test along the way.  This is one significant difference between working on an exam question and building your own services or scripts. 

## Part 1: The XML Configuration Template
We'll start with the XML template configuration. Opening the file will reveal there are **5** TODOs that each indicate the need to provide the correct variables within the configuration.  The question details indicate that the variable names are already identified and declared in the Python script.  So using that file the following changes are made. 

> Note: for convenience in the solution the "original" line is commented out and left above the solution line below. 

<details><summary>XML Template Solution: acl-service-template.xml</summary>

```xml
<config-template xmlns="http://tail-f.com/ns/config/1.0">
  <devices xmlns="http://tail-f.com/ns/ncs">
    <device>
      <!-- TODO: Provide the proper variable for device -->
      <!-- <name>NETWORK_DEVICE</name> -->
      <name>{$DEVICE_NAME}</name>
      <config>
        <ip xmlns="urn:ios">
          <access-list>
            <extended>
              <ext-named-acl>
                <!-- TODO: Provide the proper variable for ACL name -->
                <!-- <name>ACL</name> -->
                <name>{$ACL_NAME}</name>
                <ext-access-list-rule>
                  <!-- TODO: Update "label" rule to include the correct sequence and value -->
                  <!-- <rule>LABEL_# remark LABEL_TEXT</rule> -->
                  <rule>{$LABEL_SEQ} remark {$LABEL}</rule>
                </ext-access-list-rule>
                <ext-access-list-rule>
                  <!-- TODO: Update the "description" rule to include correct sequence and value -->
                  <!-- <rule>DESC # remark DESCRIPTION_TEXT</rule> -->
                  <rule>{$DESC_SEQ} remark {$DESCRIPTION}</rule>
                </ext-access-list-rule>
                <ext-access-list-rule>
                  <!-- TODO: Provide the proper variable for the rule line -->
                  <!-- <rule>RULE_LINE</rule> -->
                  <rule>{$RULE}</rule>
                </ext-access-list-rule>
              </ext-named-acl>
            </extended>
          </access-list>
        </ip>
      </config>
    </device>
  </devices>
</config-template>
```

</details>

## Part 2: The YANG Model
Next up we'll tackle the updates to the YANG model. 

Looking at the YANG model you will find **9** TODOs indicating updates to make.  Several of these TODOs are for similar changes so we'll group them together in this solution walkthrough. 

> Note: In this section, only the relevant parts of the YANG model will be shown.  The full solution YANG file is available at [`acl-service/src/yang/acl-service.yang`](acl-service/src/yang/acl-service.yang). 

### Requiring names without whitespace 
Both the `access-list\name` and `rule\name` values must be configured in YANG to not allow whitespace characters.  The question text provides a regex that can be used to check for this state.  The [`pattern` statement](https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.5) can be used in YANG to check input against a regex.

Here is an example applying this pattern to the `access-list\name`. 

```yang
// TODO: Rule names can NOT have whitespace
leaf name {
    tailf:info "Unique name for this access-list";
    tailf:cli-allow-range;
    type string {
        pattern '[\S]*';
    } 
}
```

### Limiting the possible choices for a leaf
TODOs and constraints exist that state

* Possible actions for rules must be limited to `deny` and `permit` 
* Only `tcp` and `udp` are allowed for protocols 

For these constraints, the best solution is the [`enumeration`](https://datatracker.ietf.org/doc/html/rfc7950#section-9.6) YANG type.  Here is an example using this type for the protocol configuration.  

```yang
// TODO: Only the valus of "tcp" or "udp" should be allowed
leaf protocol { 
    mandatory true;
    tailf:info "tcp/udp";
    type enumeration {
        enum tcp; 
        enum udp; 
    }
}
```

> Hint: The pyang output provided with the question indicates `enumeration` as the data type for these fields already.

### Allowing one of two types for a leaf 
The `source\address` and `destination\address` leafs need to support two different data types.  

Both from the `ietf-inet-types`:

* `ipv4-address`
* `ipv4-prefix`

> Note: The YANG module already includes the `import` statement for `ietf-inet-types` with a prefix of `inet`

The best solution for this is to leverage the [`union`](https://datatracker.ietf.org/doc/html/rfc7950#section-9.12) datatype which allows the definition of a list of possible supported data types for a leaf.  Here is an example of this solution for the `source\address` leaf. 

```yang
// TODO: allow IPv4 address or prefix based on ietf-inet-types
leaf address {
  mandatory true;
  tailf:info "The source address for this rule";
  type union {
    type inet:ipv4-address;
    type inet:ipv4-prefix;
  }
}
```

> Hint: The pyang output provided with the question indicates `union` as the data type for these fields already. 

### Limit the ports supported for `destination\port`
The question states that only "well-known (1-1024)" ports are to be supported for `destination\port`.  This field is configured to a `type uint16` which allows for valid values of `0 - 65535` which is great when any valid tcp/udp port is supported, such as for `source\port`. 

The best option to limit the values for an integer based data type is the [`range`](https://datatracker.ietf.org/doc/html/rfc7950#section-9.2.4) statement.  Here is an example configuration that uses this solution. 

```yang
// TODO: Only allow well known ports (1 - 1024)
leaf port {
  mandatory true;
  tailf:info "The destination port for this rule";
  type uint16{
    range 1..1024;
  }
}
```

### Configure a presence based log leaf 
Whether to capture logs for a rule or not needs to be a simple "flag" in the rule defintion.  Currently the `log` leaf is configured as `type string` which requires some value to be set for `log`.  

The best option for this is to use the [`empty`](https://datatracker.ietf.org/doc/html/rfc7950#section-9.11) for the leaf.  This turns a leaf into having meaning depending on whether it is "present" or "absent" from the configuration.  Here is an example using this configuration for `log`. 

```yang
// TODO: The log leaf should either be present or not
leaf log {
  tailf:info "Whether to log hits to this rule";
  type empty;
}
```

### Compiling the changed YANG model 
The YANG source file you make the changes in isn't actually used by NSO.  NSO needs a compiled YANG module of format `fxs`.  This can be created by running `make` from the `acl-service/src` directory.  

## Part 3: Applying the template in Python 
The final step in our solution is to update the Python script to apply the template.  This is done in the `main.py` file under `acl-service/python/acl_service`.  Within the file you'll find **2** TODOs for the same addition.  The first to apply for all configured `rules`, and the second for the `default` rule.  

The `template` object is already defined in the `cb_create()` method: 

```python
template = ncs.template.Template(service)
```

And the variables object has been defined and already populated with the proper values.  

```python
vars = ncs.template.Variables()

vars.add("ACL_NAME", service.name)

# And many others
```

The command needed to apply the template just needs to be added at the `TODO` spots. 

```python
# TODO: Apply the template named "acl-service-template" using the configured vars
template.apply("acl-service-template", vars)
```

## Checking the solution
We can check our solution using the `validation-files` provided. 

### Testing the `FAIL`s
First up, let's check that the constraints are being met. 

#### ACL and Rule Names lack whitespace 
If either of these two configurations are accepted, check the `pattern` configuration. 

***ACL Name***

```
admin@ncs(config)# load merge validation-files/FAIL-bad-acl-name.xml 
Loading.
Error: on line 3: invalid value for: name in /access-list/name
```

***Rule Name***

```
admin@ncs(config)# load merge validation-files/FAIL-bad-rule-name.xml 
Loading.
Error: on line 6: invalid value for: name in /access-list/rule/name
```

#### Rule action only permit/deny 
If this is accepted, check the enumeration configuration. 

```
admin@ncs(config)# load merge validation-files/FAIL-bad-rule-action.xml 
Loading.
Error: on line 8: invalid value for: action in /acl-service:access-list[acl-service:name='web-servers']/acl-service:rule[acl-service:name='https-web1']/acl-service:action: "allow" is an invalid value.
```

#### Source/Destination address 
If this is accepted, check the union configuration

```
admin@ncs(config)# load merge validation-files/FAIL-bad-rule-address.xml 
Loading.
Error: on line 11: invalid value for: address in /acl-service:access-list[acl-service:name='web-servers']/acl-service:rule[acl-service:name='https-web1']/acl-service:source/acl-service:address: "any" is not a valid value.
```

#### Protocol values tcp/udp
If this is accepted, check the enumeration on the protocol configuration. 

```
admin@ncs(config)# load merge validation-files/FAIL-bad-rule-protocol.xml 
Loading.
Error: on line 9: invalid value for: protocol in /acl-service:access-list[acl-service:name='web-servers']/acl-service:rule[acl-service:name='https-web1']/acl-service:protocol: "TCP" is an invalid value.
```

#### Destination port value 
If this is accepted, check the range on the `destination\port`

```
admin@ncs(config)# load merge validation-files/FAIL-bad-dest-port.xml 
Loading.
Error: on line 15: invalid value for: port in /acl-service:access-list[acl-service:name='web-servers']/acl-service:rule[acl-service:name='https-web1']/acl-service:destination/acl-service:port: "9443" is out of range.
```

### Testing the `PASS`s
Now we can test the configurations that should work.  

#### A basic ACL configuration
This first check is a single rule ACL to do a basic test. 

```
admin@ncs(config)# load merge validation-files/PASS-basic-acl.xml 
Loading.
536 bytes parsed in 0.00 sec (69.52 KiB/sec)


admin@ncs(config)# show configuration 
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

<details><summary>`commit dry-run`</summary>

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

</details>

### A comprehensive ACL example
This second exmaple includes many rules that check the different variations possible with the configuration.

```
admin@ncs(config)# load merge validation-files/PASS-comprehensive.xml 
Loading.
3.03 KiB parsed in 0.01 sec (210.53 KiB/sec)


admin@ncs(config)# show config
access-list full-rule-set
 device [ ios-1 ]
 rule host-to-host
  description "Allow inbound smtp access"
  action      permit
  protocol    tcp
  source address 192.168.1.1
  destination address 192.168.10.11
  destination port 25
  log
 !
 rule host-to-net
  description "Allow inbound mgmt access"
  action      permit
  protocol    tcp
  source address 192.168.1.5
  destination address 192.168.11.0/24
  destination port 22
  log
 !
 rule net-to-host
  description "Allow inbound ftp access"
  action      permit
  protocol    tcp
  source address 192.168.0.0/16
  destination address 192.168.10.16
  destination port 21
  log
 !
 rule any-to-host
  description "Allow inbound dns access"
  action      permit
  protocol    udp
  source address 0.0.0.0/0
  destination address 192.168.10.20
  destination port 53
  log
 !
 rule host-to-any
  description "Allow inbound dns-tcp access"
  action      permit
  protocol    tcp
  source address 192.168.15.5
  destination address 0.0.0.0/0
  destination port 53
  log
 !
 rule any-to-any
  description "Allow inbound https access"
  action      permit
  protocol    tcp
  source address 0.0.0.0/0
  destination address 0.0.0.0/0
  destination port 443
  log
 !
 rule src-port
  description "Allow inbound app access"
  action      permit
  protocol    tcp
  source address 192.168.5.0/26
  source port 333
  destination address 192.168.17.16
  destination port 333
  log
 !
 rule no-log
  description "Allow telnet access - no log"
  action      permit
  protocol    tcp
  source address 192.168.5.0/26
  destination address 192.168.17.16
  destination port 23
 !
!
```

<details><summary>`commit dry-run`</summary>

```
cli {
    local-node {
        data +access-list full-rule-set {
             +    device [ ios-1 ];
             +    rule host-to-host {
             +        description "Allow inbound smtp access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 192.168.1.1;
             +        }
             +        destination {
             +            address 192.168.10.11;
             +            port 25;
             +        }
             +        log;
             +    }
             +    rule host-to-net {
             +        description "Allow inbound mgmt access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 192.168.1.5;
             +        }
             +        destination {
             +            address 192.168.11.0/24;
             +            port 22;
             +        }
             +        log;
             +    }
             +    rule net-to-host {
             +        description "Allow inbound ftp access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 192.168.0.0/16;
             +        }
             +        destination {
             +            address 192.168.10.16;
             +            port 21;
             +        }
             +        log;
             +    }
             +    rule any-to-host {
             +        description "Allow inbound dns access";
             +        action permit;
             +        protocol udp;
             +        source {
             +            address 0.0.0.0/0;
             +        }
             +        destination {
             +            address 192.168.10.20;
             +            port 53;
             +        }
             +        log;
             +    }
             +    rule host-to-any {
             +        description "Allow inbound dns-tcp access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 192.168.15.5;
             +        }
             +        destination {
             +            address 0.0.0.0/0;
             +            port 53;
             +        }
             +        log;
             +    }
             +    rule any-to-any {
             +        description "Allow inbound https access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 0.0.0.0/0;
             +        }
             +        destination {
             +            address 0.0.0.0/0;
             +            port 443;
             +        }
             +        log;
             +    }
             +    rule src-port {
             +        description "Allow inbound app access";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 192.168.5.0/26;
             +            port 333;
             +        }
             +        destination {
             +            address 192.168.17.16;
             +            port 333;
             +        }
             +        log;
             +    }
             +    rule no-log {
             +        description "Allow telnet access - no log";
             +        action permit;
             +        protocol tcp;
             +        source {
             +            address 192.168.5.0/26;
             +        }
             +        destination {
             +            address 192.168.17.16;
             +            port 23;
             +        }
             +    }
             +}
              devices {
                  device ios-1 {
                      config {
                          ip {
                              access-list {
                                  extended {
             +                        ext-named-acl full-rule-set {
             +                            ext-access-list-rule "10 remark Rule host-to-host in ACL Service full-rule-set";
             +                            ext-access-list-rule "11 remark Description Allow inbound smtp access";
             +                            ext-access-list-rule "12 permit tcp host 192.168.1.1 host 192.168.10.11 eq smtp log";
             +                            ext-access-list-rule "20 remark Rule host-to-net in ACL Service full-rule-set";
             +                            ext-access-list-rule "21 remark Description Allow inbound mgmt access";
             +                            ext-access-list-rule "22 permit tcp host 192.168.1.5 192.168.11.0 0.0.0.255 eq 22 log";
             +                            ext-access-list-rule "30 remark Rule net-to-host in ACL Service full-rule-set";
             +                            ext-access-list-rule "31 remark Description Allow inbound ftp access";
             +                            ext-access-list-rule "32 permit tcp 192.168.0.0 0.0.255.255 host 192.168.10.16 eq ftp log";
             +                            ext-access-list-rule "40 remark Rule any-to-host in ACL Service full-rule-set";
             +                            ext-access-list-rule "41 remark Description Allow inbound dns access";
             +                            ext-access-list-rule "42 permit udp any host 192.168.10.20 eq domain log";
             +                            ext-access-list-rule "50 remark Rule host-to-any in ACL Service full-rule-set";
             +                            ext-access-list-rule "51 remark Description Allow inbound dns-tcp access";
             +                            ext-access-list-rule "52 permit tcp host 192.168.15.5 any eq domain log";
             +                            ext-access-list-rule "60 remark Rule any-to-any in ACL Service full-rule-set";
             +                            ext-access-list-rule "61 remark Description Allow inbound https access";
             +                            ext-access-list-rule "62 permit tcp any any eq 443 log";
             +                            ext-access-list-rule "70 remark Rule src-port in ACL Service full-rule-set";
             +                            ext-access-list-rule "71 remark Description Allow inbound app access";
             +                            ext-access-list-rule "72 permit tcp 192.168.5.0 0.0.0.63 eq 333 host 192.168.17.16 eq 333 log";
             +                            ext-access-list-rule "80 remark Rule no-log in ACL Service full-rule-set";
             +                            ext-access-list-rule "81 remark Description Allow telnet access - no log";
             +                            ext-access-list-rule "82 permit tcp 192.168.5.0 0.0.0.63 host 192.168.17.16 eq telnet";
             +                            ext-access-list-rule "170 remark Default Rule in ACL Service full-rule-set";
             +                            ext-access-list-rule "171 remark Description deny all";
             +                            ext-access-list-rule "172 deny ip any any log";
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

</details>