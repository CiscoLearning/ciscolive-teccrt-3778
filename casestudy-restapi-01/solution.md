# Solution: Integrating Network Source of Truth into Change Control
This is a walkthrough solution to this example question.  Where relevant, links to documentation are included. 

## Question Text
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

## Question Analysis
This question asks for three specific `curl` commands to be provided. 

> Note: This question requires some basic knowledge of how NetBox works.  If you are unfamilar with NetBox, you'll need to take time during the exam to review the interface and documentation.  
> 
> You may think "but NetBox is ***NOT*** on the Software and Equipment List for the exam.  This is true, but Blueprint 2.4 reads: 
>  * "Consume and use a *new* REST API, given the documentation"
> 
> An important skill for a senior automation engineer is the ability to quickly leverage a new REST API as new ones may come across your workstation quite regularly.  Any resources needed related to an unfamilar REST API will be provided during the lab exam. And time to understand the new system is included in the allocation for a question.

1. Generation of a new authentication token for a user
    * Username/Password credentials are provided, however all API requests to NetBox require a token
    * The ability to create a token via API is useful when trying to fully automate an integration 
1. A listing of all managment switches currently in inventory at site “DC1” unassigned to any tenant
    * This will be a `GET` request from the API for `devices` endpoints
    * There are multiple filter/limitation indications in the question that need to be addressed 
        * a status of "inventory" 
        * at site "DC1" 
        * unassigned to any tenant 
        * "management switches" indicated by `mgmt` in the device name 
1. A list of all possible device interface type options 
    * Interfaces have a type field that has a set of valid options in NetBox
    * Will need to find an API to list these values 

