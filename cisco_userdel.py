#!/usr/local/bin/python3.9
# Cisco Account Automation
# This is basic function that will log into a switch and remove a user.

import datetime
import os
# import re
import time
from getpass import getpass
import paramiko

print('\n    #### Caution Updating all IOS Devices type \'Cntr\' \'C\' to Exit ####\n\n')
sshUsername = input('    Enter Current Privileged User Name: ').strip()
sshPassword = getpass('    Enter Current Password: ').strip()
delUser = input('    Enter the User account to Delete: ').strip()


# noinspection PyPep8Naming
class ssh:
    shell = None
    client = None
    transport = None

    def __init__(self, ipaddr, user, passwd):
        print('  Connecting to host: ', str(ipaddr))
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(ipaddr, username=user, password=passwd, look_for_keys=False)
        self.transport = paramiko.Transport((ipaddr, 22))
        self.transport.connect(username=user, password=passwd)

    def close_connection(self):
        if self.client is not None:
            self.client.close()
            self.transport.close()

    def open_shell(self):
        self.shell = self.client.invoke_shell()

    def send_shell(self, command):
        if self.shell:
            self.shell.send(command + "\n")
        else:
            print('  Connection Failed.')


time_now = datetime.datetime.now().strftime('%H:%M:%S %m/%d/%Y')
# infilepath = os.path.expanduser('~/scripts/')  # UNIX Pathing
infilepath = os.path.expanduser('~\\scripts\\')  # Windows Pathing
devicelist = "test_devices.txt"  # Set devicelist default
# devicelist = "ios_devices.txt"  # Set devicelist default
input_file = open(infilepath + devicelist, "r")
print(f'\n    Using File {infilepath} {devicelist}\n')  # debug line verifying the device list
iplist = input_file.readlines()
input_file.close()
try:
    for ip in iplist:
        try:
            host = ip.strip()
            connection = ssh(host, sshUsername, sshPassword)
            connection.open_shell()
            time.sleep(1)
            connection.send_shell('conf term')  # Cmd1
            connection.send_shell(f'no username {delUser}')  # Cmd2
            time.sleep(1)
            connection.send_shell('\n')  # Cmd3 THIS IS NEEDED to handle the response for 6500's
            connection.send_shell('end')  # Cmd4
            connection.send_shell('write mem')  # Cmd5
            time.sleep(1)
            connection.send_shell('exit')  # Cmd6
            # time.sleep(1)  # Time delay does not appear to be needed, will remove after testing
            print(f'\n    >>> {delUser} removed from:  {host} \n')
            connection.close_connection()
        finally:
            pass
finally:
    print(f'\n    Devices Updated: {time_now}\n')
