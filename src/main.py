import RPi.GPIO as gpio # GPIO access
import threading # To run the console
import queue # To run the console
from time import sleep # For delays

from config import * # Import config, commands and Any type
from watchdog import check_connection # Check connection

print(motd)

print('Setting up RPI board...\n')
gpio.setmode(gpio.BCM) # Set rpi board

for pin in PINS.values(): # Iterate through relay pins and make each an output
    gpio.setup(pin, gpio.OUT)
print('All Set!\n')

if host_ip_address == '':
    host_ip_address: str = input('Enter your host IP Address: ') # Gets host ip address if not set

stop_event: threading.Event = threading.Event()

watchdog_queue: queue.Queue = queue.Queue()
watchdog_lock: threading.Lock = threading.Lock()
watchdog_thread = threading.Thread(target=check_connection, args=(stop_event, watchdog_queue, watchdog_lock, host_ip_address, watchdog_timout_delay)) # Instantiate watchdog thread
watchdog_thread.start()
print("Started Watchdog Timer...\n")

Default_Pins( PINS )

try:
    while 1: # Main Loop

        cmd = console() # Get command from console
        if watchdog_queue.get() == 'abort': # If connectivity is lost, abort
            cmd = 'abort'
            
        if cmd in ['quit', 'q', 'exit']: # If quit/q
            stop_event.set()
            watchdog_thread.join()
            gpio.cleanup()
            break

        if cmd in ['?', 'help']: # If help/?
            list_commands(COMMANDS.keys())
            continue

        if not Get_State('ArmingTrigger') and ( cmd in ['open gox valve', 'start ignition', 'auto ignition'] ):
            print('--> IGNITION IS NOT ARMED\n')
            continue
        
        action: Any = unknown_command
        for com in list(COMMANDS.keys()):
            if com[0] == cmd:
                action: Any = COMMANDS.get(com)
                break
            
        action( PINS )
        
        if action == clear:
            print(motd)
            
        if cmd == 'auto ignition':
            open_gox(PINS)
            sleep( IgniteDelay )
            ignition(PINS)
            sleep( GOXCloseDelay )
            close_gox(PINS)
            stop_ignition(PINS)
            print('--> Auto Ignition Sequence Completed\n')
            
        if cmd.__contains__('abort'):
            close_bottle_valve(PINS)
            close_tank_valve(PINS)
            close_gox(PINS)
            stop_ignition(PINS)
            open_vent(PINS)
            disarm_ignition(PINS)
            print('-->!!ABORTED!!\n')
            
            if not cmd.__contains__('soft'):
                stop_event.set()
                watchdog_thread.join()
                gpio.cleanup()
                break
            
        
except KeyboardInterrupt:
    stop_event.set()
    watchdog_thread.join()
    gpio.cleanup()
