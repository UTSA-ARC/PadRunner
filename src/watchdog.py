from time import sleep
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def check_connection(q, ip_address: str = '127.0.0.1', timeout: int = 60):
    while 1:
        response = ping(ip_address, timeout)
        if response != True:
            q.put('abort')

def ping(host, timeout):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    param += f'-W {timeout}'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0
