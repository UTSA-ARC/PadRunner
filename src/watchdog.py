from os import system

def check_connection(stop, q, lock, ip_address: str = '127.0.0.1', timeout: int = 60): # Watchdog runner function
    while not stop.is_set():
        with lock:
            response = system(f'ping -c 1 -w {timeout} {ip_address}')
            if response != 0:
                q.put('abort')
            else:
                q.put('pass')
