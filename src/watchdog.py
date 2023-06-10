from os import system

def check_connection(stop, q, lock, ip_address: str, timeout: int): # Watchdog runner function
    while not stop.is_set():
        with lock:
            response = system(f'ping -c 1 -w {timeout} {ip_address} > /dev/null 2>&1')
            if response != 0:
                q.put('abort')
            else:
                q.put('pass')
