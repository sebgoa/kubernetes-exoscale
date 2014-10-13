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

#This is a coreos template with a 10GB disk
image=getimage('d2857804-034c-4973-8944-fb1639eafca5')
#This is a micro instance
size=getsize('71004023-bb72-4a97-b1e9-bc66dfce9470')

#Reads cloud config file
userdata = "\n".join(open('./nodes/etcd.yml').readlines())

# Replace the name of the key with what you created and make sure you created an etcd security group
name = 'etcd'
for i in range(5):
    name = name + '-' + str(i)
    conn.create_node(image=image,size=size,ex_keyname='exoscale',ex_security_groups=['etcd'],ex_display_name=name, ex_userdata=userdata)
