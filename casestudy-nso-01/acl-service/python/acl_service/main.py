# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
from utils import ios_acl_port_map, acl_address
    

class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)

        vars.add("ACL_NAME", service.name)

        # Loop over rules 
        for i, rule in enumerate(service.rule): 
            self.log.info(f"Creating rule [{rule.name}]")
            ace_seq = (i+1)*10
            vars.add("LABEL_SEQ", ace_seq)
            vars.add("DESC_SEQ", ace_seq+1)
            vars.add("SEQ", ace_seq+2)
            vars.add("LABEL", f"Rule {rule.name} in ACL Service {service.name}")
            vars.add("DESCRIPTION", f"Description {rule.description}")
            vars.add("ACTION", rule.action)
            vars.add("PROTOCOL", rule.protocol)
            vars.add("SOURCE_ADDRESS", acl_address(rule.source.address))
            # TODO: determine source port 
            vars.add("SOURCE_PORT", "")
            vars.add("DESTINATION_ADDRESS", acl_address(rule.destination.address))
            # TODO: detemrine destination port based on service input 
            vars.add("DESTINATION_PORT", "eq 80")
            # TODO: determine how to identify if log is set or not 
            vars.add("LOG", rule.log)

            # loop over devices to apply 
            for device in service.device: 
                vars.add("DEVICE_NAME", device)
                self.log.info(f"vars: {vars}")
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
