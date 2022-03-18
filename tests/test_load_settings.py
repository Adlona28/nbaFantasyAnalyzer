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
        

class TestConnectionSettings(unittest.TestCase):
    
    @patch('clock.omron_clock._current_directory')
    def test_load_settings(self, mock_current_directory):
        
        settings_file_path = os.path.join(CURRENT_DIRECTORY, 'this_will_be_deleted')
        mock_current_directory.return_value  = settings_file_path  
        
        user, password = load_settings()
        self.assertEqual(user, 'this_is_the_user')
        self.assertEqual(password, 'this_is_the_password')
        

if __name__ == '__main__':
    unittest.main()
