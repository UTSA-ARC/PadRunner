from time import sleep
import pyping

def check_connection(q, ip_address: str = '127.0.0.1', timeout: int = 60):
    while 1:
        response = pyping.ping(ip_address, timeout)
        if response.ret_code != 0:
            q.put('abort')
