 #! PYTHON DOES NOT HONOR CONSTANTS SO YOU HAVE TO INSTEAD
 
PINS: dict[str, int] = {
    
    'BottleFillPin' : 4,
    'TankFillPin' : 27,
    'VentPin' : 22,
    'IgnitePin' : 22
    
}

AutoGOXClose: bool = True
AutoIgniterOpen: bool =  True

GOXCloseDelay: float = 1.5 #* In Seconds
IgniteDelay: float = 0.25 #* In Seconds
