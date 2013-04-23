#!/usr/bin/env python

import time
import os
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

#
# List the servers.
#
#print "Here are the servers listed: "
#for server in cs.servers.list():
#	print server.name,server.status

print "Here are the servers: "
for server in cs.servers.list():
	wait = 1
	while wait == 1:
		server = cs.servers.get(server.id)
		if server.status == 'BUILD':
			print server.name, "is still building"
			print "Sleeping for 150 seconds"
			time.sleep(150)
		elif server.status == 'ACTIVE':
			print server.name, " network is", server.networks
			wait = 0
		else:
			print server.name, "is", server.status
			wait = 0
