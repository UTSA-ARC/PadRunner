import pytest
from io import StringIO
import sys

sys.path.append(r'E:\School\3rdYear\Clubs\ARC\Spaceport-2024\Ground-Support\PadRunner\src')
import main

class Test_Commands():
    
    def test_special_case_quit(self):
        result = main.check_special_cases('quit')
        assert result == False

    def test_special_case_help(self):
        result = main.check_special_cases('help')
        assert result == True
    
    @pytest.mark.parametrize(
        "enabled, expected_stdout", \
        [
            (True,''), # Gox enabled
            (False, '\n--> You do not have GOX enabled, please close the program and edit `src/config.py` to enable it\n\n'), # Gox disabled
        ]
    )
    def test_special_cases_GOX(self, mocker, capsys, enabled, expected_stdout):
        
        mocker.patch.object(main, 'Enable_Gox', enabled)
        
        result = main.check_special_cases('gox')
        
        out, err = capsys.readouterr()
        sys.stdout.write(out)
        sys.stderr.write(err)
        
        assert out == expected_stdout
        assert result == True
        
    
        