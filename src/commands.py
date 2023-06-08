import RPi.GPIO as gpio # GPIO Access
from typing import Union

states: dict[str, bool] = { # For pin states
    
    'BottleValve': False,
    'TankValve': False,
    'VentValve': False,
    'GOXValve': False,
    'ArmingTrigger': False,
    'IgnitionTrigger': False
    
    }

armed: bool = False
quit_program: bool = False

def Get_State( key: str ) -> Union[ bool, None ]: return states[key] # Get pin state

def Default_Pins() -> None:
    gpio.output( pins['BottleValvePin'], False )
    gpio.output( pins['TankValvePin'], False )
    gpio.output( pins['GOXValvePin'], False )
    gpio.output( pins['VentValvePin'], False )
    print("Defaulted Pins\n")

def console(q, lock) -> None: # Console Thread
    while quit_program != True: # Thread inf loop
        with lock:
            input()
            cmd = input('> ')
            cmd = cmd.lower() # Lowercase it all

        q.put(cmd)

def exit_program(lock, pins) -> None: # Exit Program
    with lock:
        quit_program = True
        print('--> Exiting program...\n')

def list_commands(lock, commands) -> None: # List out all commands
    with lock:
        print('--> Here is a list of all the registered commands')
        print( 'q' + '\n' )
        print( 'quit' + '\n' )
        for key in commands:
            print( key + '\n' )

def open_bottle_valve(lock, pins) -> None: # Trigger to Open Bottle Relay
    with lock:
        print('--> Opening Bottle Valve...\n')
        gpio.output( pins['BottleValvePin'], True )
        states['BottleValve'] = True
        print('--> Bottle Valve Opened\n')

def close_bottle_valve(lock, pins) -> None: # Trigger to Open Bottle Relay
    with lock:
        print('--> Stopping Bottle valve...\n')
        gpio.output( pins['BottleValvePin'], False )
        states['BottleValve'] = False
        print('--> Bottle Valve Closed\n')

def open_tank_valve(lock, pins) -> None: # Trigger Open Tank Relay
    with lock:
        print('--> Opened Tank Valve...\n')
        gpio.output( pins['TankValvePin'], True )
        states['TankValve'] = True
        print('--> Fill Tank Pin Opened\n')
        
def close_tank_valve(lock, pins) -> None: # Trigger Open Tank Relay
    with lock:
        print('--> Closed Tank Valve...\n')
        gpio.output( pins['TankValvePin'], False )
        states['TankValve'] = False
        print('--> Closed Tank Valve\n')

def close_vent(lock, pins) -> None: # Trigger to Close Vent Relay
    with lock:
        print('--> Closing Vent...\n')
        gpio.output( pins['VentValvePin'], True )
        states['VentValve'] = True
        print('--> Closed Vent\n')
        
def open_vent(lock, pins) -> None: # Trigger to Open Vent Relay
    with lock:
        print('--> Opening Vent...\n')
        gpio.output( pins['VentValvePin'], False )
        states['VentValve'] = False
        print('--> Opened Vent\n')


def open_gox(lock, pins) -> None: # Trigger to Open GOX Relay
    with lock:
        print('--> Flowing GOX...\n')
        gpio.output( pins['GOXValvePin'], True )
        states['GOXValve'] = True
        print('--> Started GOX\n')

def close_gox(lock, pins) -> None: # Trigger to Close GOX relay
    with lock:
        print('--> Stopping GOX...\n')
        gpio.output( pins['GOXValvePin'], False )
        states['GOXValve'] = False
        print('--> Stopped GOX\n')

def ignition(lock, pins) -> None: # Trigger to Start Ignition Relay
    with lock:
        print('--> Ignition!...\n')
        gpio.output( pins['IgnitionPin'], True )
        states['IgnitionTrigger'] = True
        print('--> !!Ignition!!\n')

def stop_ignition(lock, pins) -> None: # Trigger to Stop Ignition Relay
    with lock:
        print('--> Stopping Ignition...\n')
        gpio.output( pins['IgnitionPin'], False )
        states['IgnitionTrigger'] = False
        print('--> Stopped Ignintion\n')
        
def arm_ignition(lock, pins) -> None: # Arm Ignition Sequence
    with lock:
        print('--> Arming Ignition Sequence...\n')
        armed = True
        states['ArmingTrigger'] = True
        print('--> Armed Ignition Sequence\n')
        
def auto_ignition(lock, pins) -> None: # Auto Ignition Sequence
    with lock:
        print('--> Auto Ignition Sequence Initiated!...\n')
        
def abort(lock, pins) -> None: # Abort Sequence
    with lock:
        print('--> !!ABORTING!!...\n')
        
def get_pins(lock, pins) -> None: # Get Pins
    with lock:
        print('--> Getting Pins...\n')
        print(pins)
        print('\n')

def get_pin_states(lock, pins) -> None:
    with lock:
        print('--> Getting Pin States...\n')
        print(states)
        print('\n')
    
def check_armed(lock, pins) -> None:
    with lock:
        print('--> Checking If Armed...\n')
        print(armed)
        print('\n')

def unknown_command(lock, pins):
    with lock:
        print('--> Unknown command\n')        
