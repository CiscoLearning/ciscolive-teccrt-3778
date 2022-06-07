# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)

        # ACL_NAME, ACTION, DESCIPTION, DESTINATION_ADDRESS, DESTIONATION_PORT, DEVICE_NAME, PROTOCOL, SOURCE_ADDRESS, SOURCE_PORT
        vars.add("ACL_NAME", service.name)

        # Loop over rules 
        for i, rule in enumerate(service.rule): 
            vars.add("DESCRIPTION", f"Rule {i} in ACL Service {service.name}. Description {rule.description}")
            vars.add("ACTION", rule.action)
            vars.add("PROTOCOL", rule.protocol)
            vars.add("SOURCE_ADDRESS", "any")
            vars.add("SOURCE_PORT", "")
            vars.add("DESTINATION_ADDRESS", "192.168.10.0 0.0.0.255")
            vars.add("DESTINATION_PORT", "eq 80")
            vars.add("LOG", rule.log)

            # loop over devices to apply 
            for device in service.device: 
                vars.add("DEVICE_NAME", device)
                template.apply('acl-service-template', vars)


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('acl-service-servicepoint', ServiceCallbacks)

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
