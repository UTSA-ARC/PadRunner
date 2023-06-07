from functions import *
from config import PINS, COMMANDS

def console(q, lock) -> None:
    while 1:
        input()   # After pressing Enter you'll be in "input mode"
        with lock:
            cmd = input('> ')

        q.put(cmd)
        if cmd == 'quit':
            break

def list_commands(lock) -> None:
    print('--> Here is a list of all the registered commands')
    for key in COMMANDS.keys():
        print( key + '\n' )

def fill_bottle(lock) -> None:
    with lock:
        print('--> Filling Bottle...\n')
        Fill_Bottle( PINS.BottleFillPin )

def fill_tank (lock) -> None:
    with lock:
        print('--> Filling Tank...\n')
        Fill_Tank( PINS.TankFillPin )

def open_vent(lock) -> None:
    with lock:
        print('--> Opening Vent...\n')
        Open_Vent( PINS.VentPin )
        
def start_gox(lock) -> None:
    with lock:
        print('--> Flowing GOX...\n')
        Start_GOX( PINS.GOXPin )
        
def stop_gox(lock) -> None:
    with lock:
        print('--> Stopping GOX...\n')
        Stop_GOX( PINS.GOXPin )
        
def ignite(lock) -> None:
    with lock:
        print('--> Ignition!...\n')
        Ignite( PINS.IgnitePin )
        
def stop_ignition(lock) -> None:
    with lock:
        print('--> Stopping Ignition...\n')
        Stop_Ignition( PINS.IgnitePin )

def invalid_input(lock) -> None:
    with lock:
        print('--> Unknown command\n')