import os
from dotenv import load_dotenv
from netmiko import ConnectHandler
import re
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
def isactive(result):
     print("Active Interfaces\n")
     for i in result.split("\n"):
        match = re.search('^(\\S+).*\\bup\\s+up\\b', i)
        if match:
            print(match.group(1))
def uptime(result, device):
    for i in result.split("\n"):
        match = re.search(f'^{device} uptime is .+', i)
        if match:
            return match.group(0)
def main():
    load_dotenv()
    username = os.getenv("ssh_username")
    privatekey = os.getenv("file_privatekey")
    devices = ["R1", "R2"]
    for i in devices:
        print(f"---{i}---\n")
        ip = os.getenv(f"{i}_ip")
        result = lab_netmiko(ip, username, privatekey, "do sh ip int br")
        isactive(result)
        result = lab_netmiko(ip, username, privatekey, "do sh version")
        print("Uptime\n" + uptime(result, i) + "\n")
main()