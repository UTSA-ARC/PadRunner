import pigpio # GPIO access
import threading # To run the console
import queue # To run the console
from time import sleep # For delays

from config import * # Import config, commands and Any type
from watchdog import check_connection # Check connection

def exit_message():
    print('\nByee!!')
    stop_event.set()
    watchdog_thread.join()
    pi.stop()
    exit()

print(motd)

print('Setting up RPI board...\n')
pi = pigpio.pi() # Set rpi board

for pin in PINS.values(): # Iterate through relay pins and make each an output
    pi.set_mode(pin, pigpio.OUTPUT)
    
print('All Set!\n')

if host_ip_address == '':
    host_ip_address: str = input('Enter your host IP Address: ') # Gets host ip address if not set
    
print('\nAre these values correct?\n')
print(f'Watchdog Timeout: {watchdog_timout_delay} seconds')
print(f'Ignition Delay (after GOX open): {IgnitionDelay} seconds')
print(f'GOX Close Delay: {GOXCloseDelay} seconds')
    
confirm_config = input('\n[Y/n]: ')

if confirm_config == 'n':
    print('Please edit `config.py`')
    exit()

stop_event: threading.Event = threading.Event() # Stop Event handler

watchdog_queue: queue.Queue = queue.Queue()
watchdog_lock: threading.Lock = threading.Lock()
watchdog_thread = threading.Thread(target=check_connection, args=(stop_event, watchdog_queue, watchdog_lock, host_ip_address, watchdog_timout_delay)) # Instantiate watchdog thread
watchdog_thread.start()
print("Started Watchdog Timer...\n")

Default_Pins( pi, PINS )

try:
    while 1: # Main Loop

        cmd = 'abort' if watchdog_queue.get() == 'abort' else console() # If connectivity is lost, exit
        if cmd in ['quit', 'q', 'exit']: # If quit/q
            exit_message()
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
            close_gox( pi, PINS )
            stop_ignition( pi, PINS )
            close_bottle_valve( pi, PINS )
            close_tank_valve( pi, PINS )
            open_vent( pi, PINS )
            print('--> Auto Ignition Sequence Completed\n')

        if cmd.__contains__('abort'): # All Abort Sequences
            close_bottle_valve( pi, PINS )
            close_tank_valve( pi, PINS )
            close_gox( pi, PINS )
            stop_ignition( pi, PINS )
            open_vent( pi, PINS )
            disarm_ignition( pi, PINS )
            print('-->!!ABORTED!!\n')

            if not cmd.__contains__('soft'): # If NOT 'Soft Abort' Sequence
                system('touch ./ABORTED')
                exit_message()
                break

except Exception:
    exit_message()
