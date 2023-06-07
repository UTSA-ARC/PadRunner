import RPi.GPIO as gpio # GPIO Access

states: dict[str, bool] = {} # For pin states

def Get_State( key: str ) -> ( bool | None ): return states[key] # Get pin state

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

def fill_bottle(lock, pins) -> None: # Trigger to Start Fill Bottle Relay
    with lock:
        print('--> Filling Bottle...\n')
        gpio.output( pins['BottleFillPin'], True )
        states['FillBottle'] = True
        print('--> Fill Bottle Pin Activated\n')

def fill_tank (lock, pins) -> None: # Trigger Start Fill Tank Relay
    with lock:
        print('--> Filling Tank...\n')
        gpio.output( pins['TankFillPin'], True )
        states['FillTank'] = True
        print('--> Fill Tank Pin Activated\n')

def open_vent(lock, pins) -> None: # Trigger to Open Vent Relay
    with lock:
        print('--> Opening Vent...\n')
        gpio.output( pins['VentPin'], True )
        states['Vent'] = True
        print('--> Opened Vent\n')

def start_gox(lock, pins) -> None: # Trigger to Open GOX Relay
    with lock:
        print('--> Flowing GOX...\n')
        gpio.output( pins['GOXPin'], True )
        states['GOX'] = True
        print('--> Started GOX\n')

def stop_gox(lock, pins) -> None: # Trigger to Close GOX relay
    with lock:
        print('--> Stopping GOX...\n')
        gpio.output( pins['GOXPin'], True )
        states['GOX'] = False
        print('--> Stopped GOX\n')

def ignite(lock, pins) -> None: # Trigger to Start Ignition Relay
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

def unknown_command(lock, pins):
    with lock:
        print('--> Unknown command\n')        
