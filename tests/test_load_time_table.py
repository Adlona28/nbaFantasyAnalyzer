# -*- coding: utf-8 -*-

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

from automatic_register.time_table import load_work_time, today_working_time, _check_time_table_format 
from automatic_register.automatic_register import _time_entries_to_date_entries

class TestAutomaticRegisterTimeTable(unittest.TestCase):
    
    @patch('clock.omron_clock._current_directory')
    def test_load_time_table(self, mock_current_directory):
        
        settings_file_path = os.path.join(CURRENT_DIRECTORY, 'this_will_be_deleted')
        mock_current_directory.return_value  = settings_file_path  
        
        time_table = load_work_time()
        self.assertEqual(time_table['monday'][0][0], '10:00')
        self.assertEqual(time_table['monday'][0][1], 'IN')
        self.assertEqual(time_table['wednesday'][1][0], '20:00')
        self.assertEqual(time_table['wednesday'][1][1], 'OUT')

    def test_time_table_format(self):

        time_table = {'monday': [['10:00', 'IN'],['11:00', 'OUT'],['12:00', 'IN'],['13:00', 'OUT']]}
        self.assertEqual(_check_time_table_format(time_table), True)
        
        time_table = {'tuesday': [['10:00', 'OUT'],['11:00', 'OUT'],['12:00', 'IN'],['13:00', 'OUT']]}
        self.assertEqual(_check_time_table_format(time_table), False)
        
        time_table = {'monday': [['10:00', 'IN'],['11:00', 'OUT'],['12:00', 'IN'],['13:00', 'IN']]}
        self.assertEqual(_check_time_table_format(time_table), False)

        time_table = {'monday': [['10:00', 'IN'],['11:00', 'IN'],['12:00', 'IN'],['13:00', 'OUT']]}
        self.assertEqual(_check_time_table_format(time_table), False)

    def test_today_time_table(self):
        pass

    def test_time_to_date_conversion(self):

        print("")
        time_entries = [['00:00', 'IN'],['11:01', 'OUT'],['12:59', 'IN'],['23:59', 'OUT']]        
        print(time_entries)
        
        import datetime as dt
        today = dt.date.today()
        date_entries = _time_entries_to_date_entries(today, time_entries)
            
        for date_entry, time_entry in zip(date_entries, time_entries):
            self.assertEqual(date_entry[0].strftime("%d/%m/%Y, %H:%M:%S"), 
                "%s, %s:00" % (today.strftime("%d/%m/%Y"), time_entry[0]))


if __name__ == '__main__':
    unittest.main()
