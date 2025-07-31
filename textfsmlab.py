from operator import ne
import os
import re
from dotenv import load_dotenv
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
load_dotenv()
username = os.getenv("ssh_username")
privatekey = os.getenv("file_privatekey")
template_dir = os.getenv("jinja2_template")
env = Environment(loader=FileSystemLoader(template_dir),trim_blocks=True,lstrip_blocks=True)
def lab_netmiko(ip, username, privatekey, commands):
    device_params = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "use_keys": True,
        "key_file": privatekey,
        "allow_agent": False,
        "disabled_algorithms": {
            "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]
        }
    }
    try:
        with ConnectHandler(**device_params) as ssh:
                output = ssh.send_config_set(commands)
                return output
    except Exception as e:
        return print("command error")
def createcommand(inttype, intnum, neighborporttype, neighborport, neighborname, ):
    data = {
                    "inttype": inttype,
                    "intnum": intnum,
                    "neighborporttype": neighborporttype,
                    "neighborport": neighborport,
                    "neighborname": neighborname
                }
    template = env.get_template('Description.txt')
    commands = template.render(data).split("\n")
    return commands
def getneighbor(ip):
    commands = "do sh cdp neighbor"
    output = lab_netmiko(ip, username, privatekey, commands)
    return output
def createcommandfromneighbor(ip):
    neighbor = getneighbor(ip)
    pattern = "^(\\S+)\\s+(Gig)\\s+(\\S+)\\s+((?:\\d+\\s+)+[A-Z\\s]+)\\s+(Gig)\\s+(\\S+)"
    list_command = []
    for j in neighbor.split("\n"):
            match = re.search(pattern, j.strip())
            if match:
                iii = match.groups()
                commands = createcommand(iii[1], iii[2], iii[4][0], iii[5], iii[0].split('.')[0])
                list_command.extend(commands)
    return list_command
def createcommandblindport(devices):
    if devices == "R0":
        commands = createcommand("Gig", "0/1", "WAN\n", "", "")
        return commands
    elif devices == "R1":
        commands = createcommand("Gig", "0/2", "Pc\n", "", "")
        return commands
    elif devices == "R2":
        commands = createcommand("Gig", "0/3", "WAN\n", "", "") 
        return commands  
    elif devices == "S1":
        commands = createcommand("Gig", "0/2", "Pc\n", "", "")  
        return commands
    return []
def main():
    devices = ["R0","R1", "R2", "S0", "S1"]
    for i in devices:
        full_command = []
        ip = os.getenv(f"{i}_ip")
        full_command.extend(createcommandfromneighbor(ip))
        full_command.extend(createcommandblindport(i))
        lab_netmiko(ip, username, privatekey, full_command)
main()