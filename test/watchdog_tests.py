import pytest
from ipaddress import IPv4Address
from subprocess import check_output
import sys

sys.path.append(r'E:\School\3rdYear\Clubs\ARC\Spaceport-2024\Ground-Support\PadRunner\src')
from watchdog import check_ssh

@pytest.mark.parametrize(
    "ssh_alive, expected_result",
    [
        ("fe80::1", True),  # IPv6 address containing 'fe80'
        ("fe80::1:1234", True),  # IPv6 address containing 'fe80' and ':'
        ("192.168.0.1", True),  # Valid IPv4 address
        ("192.168.0.1:1234", True),  # Valid IPv4 address containing ':'
        ("", False),  # Empty string
        ("fe80::1:1234", False),  # IPv6 address containing ':', but not 'fe80'
        ("192.168.0.1:1234:5678", False),  # Invalid IPv4 address containing multiple ':'
        ("not_an_ip_address", False),  # Invalid IP address
    ]
)
def test_check_ssh(ssh_alive, expected_result, mocker):
    # Arrange

    # Act
    mocker.patch('watchdog.check_output', return_value=ssh_alive)
    result = check_ssh()
    print(f'{result} : {expected_result}')

    # Assert
    assert result == expected_result
