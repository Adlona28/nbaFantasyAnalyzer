import sys
import os


PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


import unittest
from unittest.mock import patch, MagicMock
sys.modules['selenium'] = MagicMock()
sys.modules['selenium.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.common.action_chains'] = MagicMock()

from clock import load_settings
        

class TestOneShotRegister(unittest.TestCase):
    
    @patch('clock.omron_clock._current_directory')
    def test_register(self, mock_current_directory):
        pass
        

if __name__ == '__main__':
    unittest.main()
