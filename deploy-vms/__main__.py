import pulumi
from pulumi import Output
from pulumi_azure import core, compute, network

# Create an Azure Resource Group
resource_group = core.ResourceGroup('resource_group')

# subnet for vms
net = network.VirtualNetwork(
    "server-network",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    address_spaces=["10.0.0.0/16"],
    subnets=[{
        "name": "default",
        "address_prefix": "10.0.1.0/24",
    }])

subnet = network.Subnet(
    "server-subnet",
    resource_group_name=resource_group.name,
    virtual_network_name=net.name,
    address_prefixes=["10.0.2.0/24"],
    enforce_private_link_endpoint_network_policies="false")

# create example userdata
userdata = """#!/bin/bash
echo "Hello, World!" > hello
"""

# show off loop usage in pulumi
names = ["vm1", "vm2", "vm3"]
for name in names:
  # every vm needs its own public ip and interface
  
  public_ip = network.PublicIp(
    "{}-public-ip".format(name),
    resource_group_name=resource_group.name,
    location=resource_group.location,
    allocation_method="Dynamic")

  network_iface = network.NetworkInterface(
    "{}-nic".format(name),
    resource_group_name=resource_group.name,
    location=resource_group.location,
    ip_configurations=[{
        "name": "server-ip",
        "subnet_id": subnet.id,
        "private_ip_address_allocation": "Dynamic", # just grab any ip
        "public_ip_address_id": public_ip.id,
    }])

  # create vm itself
  vm = compute.VirtualMachine(
    "server-vm-{}".format(name),
    resource_group_name=resource_group.name,
    location=resource_group.location,
    network_interface_ids=[network_iface.id],
    vm_size="Standard_A0", # small vm
    delete_data_disks_on_termination=True,
    delete_os_disk_on_termination=True,
    os_profile={
        "computer_name": name, # set name
        "admin_username": "myUsername",
        "admin_password": "Abc1234!",
        "custom_data": userdata,
    },
    os_profile_linux_config={
        "disable_password_authentication": False,
    },
    storage_os_disk={
        "create_option": "FromImage",
        "name": "os-disk-{}".format(name),
    },
    storage_image_reference={
        "publisher": "canonical",
        "offer": "UbuntuServer",
        "sku": "18.04-LTS",
        "version": "latest",
    })

  # prepare API call
  combined_output = Output.all(vm.id, public_ip.name,public_ip.resource_group_name)

  # create vm and apply public ip
  public_ip_addr = combined_output.apply(
    lambda lst: network.get_public_ip(name=lst[1], resource_group_name=lst[2]))
  
  pulumi.export('public_ip', public_ip.ip_address)