## Part 1: Creation of an authentication token 
The [NetBox Docs](http://0.0.0.0:8000/static/docs/integrations/rest-api/#initial-token-provisioning) provide details on how to create a token for a user. 

This curl request will generate a token for user and return the details in JSON.

> Note: I am using the `jq` (jquery) utility to make displaying and working with the returned JSON simpler

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    http://0.0.0.0:8000/api/users/tokens/provision/ \
    --data '{"username": "expert","password": "1234QWer!"}' | jq .
```

<details><summary>Example Output</summary>

```json
{
  "id": 5,
  "url": "http://0.0.0.0:8000/api/users/tokens/5/",
  "display": "1f13f3 (expert)",
  "user": {
    "id": 2,
    "url": "http://0.0.0.0:8000/api/users/users/2/",
    "display": "expert",
    "username": "expert"
  },
  "created": "2022-06-06T20:50:26.975998Z",
  "expires": null,
  "key": "c55cdb851c2b0dfc4660e528ee4b9e13a51f13f3",
  "write_enabled": true,
  "description": ""
}
```

</details>

## Part 2: Filtered Device Listing 
All the details needed on how to filter API requests with NetBox are listed in the [Docs](http://0.0.0.0:8000/static/docs/reference/filtering/).  Also of use is the [OpenAPI interface](http://0.0.0.0:8000/api/docs/) to the API available for NetBox.  The `devices` endpoint is under the `dcim` application/category. 

We can build up the full filtered request one requirement at a time. 

1. Lookup ***ALL*** devices. 

    ```bash
    curl -X GET "http://0.0.0.0:8000/api/dcim/devices/" \
        -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
        | jq .count
    ```

    <details><summary>Example Output</summary>

    ```json
    1000
    ```

    </details>

1. Filter for a status of `inventory`

    ```bash
    curl -X GET "http://0.0.0.0:8000/api/dcim/devices/?status=inventory" \
        -H  "accept: application/json" \
        -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
        | jq .count
    ```

    <details><summary>Example Output</summary>

    ```json
    161
    ```

    </details>

1. Filter for a site value of `DC1`

    ```bash
    curl -X GET "http://0.0.0.0:8000/api/dcim/devices/?status=inventory&site=dc1" \
        -H  "accept: application/json" \
        -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
        | jq .count
    ```

    > Note the value used for `DC1` is lowercase `dc1`.  This is because NetBox uses the `slug` field for filters.

    <details><summary>Example Output</summary>

    ```json
    33
    ```

    </details>

1. Filter for no tenant assigned.

    ```bash
    curl -X GET "http://0.0.0.0:8000/api/dcim/devices/?status=inventory&site=dc1&tenant=null" \
        -H  "accept: application/json" \
        -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
        | jq .count
    ```

    > Note that `null` is used for the tenant value to align to JSON standard

    <details><summary>Example Output</summary>

    ```json
    7
    ```

    </details>

1. Filter for Management switches.

    ```bash
    curl -X GET "http://0.0.0.0:8000/api/dcim/devices/?status=inventory&site=dc1&tenant=null&name__ic=mgmt" \
        -H  "accept: application/json" \
        -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
        | jq .count
    ```

    > How to use lookup expressions like "Contains" are detailed in the [Docs](http://0.0.0.0:8000/static/docs/rest-api/filtering/#string-fields)

    <details><summary>Example Output</summary>

    ```json
    2
    ```

    </details>

1. Here is the final query with all data included in the example output. 

    ```bash
    curl -X GET "http://0.0.0.0:8000/api/dcim/devices/?status=inventory&site=dc1&tenant=null&name__ic=mgmt" \
        -H  "accept: application/json" \
        -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
        | jq .
    ```


    <details><summary>Example Output</summary>

    ```json
    {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
        "id": 1314,
        "url": "http://0.0.0.0:8000/api/dcim/devices/1314/",
        "display": "dc1-mgmt-switch-302",
        "name": "dc1-mgmt-switch-302",
        "device_type": {
            "id": 457,
            "url": "http://0.0.0.0:8000/api/dcim/device-types/457/",
            "display": "Catalyst 9300L-48P-4G",
            "manufacturer": {
            "id": 1,
            "url": "http://0.0.0.0:8000/api/dcim/manufacturers/1/",
            "display": "Cisco",
            "name": "Cisco",
            "slug": "cisco"
            },
            "model": "Catalyst 9300L-48P-4G",
            "slug": "c9300l-48p-4g"
        },
        "device_role": {
            "id": 1,
            "url": "http://0.0.0.0:8000/api/dcim/device-roles/1/",
            "display": "switch",
            "name": "switch",
            "slug": "switch"
        },
        "tenant": null,
        "platform": null,
        "serial": "",
        "asset_tag": null,
        "site": {
            "id": 1,
            "url": "http://0.0.0.0:8000/api/dcim/sites/1/",
            "display": "DC1",
            "name": "DC1",
            "slug": "dc1"
        },
        "location": null,
        "rack": null,
        "position": null,
        "face": null,
        "parent_device": null,
        "status": {
            "value": "inventory",
            "label": "Inventory"
        },
        "airflow": null,
        "primary_ip": null,
        "primary_ip4": null,
        "primary_ip6": null,
        "cluster": null,
        "virtual_chassis": null,
        "vc_position": null,
        "vc_priority": null,
        "comments": "",
        "local_context_data": null,
        "tags": [],
        "custom_fields": {},
        "config_context": {},
        "created": "2022-06-06T20:10:37.030925Z",
        "last_updated": "2022-06-06T20:10:37.030944Z"
        },
        {
        "id": 1979,
        "url": "http://0.0.0.0:8000/api/dcim/devices/1979/",
        "display": "dc1-mgmt-switch-967",
        "name": "dc1-mgmt-switch-967",
        "device_type": {
            "id": 145,
            "url": "http://0.0.0.0:8000/api/dcim/device-types/145/",
            "display": "Catalyst 9300L-24P-4G",
            "manufacturer": {
            "id": 1,
            "url": "http://0.0.0.0:8000/api/dcim/manufacturers/1/",
            "display": "Cisco",
            "name": "Cisco",
            "slug": "cisco"
            },
            "model": "Catalyst 9300L-24P-4G",
            "slug": "c9300l-24p-4g"
        },
        "device_role": {
            "id": 1,
            "url": "http://0.0.0.0:8000/api/dcim/device-roles/1/",
            "display": "switch",
            "name": "switch",
            "slug": "switch"
        },
        "tenant": null,
        "platform": null,
        "serial": "",
        "asset_tag": null,
        "site": {
            "id": 1,
            "url": "http://0.0.0.0:8000/api/dcim/sites/1/",
            "display": "DC1",
            "name": "DC1",
            "slug": "dc1"
        },
        "location": null,
        "rack": null,
        "position": null,
        "face": null,
        "parent_device": null,
        "status": {
            "value": "inventory",
            "label": "Inventory"
        },
        "airflow": null,
        "primary_ip": null,
        "primary_ip4": null,
        "primary_ip6": null,
        "cluster": null,
        "virtual_chassis": null,
        "vc_position": null,
        "vc_priority": null,
        "comments": "",
        "local_context_data": null,
        "tags": [],
        "custom_fields": {},
        "config_context": {},
        "created": "2022-06-06T20:12:15.060252Z",
        "last_updated": "2022-06-06T20:12:15.060270Z"
        }
    ]
    }
    ```
    </details>

## Part 3: An API for interface type choices 
The [NetBox Docs on Filtering include a section on using choice fields](http://0.0.0.0:8000/static/docs/reference/filtering/#filtering-by-choice-field) that provide all the details needed to build this API request.

```bash
curl -X OPTIONS "http://0.0.0.0:8000/api/dcim/interfaces/" \
    -H  "accept: application/json" \
    -H  "Authorization: Token 0123456789abcdef0123456789abcdef01234567" \
    | jq .actions.POST.type
