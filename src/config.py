 #! PYTHON DOES NOT HONOR CONSTANTS SO YOU HAVE TO INSTEAD

from typing import Any # For typehinting
from commands import * # For command headers

watchdog_timout_delay: float = 60 #* In Seconds
host_ip_address: str = ''

PINS: dict[str, int] = { # Pin Dict

    'BottleValvePin' : 4,
    'TankValvePin' : 27,
    'VentValvePin' : 22,
    'GOXValvePin' : 24,
    'IgnitionPin' : 25

}

FUNCTION_COMMANDS: dict[str, Any] = { # Command dict

    '?': list_commands,
    'help': list_commands,
    'q': '',
    'quit':'',

    'open bottle valve': open_bottle_valve,
    'close bottle valve': close_bottle_valve,
    'open tank valve': open_tank_valve,
    'close tank valve': close_tank_valve,
    'open gox valve': open_gox,
    'close gox valve': close_gox,
    'open vent valve': open_vent,
    'close vent valve': close_vent,
    'start ignition': ignition,
    'stop ignition': stop_ignition,
    
    'arm ignition': arm_ignition,
    'auto ignition': auto_ignition,
    'abort': abort,
    
    'get pins': get_pins,
    'get pin states': get_pin_states,
    'check if armed': check_armed 

}

GOXCloseDelay: float = 1.5 #* In Seconds
IgniteDelay: float = 0.25 #* In Seconds
