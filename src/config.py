 #! PYTHON DOES NOT HONOR CONSTANTS SO YOU HAVE TO INSTEAD

from typing import Any # For typehinting
from commands import * # For command dictionary
 
PINS: dict[str, int] = {
    
    'BottleFillPin' : 4,
    'TankFillPin' : 27,
    'VentPin' : 22,
    'GOXPin' : 24,
    'IgnitePin' : 22
    
}

COMMANDS: dict[str, Any] = {
    
    #* Do not edit position of help commands
    '?': list_commands,
    'help': list_commands,
    
    'fill bottle': fill_bottle,
    'fill tank': fill_tank,
    'start gox': start_gox,
    'stop gox': stop_gox,
    'ignite': ignite,
    'stop ignition': stop_ignition     
                            
}

AutoGOXClose: bool = True
AutoIgniterOpen: bool =  True
AutoIgniterClose: bool = True

GOXCloseDelay: float = 1.5 #* In Seconds
IgniteDelay: float = 0.25 #* In Seconds
