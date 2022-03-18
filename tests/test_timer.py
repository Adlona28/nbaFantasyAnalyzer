import sys
import os
import time


PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


import unittest
from unittest.mock import patch, MagicMock
sys.modules['selenium'] = MagicMock()
sys.modules['selenium.webdriver'] = MagicMock()
sys.modules['selenium.webdriver.common.action_chains'] = MagicMock()


from automatic_register.timer import RepeatedTimer


class TestRepeatedTime(unittest.TestCase):
    
    #patch('clock.omron_clock._current_directory')
    def test_load_settings(self):#, mock_current_directory):
        
        def do():
            print("helloworld!!!")

        timer = RepeatedTimer(1.0, do)
        time.sleep(10)
        timer.stop()


if __name__ == '__main__':
    unittest.main()
