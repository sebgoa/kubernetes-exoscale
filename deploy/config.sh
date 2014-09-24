#!/bin/bash

git clone https://github.com/runseb/kubernetes-exoscale.git
cd kubernetes-exoscale/units
find .

ETCD_IP=`fleetctl list-machine | grep etcd | awk {'print $2'} | tail -n 1

for f in `ls`;
do
sed -i 's/<ip>/$ETCD_IP/g' $f
fleetctl start $f
done

API_IP=`fleetctl list-units | grep apiserver | awk {'print $2'}

echo API_IP

wget http://storage.googleapis.com/kubernetes/kubecfg
chmod +x ./kubecfg
