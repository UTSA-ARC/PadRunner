from subprocess import check_output
from ipaddress import IPv4Address
from time import sleep

def check_connection(stop, s, lock, timeout: int): # Watchdog runner function
    while not stop.is_set(): # Until Stopped
        with lock: # Thread Lock to not jump values 
            if not check_ssh(): # If first check is false
                sleep(timeout) # Wait for some time
                if not check_ssh(): # If second check is false
                    s.append('abort') # Send an abort
                    break # Break Loop
            s.append('pass') # Else send a pass

def check_ssh():
    output = check_output(['w', '-i']).decode('utf-8')
    ssh_alive = output.split('\n')[2].split()[2]
    
    if 'fe80' in ssh_alive:
        return True
    
    if ':' in ssh_alive:
        ssh_alive = ssh_alive.split(':')[0]
    
    try:
        IPv4Address(ssh_alive)
    except ValueError:
        return False
    
    return True
