import RPi.GPIO as gpio # GPIO Access
from typing import Union
from os import system

states: dict[str, bool] = { # For pin states
    
    'BottleValve': False,
    'TankValve': False,
    'VentValve': False,
    'GOXValve': False,
    'ArmingTrigger': False,
    'IgnitionTrigger': False
    
    }

def Get_State( key: str ) -> Union[ bool, None ]: return states[key] # Get pin state

def Default_Pins( pins ) -> None:
    gpio.output( pins['BottleValvePin'], False )
    gpio.output( pins['TankValvePin'], False )
    gpio.output( pins['GOXValvePin'], False )
    gpio.output( pins['VentValvePin'], False )
    print("Defaulted Pins...\n")

def console() -> str: # Console Input
    cmd = input('> ').lower()
    return cmd

def clear( pins ) -> None: # Clear Console
    system('clear')

def list_commands( commands ) -> None: # List out all commands
    print('--> Here is a list of all the registered commands: ')
    for key in commands:
        print( f'{key[0]} - {key[1]}\n' )

def open_bottle_valve( pins ) -> None: # Trigger to Open Bottle Relay
    print('--> Opening Bottle Valve...\n')
    gpio.output( pins['BottleValvePin'], True )
    states['BottleValve'] = True
    print('--> Bottle Valve Opened\n')

def close_bottle_valve( pins ) -> None: # Trigger to Open Bottle Relay
    print('--> Stopping Bottle valve...\n')
    gpio.output( pins['BottleValvePin'], False )
    states['BottleValve'] = False
    print('--> Bottle Valve Closed\n')

def open_tank_valve( pins ) -> None: # Trigger Open Tank Relay
    print('--> Opened Tank Valve...\n')
    gpio.output( pins['TankValvePin'], True )
    states['TankValve'] = True
    print('--> Fill Tank Pin Opened\n')
        
def close_tank_valve( pins ) -> None: # Trigger Open Tank Relay
    print('--> Closed Tank Valve...\n')
    gpio.output( pins['TankValvePin'], False )
    states['TankValve'] = False
    print('--> Tank Valve Closed\n')

def close_vent( pins ) -> None: # Trigger to Close Vent Relay
    print('--> Closing Vent...\n')
    gpio.output( pins['VentValvePin'], True )
    states['VentValve'] = True
    print('--> Vent Closed\n')
        
def open_vent( pins ) -> None: # Trigger to Open Vent Relay
    print('--> Opening Vent...\n')
    gpio.output( pins['VentValvePin'], False )
    states['VentValve'] = False
    print('--> Vent Opened\n')


def open_gox( pins ) -> None: # Trigger to Open GOX Relay
    print('--> Flowing GOX...\n')
    gpio.output( pins['GOXValvePin'], True )
    states['GOXValve'] = True
    print('--> GOX Opened\n')

def close_gox( pins ) -> None: # Trigger to Close GOX relay
    print('--> Closing GOX...\n')
    gpio.output( pins['GOXValvePin'], False )
    states['GOXValve'] = False
    print('--> GOX Closed\n')

def ignition( pins ) -> None: # Trigger to Start Ignition Relay
    print('--> Ignition!...\n')
    gpio.output( pins['IgnitionPin'], True )
    states['IgnitionTrigger'] = True
    print('--> !!Ignition!!\n')

def stop_ignition( pins ) -> None: # Trigger to Stop Ignition Relay
    print('--> Stopping Ignition...\n')
    gpio.output( pins['IgnitionPin'], False )
    states['IgnitionTrigger'] = False
    print('--> Ignition Stopped\n')
        
def arm_ignition( pins ) -> None: # Arm Ignition Sequence
    print('--> Arming Ignition Sequence...\n')
    gpio.output( pins['ArmingPin'], True )
    states['ArmingTrigger'] = True
    print('--> Ignition Sequence Armed\n')
    
def disarm_ignition( pins ) -> None: # Arm Ignition Sequence
    print('--> Disarming Ignition Sequence...\n')
    states['ArmingTrigger'] = False
    print('--> Ignition Sequence Disarmed\n')
        
def auto_ignition( pins ) -> None: # Auto Ignition Sequence
    print('--> Auto Ignition Sequence Initiated!...\n')
        
def abort( pins ) -> None: # Abort Sequence
    print('--> !!ABORTING!!...\n')
        
def get_pins( pins ) -> None: # Get Pins
    print('--> Getting Pins...\n')
    print(pins)
    print('\n')

def get_pin_states( pins ) -> None:
    print('--> Getting Pin States...\n')
    print(states)
    print('\n')
    
def check_armed( pins ) -> None:
    print('--> Checking If Armed...\n')
    print(Get_State('ArmingTrigger'))
    print('\n')

def unknown_command( pins ):
    print('--> Unknown command\n')        
