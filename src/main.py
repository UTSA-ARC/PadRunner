import pigpio # GPIO access
import threading # To run the console
import queue # To run the console
from time import sleep # For delays
from os import _exit

from config import * # Import config, commands and Any type
from watchdog import check_connection # Check connection

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def exit_message():
    print('\nByee!!')
    if enable_watchdog:
        stop_event.set()
        watchdog_thread.join()
    pi.stop()
    _exit(0)

def check_wd(q):
    if q.get() == 'abort':
        Default_Pins( pi, PINS )
        print('-->!!ABORTED!!\n')
        exit_message()

print(motd)

print('Setting up RPI board...\n')
pi = pigpio.pi() # Set rpi board

for pin in PINS.values(): # Iterate through relay pins and make each an output
    pi.set_mode(pin, pigpio.OUTPUT)
    
print('All Set!\n')

if enable_watchdog and host_ip_address == '':
    host_ip_address: str = input('Enter your host ip Address/hostname: ') # Gets host ip address if not set
    
print('\nAre these values correct?\n')

print(f'Watchdog Enable: {enable_watchdog}')
if enable_watchdog: 
    print(f'Host ip address/hostname: {host_ip_address}')
    print(f'Watchdog Timeout: {watchdog_timout_delay} seconds')
print(f'Ignition Delay (after GOX open): {IgnitionDelay} seconds')
print(f'GOX Close Delay: {GOXCloseDelay} seconds')
    
confirm_config = input('\n[Y/n]: ')

if confirm_config == 'n':
    print('Please edit `config.py`')
    exit_message()

stop_event: threading.Event = threading.Event() # Stop Event handler
watchdog_queue: queue.Queue = queue.Queue()
watchdog_lock: threading.Lock = threading.Lock()
watchdog_thread = threading.Thread(target=check_connection, args=(stop_event, watchdog_queue, watchdog_lock, host_ip_address, watchdog_timout_delay)) # Instantiate watchdog thread

if enable_watchdog:
    watchdog_thread.start()
    print("Started Watchdog Timer...\n")

Default_Pins( pi, PINS )

try:
    while not stop_event.is_set(): # Main Loop
        
        rt = RepeatTimer(watchdog_check_interval, check_wd, (watchdog_queue,))
        rt.start()
        
        cmd: str = input('> ').lower()
            
        if cmd in ['quit', 'q', 'exit']: # If quit/q
            break

        if cmd in ['?', 'help']: # If help/?
            list_commands(COMMANDS.keys())
            continue

        if not Get_State('ArmingTrigger') and ( cmd in ['open gox valve', 'start ignition', 'auto ignition'] ): # If not armed
            print('--> IGNITION IS NOT ARMED\n')
            continue

        action: Any = unknown_command # Default to unknown
        for com in list(COMMANDS.keys()):
            if com[0] == cmd:
                action: Any = COMMANDS.get(com) # If command exists in list
                break

        action( pi, PINS )

        if action == clear: # Clear with motd
            print(motd)
            
        if cmd == 'auto ignition': # Auto Ignition Sequence
            open_gox( pi, PINS )
            sleep( IgnitionDelay )
            ignition( pi, PINS )
            sleep( GOXCloseDelay )
            Default_Pins( pi, PINS )
            print('--> Auto Ignition Sequence Completed\n')

        if cmd.__contains__('abort'): # All Abort Sequences
            Default_Pins( pi, PINS )
            print('-->!!ABORTED!!\n')

            if not cmd.__contains__('soft'): # If NOT 'Soft Abort' Sequence
                system('touch ./ABORTED')
                break

except Exception:
    sleep(0)
exit_message()