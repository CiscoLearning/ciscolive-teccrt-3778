# SSL certificates

This case study explores using OpenSSL key generation and using the resulting certificate in an NGINX env.

## Documentation for the Question

In order to keep our data secure and to be able to validate ownership, our company is using it’s own CA. As our desktops have been configured to refuse any untrusted certificate, all desktops in our company have our Company Root CA installed to accomplish this. You are tasked to generate a new key/CSR and install an existing certificate into a NGINX web-proxy so our users can start using this service.

On completion of this task, you should meet the following requirements:

* The newly generated key/CSR should have the following parameters:
  * Use RSA algorithms with 1024 bits
  * The FQDN of the server will be ‘www.teccrt-3778.example.com’
  * Name as following:
    * Key file: www.teccrt-3778.example.com.key
    * CSR File: www.teccrt-3778.example.com.csr
* Correct our existing nginx.conf to correctly includes our existing certificate:
  * Use the files name demo.teccrt-3778.example.com.*
  * You are allowed to create new files for this task to make the existing nginx.conf work correctly with the provide key/certificate

Please note that the existing Certificate has been signed with an intermediate CA.

You can validate your NGINX configuration by running “nginx -c nginx.conf  -p $PWD”

## Solution

The solution is provided in the `code_solution` directory.