```

> Note that all relevant "Choices" for interface configuration are returned with this query.  To find just the interface types a developer needs to parse through the returned object to the details desired. `jq` is used to do that in this example solution. 

<details><summary>Example Output</summary>

```json
{
  "type": "field",
  "required": true,
  "read_only": false,
  "label": "Type",
  "choices": [
    {
      "value": "virtual",
      "display_name": "Virtual"
    },
    {
      "value": "bridge",
      "display_name": "Bridge"
    },
    {
      "value": "lag",
      "display_name": "Link Aggregation Group (LAG)"
    },
    {
      "value": "100base-tx",
      "display_name": "100BASE-TX (10/100ME)"
    },
    {
      "value": "1000base-t",
      "display_name": "1000BASE-T (1GE)"
    },
    {
      "value": "2.5gbase-t",
      "display_name": "2.5GBASE-T (2.5GE)"
    },
    {
      "value": "5gbase-t",
      "display_name": "5GBASE-T (5GE)"
    },
    {
      "value": "10gbase-t",
      "display_name": "10GBASE-T (10GE)"
    },
    {
      "value": "10gbase-cx4",
      "display_name": "10GBASE-CX4 (10GE)"
    },
    {
      "value": "1000base-x-gbic",
      "display_name": "GBIC (1GE)"
    },
    {
      "value": "1000base-x-sfp",
      "display_name": "SFP (1GE)"
    },
    {
      "value": "10gbase-x-sfpp",
      "display_name": "SFP+ (10GE)"
    },
    {
      "value": "10gbase-x-xfp",
      "display_name": "XFP (10GE)"
    },
    {
      "value": "10gbase-x-xenpak",
      "display_name": "XENPAK (10GE)"
    },
    {
      "value": "10gbase-x-x2",
      "display_name": "X2 (10GE)"
    },
    {
      "value": "25gbase-x-sfp28",
      "display_name": "SFP28 (25GE)"
    },
    {
      "value": "50gbase-x-sfp56",
      "display_name": "SFP56 (50GE)"
    },
    {
      "value": "40gbase-x-qsfpp",
      "display_name": "QSFP+ (40GE)"
    },
    {
      "value": "50gbase-x-sfp28",
      "display_name": "QSFP28 (50GE)"
    },
    {
      "value": "100gbase-x-cfp",
      "display_name": "CFP (100GE)"
    },
    {
      "value": "100gbase-x-cfp2",
      "display_name": "CFP2 (100GE)"
    },
    {
      "value": "200gbase-x-cfp2",
      "display_name": "CFP2 (200GE)"
    },
    {
      "value": "100gbase-x-cfp4",
      "display_name": "CFP4 (100GE)"
    },
    {
      "value": "100gbase-x-cpak",
      "display_name": "Cisco CPAK (100GE)"
    },
    {
      "value": "100gbase-x-qsfp28",
      "display_name": "QSFP28 (100GE)"
    },
    {
      "value": "200gbase-x-qsfp56",
      "display_name": "QSFP56 (200GE)"
    },
    {
      "value": "400gbase-x-qsfpdd",
      "display_name": "QSFP-DD (400GE)"
    },
    {
      "value": "400gbase-x-osfp",
      "display_name": "OSFP (400GE)"
    },
    {
      "value": "ieee802.11a",
      "display_name": "IEEE 802.11a"
    },
    {
      "value": "ieee802.11g",
      "display_name": "IEEE 802.11b/g"
    },
    {
      "value": "ieee802.11n",
      "display_name": "IEEE 802.11n"
    },
    {
      "value": "ieee802.11ac",
      "display_name": "IEEE 802.11ac"
    },
    {
      "value": "ieee802.11ad",
      "display_name": "IEEE 802.11ad"
    },
    {
      "value": "ieee802.11ax",
      "display_name": "IEEE 802.11ax"
    },
    {
      "value": "ieee802.15.1",
      "display_name": "IEEE 802.15.1 (Bluetooth)"
    },
    {
      "value": "gsm",
      "display_name": "GSM"
    },
    {
      "value": "cdma",
      "display_name": "CDMA"
    },
    {
      "value": "lte",
      "display_name": "LTE"
    },
    {
      "value": "sonet-oc3",
      "display_name": "OC-3/STM-1"
    },
    {
      "value": "sonet-oc12",
      "display_name": "OC-12/STM-4"
    },
    {
      "value": "sonet-oc48",
      "display_name": "OC-48/STM-16"
    },
    {
      "value": "sonet-oc192",
      "display_name": "OC-192/STM-64"
    },
    {
      "value": "sonet-oc768",
      "display_name": "OC-768/STM-256"
    },
    {
      "value": "sonet-oc1920",
      "display_name": "OC-1920/STM-640"
    },
    {
      "value": "sonet-oc3840",
      "display_name": "OC-3840/STM-1234"
    },
    {
      "value": "1gfc-sfp",
      "display_name": "SFP (1GFC)"
    },
    {
      "value": "2gfc-sfp",
      "display_name": "SFP (2GFC)"
    },
    {
      "value": "4gfc-sfp",
      "display_name": "SFP (4GFC)"
    },
    {
      "value": "8gfc-sfpp",
      "display_name": "SFP+ (8GFC)"
    },
    {
      "value": "16gfc-sfpp",
      "display_name": "SFP+ (16GFC)"
    },
    {
      "value": "32gfc-sfp28",
      "display_name": "SFP28 (32GFC)"
    },
    {
      "value": "64gfc-qsfpp",
      "display_name": "QSFP+ (64GFC)"
    },
    {
      "value": "128gfc-qsfp28",
      "display_name": "QSFP28 (128GFC)"
    },
    {
      "value": "infiniband-sdr",
      "display_name": "SDR (2 Gbps)"
    },
    {
      "value": "infiniband-ddr",
      "display_name": "DDR (4 Gbps)"
    },
    {
      "value": "infiniband-qdr",
      "display_name": "QDR (8 Gbps)"
    },
    {
      "value": "infiniband-fdr10",
      "display_name": "FDR10 (10 Gbps)"
    },
    {
      "value": "infiniband-fdr",
      "display_name": "FDR (13.5 Gbps)"
    },
    {
      "value": "infiniband-edr",
      "display_name": "EDR (25 Gbps)"
    },
    {
      "value": "infiniband-hdr",
      "display_name": "HDR (50 Gbps)"
    },
    {
      "value": "infiniband-ndr",
      "display_name": "NDR (100 Gbps)"
    },
    {
      "value": "infiniband-xdr",
      "display_name": "XDR (250 Gbps)"
    },
    {
      "value": "t1",
      "display_name": "T1 (1.544 Mbps)"
    },
    {
      "value": "e1",
      "display_name": "E1 (2.048 Mbps)"
    },
    {
      "value": "t3",
      "display_name": "T3 (45 Mbps)"
    },
    {
      "value": "e3",
      "display_name": "E3 (34 Mbps)"
    },
    {
      "value": "xdsl",
      "display_name": "xDSL"
    },
    {
      "value": "cisco-stackwise",
      "display_name": "Cisco StackWise"
    },
    {
      "value": "cisco-stackwise-plus",
      "display_name": "Cisco StackWise Plus"
    },
    {
      "value": "cisco-flexstack",
      "display_name": "Cisco FlexStack"
    },
    {
      "value": "cisco-flexstack-plus",
      "display_name": "Cisco FlexStack Plus"
    },
    {
      "value": "cisco-stackwise-80",
      "display_name": "Cisco StackWise-80"
    },
    {
      "value": "cisco-stackwise-160",
      "display_name": "Cisco StackWise-160"
    },
    {
      "value": "cisco-stackwise-320",
      "display_name": "Cisco StackWise-320"
    },
    {
      "value": "cisco-stackwise-480",
      "display_name": "Cisco StackWise-480"
    },
    {
      "value": "juniper-vcp",
      "display_name": "Juniper VCP"
    },
    {
      "value": "extreme-summitstack",
      "display_name": "Extreme SummitStack"
    },
    {
      "value": "extreme-summitstack-128",
      "display_name": "Extreme SummitStack-128"
    },
    {
      "value": "extreme-summitstack-256",
      "display_name": "Extreme SummitStack-256"
    },
    {
      "value": "extreme-summitstack-512",
      "display_name": "Extreme SummitStack-512"
    },
    {
      "value": "other",
      "display_name": "Other"
    }
  ]
}
```

</details>