#!/usr/bin/env python

import time
import os
import pyrax

#
# Setup the number of servers to create.
#
num = ['1', '2', '3']
servers = []

#
# Read in the credentials.
#
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

#
# Find the Debian image.
#
debian = [img for img in cs.images.list()
	if "Squeeze" in img.name] [0]
print "Using the following image: ", debian, "(", debian.id, ")"

#
# Find the 512 flavor.
#
flavor = [flavor for flavor in cs.flavors.list()
	if flavor.ram == 512] [0]
print "Flavor is: ", flavor, "(", flavor.id, ")"

#
# Create the servers.
#
for i in num:
	name = 'test' + i
	server = cs.servers.create(name, debian.id, flavor.id)
	servers.append(server)

#
# Output the credentials and network for each server.
#
for server in servers:
	#
	# Use a while loop to wait until the server is active.
	#
	wait = 1
	while wait == 1:
		j = cs.servers.get(server.id)
		if j.status == "BUILD":
			print j.name, "is still building"
			time.sleep(180)
		elif j.status == "ACTIVE":
			print "Name: ", j.name
			print "Admin Password: ", server.adminPass
			print "Networks: ", j.networks
			wait = 0
