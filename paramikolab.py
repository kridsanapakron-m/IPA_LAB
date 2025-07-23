import time
import paramiko
import os
from dotenv import load_dotenv
load_dotenv()
USERNAME = os.getenv("SSH_USERNAME")
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
DEVICE_IP = os.getenv("DEVICE_IP").split(",")
key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
for i in DEVICE_IP:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=i, username=USERNAME, pkey=key)
    stdin, stdout, stderr = client.exec_command("show running-config")
    output = stdout.read().decode()
    if "hostname R0" in output:
        print(output)
    client.close()
