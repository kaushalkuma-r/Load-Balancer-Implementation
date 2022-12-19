#!/bin/bash
sudo virt-clone  --original newdemo --name ${vm_name} --file /media/kaushal/DATA/${vm_name}.qcow2
sudo grep pid /var/run/libvirt/qemu/${vm_name}.xml  >> name.txt
echo ${vm_name} >> vm_name.txt

