import datetime
import random
import numpy as np
import pandas as pd

import day_schedule

class my_schedule(object):
    
    def __init__(self, schedule_name = 'test_' + str(random.randint(1, 99)) + '_' + str(random.randint(1, 99)) + '_' + str(random.randint(1, 99)) + '_' + str(random.randint(1, 99))):
        
        self._full_schedule_name = schedule_name + '_all_day_schedules'

        try:
            self._day_schedules = pd.read_pickle(self._full_schedule_name)
        
        except FileNotFoundError:
        
            todays_date = datetime.datetime.now().date()

            index = pd.date_range(todays_date - datetime.timedelta(1), periods = 1, freq = 'D')

            columns = ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30',\
                      '4:00', '4:30', '5:00', '5:30', '6:00', '6:30', '7:00', '7:30',\
                      '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30',\
                      '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',\
                      '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',\
                      '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']

            data = np.array([np.array(['Sleep'] * len(columns))])

            self._day_schedules = pd.DataFrame(data, index = index, columns = columns)
      
    @property
    def full_schedule_name(self):
        return self._full_schedule_name
    
    @property
    def day_schedules(self):
        return self._day_schedules
        
    def add_day(self):
        return None
        
    def get_days(self):
        return None