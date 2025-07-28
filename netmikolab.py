import os
from dotenv import load_dotenv
from netmiko import ConnectHandler
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
                print(output)
    except Exception as e:
        return print("command error")

def main():
    load_dotenv()
    username = os.getenv("ssh_username")
    privatekey = "./user"
    devices = ["S1", "R1", "R2"]

    for i in devices:
        ip = os.getenv(f"{i}_ip")
        commands = os.getenv(f"{i}_command").split(", ")
        lab_netmiko(ip, username, privatekey, commands)
main()