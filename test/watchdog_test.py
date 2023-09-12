import pytest
import sys

sys.path.append(r'E:\School\3rdYear\Clubs\ARC\Spaceport-2024\Ground-Support\PadRunner\src')
from watchdog import *

class Test_Watchdog:

    @pytest.mark.parametrize(
        "ssh_alive, expected_result",
        [
            ("fe80::1", True),  # IPv6 address containing 'fe80'
            ("fe80::1:1234", True),  # IPv6 address containing 'fe80' and ':'
            ("192.168.0.1", True),  # Valid IPv4 address
            ("192.168.0.1:1234", True),  # Valid IPv4 address containing ':'
            ("", False),  # Empty string
            (":1:1234", False),  # IPv6 address containing ':', but not 'fe80'
            ("not_an_ip_address", False),  # Invalid IP address
        ]
    )
    def test_check_ssh(self, ssh_alive, expected_result, mocker):
        # Arrange

        # Act
        mocker.patch('watchdog.getoutput', return_value=ssh_alive)
        result = check_ssh()
        print(f'{result} : {expected_result}')

        # Assert
        assert result == expected_result

    @pytest.mark.parametrize(
        "check, expected_result",
        [
            ([True, True], 'pass'), # Both connection checks are True | pass
            ([True, False], 'pass'), # First check True, Second is False | should pass as 2nd call will be sent to next iteration of the loop
            ([False, True], 'pass'), # First check False, Second check True | should pass after re-check
            ([False, False], 'abort'), # Both checks False | abort
        ]
    )
    def test_check_connection(self, check, expected_result, mocker):
        # Arrange
        mocker.patch('watchdog.check_ssh', side_effect=check)
        
        # Act
        result = check_connection(2)

        # Assert
        assert expected_result in result
