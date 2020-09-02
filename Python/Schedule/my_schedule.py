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
        return np.array([np.array(['Nothing Scheduled'] * len(self.day_columns))])
    
    @property
    def days_until_today(self):
        return (datetime.datetime.now().date() - self.last_day_in_calendar).days
    
    @property
    def days_until_monday(self):
        return ((-1 * self.last_day_in_calendar.weekday()) + 7) % 7
    
    @property
    def days_until_tuesday(self):
        return (self.days_until_monday + 1) % 7
    
    @property
    def days_until_wednesday(self):
        return (self.days_until_monday + 2) % 7
    
    @property
    def days_until_thursday(self):
        return (self.days_until_monday + 3) % 7
    
    @property
    def days_until_friday(self):
        return (self.days_until_monday + 4) % 7
    
    @property
    def days_until_saturday(self):
        return (self.days_until_monday + 5) % 7
    
    @property
    def days_until_sunday(self):
        return (self.days_until_monday + 6) % 7
    
    @property
    def days_until_next_week(self):
        return self.days_until_monday
    
    @property
    def days_until_next_work_week(self):
        return self.days_until_monday
    
    @property
    def days_until_next_weekend(self):
        return self.days_until_saturday
    
    @property
    def days_left_in_week(self):
        
        if self.last_day_in_calendar.weekday == 6:
            warnings.warn(message = "It is the last day of the week.")
            return 0
        
        else:
            return self.days_until_sunday
    
    @property
    def days_left_in_work_week(self):
    
        if self.last_day_in_calendar.weekday() > 4:
            warnings.warn(message = "It is not currently the work week.")
            return 0
    
        else:
            return self.days_until_friday
    
    @property
    def days_left_in_weekend(self):
        
        if self.last_day_in_calendar.weekday() < 5:
            
            warnings.warn(message = "It is not currently the weekend.")
            return 0
        
        else:
            return self.days_until_sunday
    
    def index_from_today(self, days_from_today):
        return pd.date_range(datetime.datetime.now().date() + datetime.timedelta(days_from_today), periods = 1, freq = 'D')
    
    #def remove_day(self, days_from_today):  
    
    def generate_new_null_day(self, days_from_today = None):
        
        if days_from_today == None:
            raise ValueError("A number of days from today should be entered. A value of 1 would be tomorrow, a value of 0 would be today, a value of -1 would be yesterday, etc.")
            
        else:
            
            index = self.index_from_today(days_from_today)
            columns = self.day_columns
            data = self.null_data
            
            return pd.DataFrame(data, index = index, columns = columns)
        
    def add_new_null_day(self):
        new_null_day = self.generate_new_null_day(-1 * self.days_until_today + 1)
        self._day_schedules = pd.concat([self._day_schedules, new_null_day])
    
    def generate_new_null_days(self, number_of_days):
        return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + number_of_days + 1)])
    
    def add_new_null_days(self, number_of_days):
        new_null_days = self.generate_new_null_days(number_of_days)
        self._day_schedules = pd.concat([self._day_schedules, new_null_days])
    
    def generate_new_null_days_until_today(self):
        return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, 1)])
    
    def add_new_null_days_until_today(self):
        new_null_days_until_today = self.generate_new_null_days_until_today()
        self._day_schedules = pd.concat([self.day_schedules, new_null_days_until_today])
    
    def generate_new_null_rest_of_week(self):
        
        if self.days_left_in_week == 0:
            return None
        
        else:
            return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + self.days_left_in_week + 1)])
    
    def add_new_null_rest_of_week(self):
        
        if self.days_until_today > 0:
            self.add_new_null_days_until_today()
        
        new_null_rest_of_week = self.generate_new_null_rest_of_week()
        
        if new_null_rest_of_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_null_rest_of_week])
        
    def generate_new_null_rest_of_work_week(self):
        
        if self.days_left_in_work_week == 0:
            return None
        
        else:
            return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + self.days_left_in_work_week + 1)])
    
    def add_new_null_rest_of_work_week(self):
        
        if self.days_until_today > 0:
            self.add_new_null_days_until_today()
            
        new_null_rest_of_work_week = self.generate_new_null_rest_of_work_week()
        
        if new_null_rest_of_work_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_null_rest_of_work_week])
        
    def generate_new_null_rest_of_weekend(self):
        
        if self.days_left_in_weekend == 0:
            return None
        
        else:
            return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + self.days_left_in_weekend + 1)])
    
    def add_new_null_rest_of_weekend(self):
        
        if self.days_until_today > 0:
            self.add_new_null_days_until_today()
            
        new_null_rest_of_weekend = self.generate_new_null_rest_of_weekend()
        
        if new_null_rest_of_weekend is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_null_rest_of_weekend])
    
    def generate_new_null_week(self):
        
        if self.days_until_next_week != 1:
            warnings.warn(message = "The last schedule day is not Sunday, so you cannot generate a full week.")
            return None
        
        else:
            return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + 8)])
    
    def add_new_null_week(self):
        
        new_null_week = self.generate_new_null_week()
            
        if new_null_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_null_week])            
        
    def generate_new_null_work_week(self):
        
        if self.days_until_next_work_week != 1:
            warnings.warn(message = "The last schedule day is not Sunday, so you cannot generate a full work week.")
            return None
        
        else:
            return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + 6)])
        
    def add_new_null_work_week(self):
        
        new_null_work_week = self.generate_new_null_work_week()
            
        if new_null_work_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_null_work_week])
        
    def generate_new_null_weekend(self):
        
        if self.days_until_next_weekend != 1:
            warnings.warn(message = "The last schedule day is not Friday, so you cannot generate a full work week.")
            return None
        
        else:
            return pd.concat([self.generate_new_null_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + 3)])
        
    def add_new_null_weekend(self):
        
        new_null_weekend = self.generate_new_null_weekend()
            
        if new_null_weekend is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_null_weekend])
    
    def generate_new_day(self, days_from_today = None):
        
        if days_from_today == None:
            raise ValueError("A number of days from today should be entered. A value of 1 would be tomorrow, a value of 0 would be today, a value of -1 would be yesterday, etc.")
            
        else:
            
            index = self.index_from_today(days_from_today)
            columns = self.day_columns
            data = day_schedule.day_schedule()
            
            return pd.DataFrame(data, index = index, columns = columns)
        
    def add_new_day(self):
        new_day = self.generate_new_day(-1 * self.days_until_today + 1)
        self._day_schedules = pd.concat([self._day_schedules, new_day])
    
    def generate_new_days(self, number_of_days):
        return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + number_of_days + 1)])
    
    def add_new_days(self, number_of_days):
        new_days = self.generate_new_days(number_of_days)
        self._day_schedules = pd.concat([self._day_schedules, new_days])
    
    def generate_new_days_until_today(self):
        return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, 1)])
    
    def add_new_days_until_today(self):
        new_days_until_today = self.generate_new_days_until_today()
        self._day_schedules = pd.concat([self.day_schedules, new_days_until_today])
    
    def generate_new_rest_of_week(self):
        
        if self.days_left_in_week == 0:
            return None
        
        else:
            return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + self.days_left_in_week + 1)])
    
    def add_new_rest_of_week(self):
        
        if self.days_until_today > 0:
            self.add_new_days_until_today()
        
        new_rest_of_week = self.generate_new_rest_of_week()
        
        if new_rest_of_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_rest_of_week])
        
    def generate_new_rest_of_work_week(self):
        
        if self.days_left_in_work_week == 0:
            return None
        
        else:
            return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + self.days_left_in_work_week + 1)])
    
    def add_new_rest_of_work_week(self):
        
        if self.days_until_today > 0:
            self.add_new_days_until_today()
            
        new_rest_of_work_week = self.generate_new_rest_of_work_week()
        
        if new_rest_of_work_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_rest_of_work_week])
        
    def generate_new_rest_of_weekend(self):
        
        if self.days_left_in_weekend == 0:
            return None
        
        else:
            return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + self.days_left_in_weekend + 1)])
    
    def add_new_rest_of_weekend(self):
        
        if self.days_until_today > 0:
            self.add_new_days_until_today()
            
        new_rest_of_weekend = self.generate_new_rest_of_weekend()
        
        if new_rest_of_weekend is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_rest_of_weekend])
    
    def generate_new_week(self):
        
        if self.days_until_next_week != 1:
            warnings.warn(message = "The last schedule day is not Sunday, so you cannot generate a full week.")
            return None
        
        else:
            return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + 8)])
    
    def add_new_week(self):
        
        new_week = self.generate_new_week()
            
        if new_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_week])            
        
    def generate_new_work_week(self):
        
        if self.days_until_next_work_week != 1:
            warnings.warn(message = "The last schedule day is not Sunday, so you cannot generate a full work week.")
            return None
        
        else:
            return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + 6)])
        
    def add_new_work_week(self):
        
        new_work_week = self.generate_new_work_week()
            
        if new_work_week is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_work_week])
        
    def generate_new_weekend(self):
        
        if self.days_until_next_weekend != 1:
            warnings.warn(message = "The last schedule day is not Friday, so you cannot generate a full work week.")
            return None
        
        else:
            return pd.concat([self.generate_new_day(days_from_today = i) for i in range(-1 * self.days_until_today + 1, -1 * self.days_until_today + 3)])
        
    def add_new_weekend(self):
        
        new_weekend = self.generate_new_weekend()
            
        if new_weekend is not None:
            self._day_schedules = pd.concat([self.day_schedules, new_weekend])
    
    def remove_day(self):
        
        if self.day_schedules is None:
            warnings.warn(message = "There is no schedule to remove days from.")
        
        elif self.day_schedules.shape[0] == 1:
            self.day_schedules = None
            
        else:
            self._day_schedules = self.day_schedules[:-1]
        
    def remove_days(self, number_of_days):
        
        if self.day_schedules is None:
            warnings.warn(message = "There is no schedule to remove days from.")
            
        elif self.day_schedules.shape[0] < number_of_days:
            warnings.warn(message = "The number of days input, to remove from the schedule, is more than the number of days currently in the schedule.")
            
        else:
            self._day_schedules = self.day_schedules[:(-1 * number_of_days)]
    
    def remove_hanging_work_week(self):
    
    def remove_work_week(self):
        
    def remove_hanging_weekend(self):
    
    def remove_weekend(self):
        
    def remove_hanging_week(self):    
    
    def remove_week(self):
        
        