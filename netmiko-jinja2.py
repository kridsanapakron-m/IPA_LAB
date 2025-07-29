import os
from dotenv import load_dotenv
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml
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
    privatekey = os.getenv("file_privatekey")
    template_dir = os.getenv("jinja2_template")
    data_dir = os.getenv("jinja2_data")
    devices = ["S1", "R1", "R2"]
    env = Environment(loader=FileSystemLoader(template_dir),trim_blocks=True,lstrip_blocks=True)
    for i in devices:
        ip = os.getenv(f"{i}_ip")
        template = env.get_template(f'{i}_template.txt')
        with open(f'{data_dir}/{i}_data.yml') as f:
            data = yaml.safe_load(f)
        commands = template.render(data).split("\n")
        #print(commands)
        lab_netmiko(ip, username, privatekey, commands)
main()