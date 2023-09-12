import pigpio # GPIO access
import threading as th # To run the console
from time import sleep # For delays
from os import _exit

from config import * # Import config, commands and Any type
from watchdog import wd_runner # Check connection

class RepeatTimer(th.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def exit_message(pi: pigpio.pi, stop_event: th.Event = Any, watchdog_thread: th.Thread = Any, hard_abort: bool = False, before_cmd: bool = False,): # Exit program
    if Enable_Watchdog:
        stop_event.set()
        watchdog_thread.join()

    if not hard_abort and not before_cmd:
        Default_Pins( pi, PINS )

    pi.stop()
    print(SECTION_SEP)
    print('Byee!!')
    sleep(1)
    _exit(0)

def print_confirmation(pi: pigpio.pi): # Prints confirmation of settings
    print('Are these values correct?\n')

    print(f' -  Watchdog Enable: {Enable_Watchdog}')
    if Enable_Watchdog:
        print(f'        Watchdog Check Interval: {Watchdog_Check_Interval} seconds')
        print(f'        Watchdog Timeout: {Watchdog_Timout_Delay} seconds')

        print()

        print(f'  - GOX Enabled: {Enable_Gox}')
    if Enable_Gox:
        print(f'        GOX Open Delay (After Ignition): {GOX_Open_Delay} seconds\n')
        print(f'  - Pins Close Delay (After GOX Opens): {Pins_Close_Delay} seconds')
    else:
        print()
        print(f'  - Pins Close Delay (After Ignition): {Pins_Close_Delay} seconds')

    confirm_config = input('\n[Y/n]: ')

    if confirm_config == 'n':
        print('Please edit `src/config.py`')
        print(SECTION_SEP)
        exit_message(pi, before_cmd=True)

    print(SECTION_SEP)

def start(): # Program Starter
    clear()
    print(MOTD)

    print('Setting up RPI board...\n')
    pi = pigpio.pi() # Set rpi board

    for pin in PINS.values(): # Iterate through relay pins and make each an output
        pi.set_mode(pin, pigpio.OUTPUT)

    print('All Set!')
    print(SECTION_SEP)
    
    print_confirmation(pi) # Print settings confirmation

    stop_event: th.Event = th.Event() # Stop Event handler
    watchdog_stack: list = []
    watchdog_lock: th.Lock = th.Lock()
    watchdog_thread = th.Thread(target=wd_runner, args=(stop_event, watchdog_stack, watchdog_lock, Watchdog_Timout_Delay)) # Instantiate watchdog thread

    if Enable_Watchdog: # If watchdog is enabled
        watchdog_thread.start()
        print("Started Watchdog Timer...")

    print(SECTION_SEP)
    Default_Pins( pi, PINS )
    print(SECTION_SEP)
    print('Launching Console...')
    sleep(1)
    clear()
    print(MOTD)
    
    loop(pi, stop_event, watchdog_stack, watchdog_thread) # Start Main Loop

def check_wd(s: list, pi: pigpio.pi, stop_event: th.Event, watchdog_thread: th.Thread) -> None: # Check watchdog thread for abort
    got = ''
    if s.__len__() != 0 : got = s.pop()
    if got == 'abort':
        abort( pi, PINS )
        Default_Pins( pi, PINS )
        print('-->!!ABORTED!!\n')
        system('touch ~/PICode/ABORTED')
        exit_message(pi, stop_event, watchdog_thread, hard_abort=True)

def get_user_cmd(pi: pigpio.pi, watchdog_stack: list, stop_event: th.Event, watchdog_thread: th.Thread) -> str:
    rt = RepeatTimer(Watchdog_Check_Interval, check_wd, (watchdog_stack, pi, stop_event, watchdog_thread))
    rt.start()
    cmd: str = input('> ').lower()
    rt.cancel()
    return cmd

def check_special_cases(cmd) -> bool:
    if cmd in {'quit', 'q', 'exit'}: # If quit/q
        return False

    if cmd in {'?', 'help'}: # If help/?
        list_commands(COMMANDS.keys())

    if cmd.__contains__('gox') and not Enable_Gox:
        print('\n--> You do not have GOX enabled, please close the program and edit `src/config.py` to enable it\n')

    if not Get_State('ArmingTrigger') and cmd in {'open gox valve', 'start ignition', 'auto ignition'}: # If not armed
        print('\n--> IGNITION IS NOT ARMED\n')
        
    return True

def get_cmds(cmd) -> Any: # Get commands
    return COMMANDS.get(cmd, unknown_command) # Default to unknown

def auto_ignition_sequence(pi: pigpio.pi): # Auto Ignition Sequence
    ignition( pi, PINS )
    if Enable_Gox:
        print(f'Wating for {GOX_Open_Delay} seconds to open GOX...')
        sleep( GOX_Open_Delay )
        open_gox( pi, PINS )
    print(f'Waiting for {Pins_Close_Delay} seconds to close pins...')
    sleep( Pins_Close_Delay )
    print(SECTION_SEP)
    Default_Pins( pi, PINS )
    print(SECTION_SEP)
    print('--> Auto Ignition Sequence Completed\n')

def abort_sequence(cmd: str, pi: pigpio.pi, stop_event: th.Event, watchdog_thread: th.Thread): # Abort Sequence
    Default_Pins( pi, PINS )
    print('-->!!ABORTED!!\n')

    if not cmd.__contains__('soft'): # If NOT 'Soft Abort' Sequence
        system('touch ~/PICode/ABORTED')
        exit_message(pi, stop_event, watchdog_thread, hard_abort=True)

def loop( pi: pigpio.pi, stop_event: th.Event, watchdog_stack: list, watchdog_thread: th.Thread) -> None: # Main loop
    try:
        while not stop_event.is_set(): # Main Loop

            cmd: str = get_user_cmd(pi, watchdog_stack, stop_event, watchdog_thread) # Get command from user

            if not check_special_cases(cmd): # If special case quits
                break # Break loop

            action: Any = get_cmds(cmd) # Get command list

            action( pi, PINS ) # Run user's command

            if action == clear: # if command 'clear', Clear with motd
                print(MOTD)

            if cmd == 'auto ignition': # Auto Ignition Sequence
                auto_ignition_sequence(pi) # Auto Ignition

            if cmd.__contains__('abort'): # All Abort Sequences
                abort_sequence(cmd, pi, stop_event, watchdog_thread) # Abort
                break # Break loop

    except Exception:
        sleep(0)
    exit_message(pi, stop_event, watchdog_thread)
    
start() # Start Program
