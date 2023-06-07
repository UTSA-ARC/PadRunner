import RPi.GPIO as gpio

states: dict[str, bool] = {}

def Get_State( key: str ) -> ( bool | None ): return states[key]

def Fill_Bottle( pin: int, ) -> None:
    gpio.output( pin, True )
    states['FillBottle'] = True
    print('Fill Bottle Pin Activated\n')
    
def Fill_Tank( pin: int ) -> None:
    gpio.output( pin, True )
    states['FillTank'] = True
    print('Fill Tank Pin Activated\n')
    
def Open_Vent( pin: int ) -> None:
    gpio.output( pin, True )
    states['FillVent'] = True
    print('Opened Vent\n')
    
def Start_GOX( pin: int ) -> None:
    gpio.output( pin, True )
    states['GOX'] = True
    print('Started GOX\n')

def Stop_GOX( pin: int ) -> None:
    gpio.output( pin, True )
    states['GOX'] = False
    print('Stopped GOX\n')
    
def Ignite( pin: int ) -> None:
    gpio.output( pin, True)
    states['Ignition'] = True
    print('!!Ignition!!\n')

def Stop_Ignition( pin: int ) -> None:
    gpio.output( pin, True )
    states['Ignition'] = False
    print('Stopped Ignintion\n')
