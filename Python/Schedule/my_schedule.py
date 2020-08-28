import warnings

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
            self._day_schedules = self.generate_new_null_day(days_from_today = -1)
      
    @property
    def full_schedule_name(self):
        return self._full_schedule_name
    
    @property
    def day_schedules(self):
        return self._day_schedules
    
    @property
    def last_day_in_calendar(self):
        return self.day_schedules.index.date[-1]
    
    @property
    def day_hours(self):
        return [str(i) for i in range(24)]
    
    @property
    def day_minutes(self):
        return ['00', '05'] + [str(10 + (5 * i)) for i in range(10)]
    
    @property
    def day_columns(self):
        return [hour + ':' + minute for hour in self.day_hours for minute in self.day_minutes]
    
    @property
    def null_data(self):
        return np.array([np.array(['Sleep'] * len(self.day_columns))])
    
    @property
    def days_until_today(self):
        return (datetime.datetime.now().date() - self.last_day_in_calendar).days
    
    @property
    def days_until_monday(self):
        return ((-1 * self.last_day_in_calendar.weekday()) + 7) % 7
    
    @property
    def days_until_tuesday(self):
        return (days_until_monday + 1) % 7
    
    @property
    def days_until_wednesday(self):
        return (days_until_monday + 2) % 7
    
    @property
    def days_until_thursday(self):
        return (days_until_monday + 3) % 7
    
    @property
    def days_until_friday(self):
        return (days_until_monday + 4) % 7
    
    @property
    def days_until_saturday(self):
        return (days_until_monday + 5) % 7
    
    @property
    def days_until_sunday(self):
        return (days_until_monday + 6) % 7
    
    @property
    def days_until_weekend(self):
        return self.days_until_saturday
    
    @property
    def days_left_in_week(self):
        return self.days_until_monday
    
    @property
    def days_left_in_work_week(self):
        if datetime.datetime.now().weekday() > 4:
            warnings.warn(message = "It is not currently the work week.")
            return 0
        else:
            return self.days_until_friday
    
    @property
    def days_left_in_weekend(self):
        if datetime.datetime.now().weekday() < 5:
            warnings.warn(message = "It is not currently the weekend.")
            return 0
        else:
            return self.days_until_monday
    
    def index_from_today(self, days_from_today):
        return pd.date_range(datetime.datetime.now().date() + datetime.timedelta(days_from_today), periods = 1, freq = 'D')
    
    def generate_new_null_day(self, days_from_today = None):
        
        if days_from_today == None:
            raise ValueError("A number of days from today should be entered. A value of 1 would be tomorrow, a value of 0 would be today, a value of -1 would be yesterday, etc.")
            
        else:
            
            index = self.index_from_today(days_from_today)
            columns = self.day_columns
            data = self.null_data
            
            return pd.DataFrame(data, index = index, columns = columns)
        
    def add_new_null_day(self):
        new_null_day = self.generate_new_null_day((self.last_day_in_calendar - datetime.datetime.now().date()).days + 1)
        self._day_schedules = pd.concat([self._day_schedules, new_null_day])
    
    def generate_some_new_null_days(self, number_of_days):
        return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(1, number_of_days + 1)])
    
    def add_some_new_null_days(self, number_of_days):
        new_null_rest_of_work_week = self.generate_new_null_rest_of_work_week()
        self._day_schedules = pd.concat([self._day_schedules, new_null_rest_of_work_week])
    
    ###########################################################################################################
    # Need to add 'generate_new_null_until_today' or else the following functions don't make sense            #
    # You also need to have a check in the following functions that will call 'generate_new_null_until_today'.#
    # If not called, these functions will treat 'today' as if it is the 'last day in the schedule'            #
    ###########################################################################################################
    
    def generate_new_null_rest_of_week(self):
        return pd.concat([self.generate_new_null_day(days_from_today = i) for i in self.days_left_in_week])
    
    def add_new_null_rest_of_week(self):
        new_null_rest_of_week = self.generate_new_null_rest_of_week()
        self._day_schedules = pd.concat([self._day_schedules, new_null_rest_of_week])
        
    def generate_new_null_rest_of_work_week(self):
        return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(1, self.days_left_in_work_week)])
    
    def add_new_null_rest_of_work_week(self):
        new_null_rest_of_work_week = self.generate_new_null_rest_of_work_week()
        self._day_schedules = pd.concat([self._day_schedules, new_null_rest_of_work_week])
        
    def generate_new_null_rest_of_weekend(self):
        return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(1, self.days_left_in_weekend)])
    
    def add_new_null_rest_of_weekend(self):
        new_null_rest_of_weekend = self.generate_new_null_rest_of_weekend()
        self._day_schedules = pd.concat([self._day_schedules, new_null_rest_of_weekend])
    
    def generate_new_day(self, days_from_today = None):
        
        if days_from_today == None:
            raise ValueError("A number of days from today should be entered. A value of 1 would be tomorrow, a value of 0 would be today, a value of -1 would be yesterday, etc.")
            
        else:
            
            index = self.index_from_today(days_from_today)
            columns = self.day_columns
            data = self.null_data
            
            return pd.DataFrame(data, index = index, columns = columns)
        
    def add_new_day(self):
        return None
    
    def generate_new_days(self):
        return None
        
    def add_new_days(self):
        return None
    
    def generate_new_rest_of_week(self):
        return None
        
    def add_new_rest_of_week(self):
        return None
    
    def generate_new_rest_of_work_week(self):
        return None
        
    def add_new_rest_of_work_week(self):
        return None
    
    def generate_new_rest_of_weekend(self):
        return None
        
    def add_new_rest_of_weekend(self):
        return None