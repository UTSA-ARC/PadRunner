import RPi.GPIO as gpio # GPIO access
import threading # To run the console
import queue # To run the console
from time import sleep # For delays

from config import * # Import config, commands and Any type

gpio.setmode(gpio.BOARD) # Set rpi board

for pin in PINS.values(): # Iterate through relay pins and make each an output
    gpio.setup(pin, gpio.OUT)

cmd_actions: dict[str, Any] = COMMANDS
cmd_queue: queue.Queue = queue.Queue()
stdout_lock: threading.Lock = threading.Lock()

input_thread = threading.Thread(target=console, args=(cmd_queue, stdout_lock)) # Instantiate input thread
print('Press Enter for Input Mode\n')
input_thread.start()

while 1: # Main Loop

    cmd = cmd_queue.get() # Get command from console
    if cmd == 'quit' or cmd == 'q': # If quit/q
        break

    if cmd == '?' or cmd == 'help': # If help/?
        action: Any = cmd_actions.get(cmd, unknown_command)
        action( stdout_lock, cmd_actions.keys() )
        print('\n------------')
        print('Press Enter for Input Mode')
        print('------------\n')
        continue

    action: Any = cmd_actions.get(cmd, unknown_command) # Default operation
    action(stdout_lock, PINS)

    if cmd == 'start gox' and AutoIgniterOpen: # For Auto Ignition
        sleep( IgniteDelay ) # Delay from GOX opening
        cmd = 'ignite'
        action = cmd_actions.get(cmd, unknown_command)
        action(stdout_lock, PINS)

    if cmd == 'ignite' and AutoGOXClose: # For Auto GOX closing
        sleep( GOXCloseDelay ) # Delay from Ignition
        cmd = 'stop gox'
        action = cmd_actions.get(cmd, unknown_command)
        action(stdout_lock, PINS)

    if cmd == 'stop gox' and AutoIgniterClose: # For Auto Ignition closing
        cmd = 'stop ignition'
        action = cmd_actions.get(cmd, unknown_command)
        action(stdout_lock, PINS)

    print('\n------------')
    print('Press Enter for Input Mode')
    print('------------\n')
