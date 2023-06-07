from triggers import * # Access gpio Calls

def console(q, lock) -> None: # Console Thread
    while 1: # Thread inf loop
        input()   # After pressing Enter you'll be in "input mode"
        with lock:
            cmd = input('> ')

        q.put(cmd)
        if cmd == 'quit' or cmd == 'q':
            break

def list_commands(lock, commands) -> None: # List out all commands
    with lock:
        print('--> Here is a list of all the registered commands')
        for key in commands:
            print( key + '\n' )

def fill_bottle(lock, pins) -> None: # Call to Start Fill Bottle Relay
    with lock:
        print('--> Filling Bottle...\n')
        Fill_Bottle( pins['BottleFillPin'] )

def fill_tank (lock, pins) -> None: # Call Start Fill Tank Relay
    with lock:
        print('--> Filling Tank...\n')
        Fill_Tank( pins['TankFillPin'] )

def open_vent(lock, pins) -> None: # Call to Open Vent Relay
    with lock:
        print('--> Opening Vent...\n')
        Open_Vent( pins['VentPin'] )

def start_gox(lock, pins) -> None: # Call to Open GOX Relay
    with lock:
        print('--> Flowing GOX...\n')
        Start_GOX( pins['GOXPin'] )

def stop_gox(lock, pins) -> None: # Call to Close GOX relay
    with lock:
        print('--> Stopping GOX...\n')
        Stop_GOX( pins['GOXPin'] )

def ignite(lock, pins) -> None: # Call to Start Ignition Relay
    with lock:
        print('--> Ignition!...\n')
        Ignite( pins['IgnitePin'] )

def stop_ignition(lock, pins) -> None: # Call to Stop Ignition Relay
    with lock:
        print('--> Stopping Ignition...\n')
        Stop_Ignition( pins['IgnitePin'] )