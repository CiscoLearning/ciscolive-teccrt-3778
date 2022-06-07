# Creating a service to manage Access Lists
A network service is being created to manage access control lists on CPE routers at branch locations using NSO. CRUD requests of this service will come from multiple systems including web applications, service catalogs, and orchestrators.

Given the below desired final configuration for an example service instance, you are to: 

* Create the XML configuration template that will be used by the service to render final device configurations 
* Update the YANG model for the service to limit the values used for ports to integers between 0 to 65535

> Note: The NetBox server is available at address http://0.0.0.0:8000 when running on CWS using the setup instructions. 
>  Credentials: 
>    * Username: `expert`
>    * Password: `1234QWer!`


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
