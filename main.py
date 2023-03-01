#!/usr/local/bin/python3.9
# This is a Python Start Menu that calls other .py files to do work.

# import subprocess
import runpy

menu_prompt = ('\n    1. Change Password\n'
               '    2. Add User Account\n'
               '    3. Delete User\n'
               '    Q. Quit\n\n'
               '    >>>  ')

while True:
    command = input(menu_prompt).lower().strip()
    if command == '1':
        print('    Changing password\n')
        runpy.run_path(path_name='cisco_userpass.py')
        # subprocess.call('cisco_userpass.py', shell=True)  # replaced with runpy which works better
    elif command == '2':
        print('    Add a User\n')
        runpy.run_path(path_name='cisco_usermod.py')
        # subprocess.call('cisco_usermod.py', shell=True)  # replaced with runpy which works better
    elif command == '3':
        print('    Delete a User\n')
        runpy.run_path(path_name='cisco_userdel.py')
        # subprocess.call('cisco_userdel.py', shell=True)  # replaced with runpy which works better
    elif command == 'q':
        break  # Exit
    else:
        print('    *** Unrecognized Entry ***')
