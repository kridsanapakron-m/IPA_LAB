import os
from dotenv import load_dotenv
from netmiko import ConnectHandler
load_dotenv()
# device_params = {
#         "device_type": "cisco_ios",
#         "ip": os.getenv("DEVICE_IP"),
#         "username": os.getenv("ssh_username"),
#         "password": os.getenv("password")
#         }
# command = {"sh ip int br"}
# with ConnectHandler(**device_params) as ssh:
#     result = ssh.send_config_set(command)
#     print(result)
command_s1 = {
    "vlan 101",
    "name ControlDataPlane",
    "no shut",
    "exit",
    "int range e0/1-2",
    "switch port mode access",
    "switch port access vlan 101",
    "no shut",
    "exit"
}
command_r1 = {
    "int Loopback0",
    "ip add 1.1.1.1 255.255.255.255",
    "no shut",
    "exit",
    "router ospf 10 vrf control-data",
    "router-id 1.1.1.1",
    "network 1.1.1.1 0.0.0.0 area 0",
    "network 172.31.8.16 0.0.0.15 area 0",
    "network 172.31.8.48 0.0.0.15 area 0",
    "exit"
    # "",
    # "",
    # "",
    # "",
    # ""
}
command_r2 = {
    "int Loopback0",
    "ip add 2.2.2.2 255.255.255.255",
    "no shut",
    "exit",
    "router ospf 10 vrf control-data",
    "router-id 2.2.2.2",
    "network 2.2.2.2 0.0.0.0 area 0",
    "network 172.31.8.16 0.0.0.15 area 0",
    "network 172.31.8.32 0.0.0.15 area 0",
    "exit"
}