 #! PYTHON DOES NOT HONOR CONSTANTS SO YOU HAVE TO INSTEAD

from typing import Any, Tuple, Union # For typehinting
from commands import * # For command headers


motd: str = '\n------------\n~~ARC Ground Support PI Software~~\n------------\n'

watchdog_timout_delay: float = 60 #* In Seconds
host_ip_address: str = ''

GOXCloseDelay: float = 1.5 #* In Seconds
IgniteDelay: float = 0.25 #* In Seconds

PINS: dict[str, int] = { # Pin Dict

    'BottleValvePin' : 4,
    'TankValvePin' : 27,
    'VentValvePin' : 22,
    'GOXValvePin' : 24,
    'IgnitionPin' : 25,
    'ArmingPin': 26

}

COMMANDS: dict[Any, Any] = { # Command dict

#*  ('Command', 'Description'): function_name

    ('?', 'Help Screen'): list_commands,
    ('help', 'Help Screen'): list_commands,
    ('q', 'Quit'): None,
    ('quit', 'Quit'): None,
    ('exit', 'Quit'): None,
    ('clear', 'Clear Screen'): clear,
    ('cls', 'Clear Screen'): clear,

    ('open bottle valve', 'Opens Bottle Valve'): open_bottle_valve,
    ('close bottle valve', 'Closes Bottle Valve'): close_bottle_valve,
    ('open tank valve', 'Opens Tank Valve'): open_tank_valve,
    ('close tank valve', 'Closes Tank Valve'): close_tank_valve,
    ('open gox valve', 'Opens GOX Valve'): open_gox,
    ('close gox valve', 'Closes GOX Valve'): close_gox,
    ('open vent valve', 'Opens Vent Valve'): open_vent,
    ('close vent valve', 'Closes Vent Valve'): close_vent,
    ('start ignition', 'Triggers Ignition Start'): ignition,
    ('stop ignition', 'Triggers Ignition Stop'): stop_ignition,
     
    ('arm ignition','Arms Ignition Sequence'): arm_ignition,
    ('disarm ignition','Disarms Igninition Sequence'): disarm_ignition,
    ('auto ignition','Automatically Perform Igniton Sequence'): auto_ignition,
    ('abort','Abort All Processes and Exit Program'): abort,
    ('soft abort', 'Only Abort All Processes' ): abort,
    
    ('get pins', 'Get dict of pins'): get_pins,
    ('get pin states', 'Get states of pins') : get_pin_states,
    ('check if armed', 'Check if Ignition Sequence is Armed'): check_armed

}
