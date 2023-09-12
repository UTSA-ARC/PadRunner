from subprocess import getoutput
from ipaddress import IPv4Address
from time import sleep

def wd_runner(stop, s, lock, timeout: int): # Watchdog runner function
    while not stop.is_set(): # Until Stopped
        with lock: # Thread Lock to not jump values
            s.append(check_connection(timeout))

def check_connection(timeout):
    if not check_ssh(): # If first check is false
        sleep(timeout) # Wait for some time
        if not check_ssh(): # If second check is false
            return 'abort' # Send an abort
    return 'pass' # Else send a pass

def check_ssh(): # Check SSH connection
    ssh_alive = getoutput('w -i | awk \'NR==3{print $3}\'')

    if 'fe80' in ssh_alive:
        return True

    if ':' in ssh_alive:
        ssh_alive = ssh_alive.split(':')[0]

    try:
        IPv4Address(ssh_alive)
    except ValueError:
        return False

    return True
