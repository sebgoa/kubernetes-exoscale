#!/usr/bin/env python

import sys
import os

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

apikey=os.getenv('EXOSCALE_API_KEY')
secretkey=os.getenv('EXOSCALE_SECRET_KEY')

Driver = get_driver(Provider.EXOSCALE)
conn=Driver(key=apikey,secret=secretkey)

#Convenience function
def getimage(id):
    return [i for i in conn.list_images() if i.id == id][0]
def getsize(id):
    return [i for i in conn.list_sizes() if i.id == id][0]

#This is a coreos template with a 10B disk
image=getimage('d2857804-034c-4973-8944-fb1639eafca5')
#This is a small instance
size=getsize('21624abb-764e-4def-81d7-9fc54b5957fb')

#Reads cloud config file
userdata = "\n".join(open('./nodes/knode.yml').readlines())

# Replace the name of the key with what you created and make sure you created an etcd security group
name = 'kube'
for i in range(5):
    name = name + '-' + str(i)
    conn.create_node(image=image,size=size,ex_keyname='exoscale',ex_security_groups=['kubernetes'],ex_display_name=name, ex_userdata=userdata)