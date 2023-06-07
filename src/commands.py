from functions import *

def console(q, lock) -> None:
    while 1:
        input()   # After pressing Enter you'll be in "input mode"
        with lock:
            cmd = input('> ')

        q.put(cmd)
        if cmd == 'quit':
            break

def list_commands(lock, commands) -> None:
    with lock:
        print('--> Here is a list of all the registered commands')
        for key in commands:
            print( key + '\n' )

def fill_bottle(lock, pins) -> None:
    with lock:
        print('--> Filling Bottle...\n')
        Fill_Bottle( pins['BottleFillPin'] )

def fill_tank (lock, pins) -> None:
    with lock:
        print('--> Filling Tank...\n')
        Fill_Tank( pins['TankFillPin'] )

def open_vent(lock, pins) -> None:
    with lock:
        print('--> Opening Vent...\n')
        Open_Vent( pins['VentPin'] )
        
def start_gox(lock, pins) -> None:
    with lock:
        print('--> Flowing GOX...\n')
        Start_GOX( pins['GOXPin'] )
        
def stop_gox(lock, pins) -> None:
    with lock:
        print('--> Stopping GOX...\n')
        Stop_GOX( pins['GOXPin'] )
        
def ignite(lock, pins) -> None:
    with lock:
        print('--> Ignition!...\n')
        Ignite( pins['IgnitePin'] )
        
def stop_ignition(lock, pins) -> None:
    with lock:
        print('--> Stopping Ignition...\n')
        Stop_Ignition( pins['IgnitePin'] )

def invalid_input(lock) -> None:
    with lock:
        print('--> Unknown command\n')