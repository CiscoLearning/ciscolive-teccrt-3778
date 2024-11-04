# Deploy an ACI infra trough IaC

This case study explores using Ansible in an IaC environment and focuses on loop.

## Documentation for the Question

We are moving away from manually provisioning our ACI fabrics and are starting our IaC journey trough ACI Ansible. You are tasked to complete our ansible playbook so that it correctly deploys an ACI fabric.

On completion the playbook must do the following:

* Create the required
  * Tenants
  * Application Profiles
  * EPGs
* Authenticate using key based authentication (use provided candidate.key)
* For each ACI object created, attach a description in the format “Created by Ansible <date>”, where <date> is the output of the Linux command ‘date’

Make sure to use all variables from the supplied inventory.yaml inventory file and make sure your code is re-usable and easily shareable with other members of the team.

Upon completion, you should validate the playbook by running it and confirming the topology is correctly created in ACI.

## Solution

The solution is provided in the `code_solution` directory.
