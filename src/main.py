import pigpio # GPIO access
import threading # To run the console
from time import sleep # For delays
from os import _exit
from subprocess import getoutput

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

def check_wd(s: list):
    got = ''
    if s.__len__() != 0 : got = s.pop()
    if got == 'abort':
        Default_Pins( pi, PINS )
        print('-->!!ABORTED!!\n')
        system('touch ./ABORTED')
        exit_message()

print(motd)

print('Setting up RPI board...\n')
pi = pigpio.pi() # Set rpi board

for pin in PINS.values(): # Iterate through relay pins and make each an output
    pi.set_mode(pin, pigpio.OUTPUT)
    
print('All Set!\n')
    
print('\nAre these values correct?\n')

print(f'Watchdog Enable: {enable_watchdog}')
if enable_watchdog:
    print(f'Watchdog Check Interval: {watchdog_check_interval} seconds')
    print(f'Watchdog Timeout: {watchdog_timout_delay} seconds\n')
print(f'Ignition Delay (After GOX Opens): {IgnitionDelay} seconds')
print(f'Pins Close Delay (After Ignition): {PinsCloseDelay} seconds')
    
confirm_config = input('\n[Y/n]: ')

if confirm_config == 'n':
    print('Please edit `config.py`')
    exit_message()

stop_event: threading.Event = threading.Event() # Stop Event handler
watchdog_stack: list = []
watchdog_lock: threading.Lock = threading.Lock()
watchdog_thread = threading.Thread(target=check_connection, args=(stop_event, watchdog_stack, watchdog_lock, watchdog_timout_delay)) # Instantiate watchdog thread

if enable_watchdog:
    watchdog_thread.start()
    print("Started Watchdog Timer...\n")

Default_Pins( pi, PINS )

try:
    while not stop_event.is_set(): # Main Loop
        
        rt = RepeatTimer(watchdog_check_interval, check_wd, (watchdog_stack,))
        rt.start()
        
        cmd: str = input('> ').lower()
        rt.cancel()
            
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
            print(f'Wating for {IgnitionDelay} seconds to ignite...')
            sleep( IgnitionDelay )
            ignition( pi, PINS )
            print(f'Waiting for {PinsCloseDelay} seconds to close pins')
            sleep( PinsCloseDelay )
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