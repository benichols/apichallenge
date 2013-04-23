#!/usr/bin/env python

import time
import os
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

#
# List the servers and delete them.
#
print "Deleting each server"
for server in cs.servers.list():
	print server.name,server.id,server.status
	server.delete()
