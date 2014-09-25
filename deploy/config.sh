#!/bin/bash

find .

ETCD_IP=`fleetctl list-machines | grep etcd | awk {'print $2'} | tail -n 1`

for f in `ls`;
do
echo $ETCD_IP | sed -i "s/<ip>/$ETCD_IP/g" $f
fleetctl start $f
done

API_IP=`fleetctl list-units | grep apiserver | awk {'print $2'}`
IFS='/' read -ra IP <<< "$API_IP"
echo ${IP[1]}

wget -O ../kubecfg http://storage.googleapis.com/kubernetes/kubecfg
chmod +x ../kubecfg
export KUBERNETES_MASTER=http://${IP[1]}:8080

../kubecfg list /minions

echo "Don't forget to set KUBERNETES_MASTER to ${IP[1]}"
