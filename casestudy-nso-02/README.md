# Working with Model Driven APIs
A network service is being created to manage access control lists on CPE routers at branch locations using NSO. CRUD requests of this service will come from multiple systems including web applications, service catalogs, and orchestrators.

You will be completing example code (`add_rule.py`) for integrating with this service.

Given the YANG model for this new service you must: 
* Determine the RESTCONF resource path for creating a new rule on an existing access-list
* Evaluate the results of the creation API call to validate success and indicate error causes

> TODOs have been placed in the code to direct you to where work must be completed

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

### Example of a rule configured using the model
```
admin@ncs# show running-config access-list full-rule-set rule host-to-host 

access-list full-rule-set
 rule host-to-host
  description "Allow inbound smtp access"
  action      permit
  protocol    tcp
  source address 192.168.1.1
  destination address 192.168.10.11
  destination port 25
  log
```

### Details on the RESTCONF endpoint for the NSO Server

```
curl -u admin:admin http://0.0.0.0:8080/.well-known/host-meta

<XRD xmlns='http://docs.oasis-open.org/ns/xri/xrd-1.0'>
    <Link rel='restconf' href='/restconf'/>
</XRD>
```



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
    - populates NSO with an access-list you can add rules to with the script
* `make clean` 
    - shutdown nso and delete all files from the local instance 
    - shutdown the netsim network and delete all files from the project

> There are other targets in the Makefile that can be useful if diving deeper into the demo. Feel free to explore for details

## Documentation for Question 
During the DevNet Expert Lab Exam candidates have access to relevant documentation to complete tasks.  While working on this sample question you should make use of the NSO documentation that is included with the application and available under `~/nso/docs`

## Validating your answer 
Here are a few examples using the `add_rule.py` script with the expected results.

> Note: These examples are provided to help with studying.  They are not a full grading service and it is possible that your solution may not fully meet the requirements if these work. Efforts have been made to provide robust examples for validation, but some elements may have been missed.

1. Successfully create a rule 

    ```bash
    ./add_rule.py \
      full-rule-set newrule deny tcp 0.0.0.0/0 192.168.1.10/32 80 \
      --nso-username admin --nso-password admin \
      --nso-server http://0.0.0.0:8080
    ```

    * Result: No output
    * Check NSO 

        ```bash
        echo "show running-config access-list full-rule-set rule newrule" | ncs_cli -C -u admin -n

        # OUPUT
        admin connected from 10.192.81.4 using ssh on expert-cws
        admin@ncs# show running-config access-list full-rule-set rule newrule
        access-list full-rule-set
         rule newrule
          action   deny
          protocol tcp
          source address 0.0.0.0/0
          destination address 192.168.1.10
          destination port 80
         !
        !
        ```

1. Attempt to create existing rule

    ```bash
    ./add_rule.py \
      full-rule-set newrule deny tcp 0.0.0.0/0 192.168.1.10/32 80 \
      --nso-username admin --nso-password admin \
      --nso-server http://0.0.0.0:8080
    ```

    * Result: Error

    ```python
    Traceback (most recent call last):
    File "/home/expert/src/ciscolive-teccrt-3778/casestudy-nso-02/solution/./add_rule.py", line 226, in <module>
        result = add_rule(server, username, password, arguments)
    File "/home/expert/src/ciscolive-teccrt-3778/casestudy-nso-02/solution/./add_rule.py", line 140, in add_rule
        raise ValueError(f"rule {args.rule} already exists on access-list {args.acl}")
    ValueError: rule newrule already exists on access-list full-rule-set
    ```

1. Attempt to add rule to access-list that does NOT exist

    ```bash
    ./add_rule.py \
      invalid-acl newrule deny tcp 0.0.0.0/0 192.168.1.10/32 80 \
      --nso-username admin --nso-password admin \
      --nso-server http://0.0.0.0:8080
    ```

    * Result: Error

    ```python
    Traceback (most recent call last):
    File "/home/expert/src/ciscolive-teccrt-3778/casestudy-nso-02/solution/./add_rule.py", line 226, in <module>
        result = add_rule(server, username, password, arguments)
    File "/home/expert/src/ciscolive-teccrt-3778/casestudy-nso-02/solution/./add_rule.py", line 143, in add_rule
        raise ValueError(f"access-list {args.acl} not found.")
    ValueError: access-list invalid-acl not found.
    ```

1. Successfully create a rule with all optional options

    ```bash
    ./add_rule.py \
      full-rule-set customapp permit tcp 10.10.32.0/28 172.16.45.111/32 85 \
      --sport 7654 \
      --description "Allow access for custom application and log" \
      --log \
      --nso-username admin --nso-password admin \
      --nso-server http://0.0.0.0:8080
    ```

    * Result: No output
    * Check NSO 

        ```bash
        echo "show running-config access-list full-rule-set rule customapp" | ncs_cli -C -u admin -n

        # OUPUT
        admin connected from 10.192.81.4 using ssh on expert-cws
        admin@ncs# show running-config access-list full-rule-set rule customapp
        access-list full-rule-set
         rule customapp
          description "Allow access for custom application and log"
          action      permit
          protocol    tcp
          source address 10.10.32.0/28
          source port 7654
          destination address 172.16.45.111
          destination port 85
          log
         !
        !        
        ```

## Solution
A fully working version of the script is included in the directory [`solution`](solution). You are encouraged to try to work through the question on your own before checking the solution.

There is also a `delete_rule.py` script that can be used to remove rules from NSO in a similar fashion as the `add_rule.py` script. 

# Resources
For more details on Cisco NSO, see the [DevNet NSO Page](https://developer.cisco.com/site/nso/).
