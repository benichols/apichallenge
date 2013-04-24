#!/usr/bin/env python

import time
import os
import pyrax

#
# Read in the credentials.
#
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

#
# Find the 512 flavor.
#
flavor = [flavor for flavor in cs.flavors.list() if flavor.ram == 512] [0]

#
# List the servers.
#
for server in cs.servers.list():
	if server.name == 'test1':
		#
		# Take an image of test1.
		#
		image = cs.servers.create_image(server.id, "Debian image")
		print "'Debian image' is being created (%s)" % (image)

#
# Check that the image ACTIVE.
#
wait = 1
while wait == 1:
        all_images = cs.images.list()
        i = [img for img in all_images if hasattr(img,"server")]
        for j in i:
		#
		# Check if the image is SAVING.
		#
		if j.status == 'SAVING':
                        #
                        # If it is saving, so sleep for 60 seconds.
                        #
			print "Image (%s), is %s" % (j.name,j.status)
			time.sleep(60)
		elif j.status == 'ACTIVE':
                        #
                        # Once it is active, output the name and id.
                        #
			print "Image (%s), id (%s)" % (j.name,j.id)
			wait = 0

#
# Create test2 as an image of test1.
#
print "Creating test2"
server = cs.servers.create('test2', image, flavor.id)
wait = 1
while wait == 1:
        i = cs.servers.get(server.id)
        if i.status == 'BUILD':
                #
                # Wait until the image is done building.
                #
                print "%s is building" % i.name
                time.sleep(180)
        elif i.status == 'ACTIVE':
                #
                # Once the server is done building, output the name, 
                # password and ip information.
                #
                print "Name: %s" % i.name
                print "Admin Password: %s" % server.adminPass
                print "Networks: %s" % i.networks
                wait = 0
