import RPi.GPIO as gpio # GPIO access
import threading # To run the console
import queue # To run the console
from time import sleep # For delays

from config import * # Import config, commands and Any type
from watchdog import check_connection # Check connection

gpio.setmode(gpio.BCM) # Set rpi board

for pin in PINS.values(): # Iterate through relay pins and make each an output
    gpio.setup(pin, gpio.OUT)

if host_ip_address is None:
    host_ip_address: str = input('Enter your host IP Address: ') # Gets host ip address if not set
watchdog_queue: queue.Queue = queue.Queue()
watchdog_thread = threading.Thread(target=check_connection, args=(watchdog_queue, host_ip_address, watchdog_timout_delay)) # Instantiate watchdog thread
watchdog_thread.start()
print("Started Watchdog Timer...\n")

cmd_actions: dict[str, Any] = FUNCTION_COMMANDS
cmd_queue: queue.Queue = queue.Queue()
stdout_lock: threading.Lock = threading.Lock()
input_thread = threading.Thread(target=console, args=(cmd_queue, stdout_lock)) # Instantiate input thread

enter_txt: str = '\n------------\nPress Enter for Input Mode\n------------\n'

print(enter_txt)
input_thread.start()


while 1: # Main Loop

    cmd = cmd_queue.get() # Get command from console
    if watchdog_queue.get() is not None: # If connectivity is lost, abort
        cmd = 'abort'
        
    if cmd in ['quit', 'q']: # If quit/q
        gpio.cleanup()
        break

    if cmd in ['?', 'help']: # If help/?
        list_commands(stdout_lock, cmd_actions.keys())
        print(enter_txt)
        continue

    if not armed and ( cmd in ['open gox valve', 'ignition', 'auto ignition'] ):
        print('--> IGNITION IS NOT ARMED\n')
        print(enter_txt)
        continue
    
    action: Any = cmd_actions.get(cmd, unknown_command) # Default operation
    action(stdout_lock, PINS)
    
    if cmd == 'auto ignition':
        open_gox(stdout_lock, PINS)
        sleep( IgniteDelay )
        ignition(stdout_lock, PINS)
        sleep( GOXCloseDelay )
        close_gox(stdout_lock, PINS)
        stop_ignition(stdout_lock, PINS)
        print('--> Auto Ignition Sequence Completed\n')
        
    if cmd == 'abort':
        close_gox(stdout_lock, PINS)
        stop_ignition(stdout_lock, PINS)
        open_vent(stdout_lock, PINS)
        print('-->!!ABORTED!!\n')

    print(enter_txt)
