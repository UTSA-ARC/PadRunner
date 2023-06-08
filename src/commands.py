import RPi.GPIO as gpio # GPIO Access
from typing import Union

states: dict[str, bool] = {} # For pin states
armed: bool = False

def Get_State( key: str ) -> Union[ bool, None ]: return states[key] # Get pin state

def console(q, lock) -> None: # Console Thread
    while 1: # Thread inf loop
        input()   # After pressing Enter you'll be in "input mode"
        with lock:
            cmd = input('> ')
            cmd = cmd.lower() # Lowercase it all

        q.put(cmd)
        if cmd in ['quit', 'q']:
            break

def list_commands(lock, commands) -> None: # List out all commands
    with lock:
        print('--> Here is a list of all the registered commands')
        print( 'q' + '\n' )
        print( 'quit' + '\n' )
        for key in commands:
            print( key + '\n' )

def bottle_valve(lock, pins) -> None: # Trigger to Open Bottle Relay
    with lock:
        print('--> Filling Bottle...\n')
        gpio.output( pins['BottleFillPin'], True )
        states['FillBottle'] = True
        print('--> Fill Bottle Pin Activated\n')

def tank_valve(lock, pins) -> None: # Trigger Open Tank Relay
    with lock:
        print('--> Filling Tank...\n')
        gpio.output( pins['TankFillPin'], True )
        states['FillTank'] = True
        print('--> Fill Tank Pin Activated\n')

def close_vent(lock, pins) -> None: # Trigger to Close Vent Relay
    with lock:
        print('--> Closing Vent...\n')
        gpio.output( pins['VentPin'], True )
        states['Vent'] = True
        print('--> Closed Vent\n')
        
def open_vent(lock, pins) -> None: # Trigger to Open Vent Relay
    with lock:
        print('--> Opening Vent...\n')
        gpio.output( pins['VentPin'], False )
        states['Vent'] = True
        print('--> Opened Vent\n')


def open_gox(lock, pins) -> None: # Trigger to Open GOX Relay
    with lock:
        print('--> Flowing GOX...\n')
        gpio.output( pins['GOXPin'], True )
        states['GOX'] = True
        print('--> Started GOX\n')

def close_gox(lock, pins) -> None: # Trigger to Close GOX relay
    with lock:
        print('--> Stopping GOX...\n')
        gpio.output( pins['GOXPin'], True )
        states['GOX'] = False
        print('--> Stopped GOX\n')

def ignition(lock, pins) -> None: # Trigger to Start Ignition Relay
    with lock:
        print('--> Ignition!...\n')
        gpio.output( pins['IgnitePin'], True)
        states['Ignition'] = True
        print('--> !!Ignition!!\n')

def stop_ignition(lock, pins) -> None: # Trigger to Stop Ignition Relay
    with lock:
        print('--> Stopping Ignition...\n')
        gpio.output( pins['IgnitePin'], True )
        states['Ignition'] = False
        print('--> Stopped Ignintion\n')
        
def arm_ignition(lock, pins) -> None: # Arm Ignition Sequence
    with lock:
        print('--> Arming Ignition Sequence...\n')
        armed = True
        
def auto_ignition(lock, pins) -> None: # Auto Ignition Sequence
    with lock:
        print('--> Auto Ignition Sequence Initiated!...\n')
        
def abort(lock, pins) -> None:
    print('--> !!ABORTING!!...\n')
    

def get_pin_states(lock, pins) -> None:
    with lock:
        print('--> Getting Pin States...\n')
        print(states)
        print('\n')
    
def check_armed(lock, pins) -> None:
    with lock:
        print('--> Getting If Armed...\n')
        print(armed)
        print('\n')

def unknown_command(lock, pins):
    with lock:
        print('--> Unknown command\n')        
