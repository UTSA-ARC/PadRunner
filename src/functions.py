import RPi.GPIO as gpio

states: dict[str, bool] = {}

def FillBottle( pin: int, ) -> None:
    gpio.output( pin, True )
    states['FillBottle'] = True
    print('Fill Bottle Pin Activated\n')
    
def FillTank( pin: int ) -> None:
    gpio.output( pin, True )
    states['FillTank'] = True
    print('Fill Tank Pin Activated\n')
    
def OpenVent( pin: int ) -> None:
    gpio.output( pin, True )
    states['FillVent'] = True
    print('Opened Vent\n')
    
def StartGOX( pin: int ) -> None:
    gpio.output( pin, True )
    states['GOX'] = True
    print('Started GOX\n')

def StopGOX( pin: int ) -> None:
    gpio.output( pin, True )
    states['GOX'] = False
    print('Stopped GOX\n')
    
def Ignite( pin: int ) -> None:
    gpio.output( pin, True)
    states['Ignition'] = True
    print('!!Ignition!!\n')
    