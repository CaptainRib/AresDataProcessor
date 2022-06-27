import datetime, pytz
import pandas as pd
import iso8601


EASTERN_TIME = 'US/Eastern'
NY_TZ = 'America/New_York'

def get_current_time_isoformat_without_ms():
    nyc_datetime = datetime.datetime.now(pytz.timezone(EASTERN_TIME)).strftime('%Y-%m-%d %H:%M:%S')
    nyc_datetime_isoformat = pd.Timestamp(nyc_datetime, tz='America/New_York').isoformat()
    return nyc_datetime_isoformat

def get_current_time_isoformat_wihout_ms_minus_x_minutes(minus):
    nyc_datetime_minus_x = (datetime.datetime.now(pytz.timezone(EASTERN_TIME)) - datetime.timedelta(minutes=minus)).strftime('%Y-%m-%d %H:%M:%S')
    nyc_datetime_minus_x_isoformat = pd.Timestamp(nyc_datetime_minus_x, tz='America/New_York').isoformat()
    return nyc_datetime_minus_x_isoformat

def get_millisecs_from_datetime(datetime_str):
    datetime_obj = iso8601.parse_date(datetime_str)
    nytz_datetime = datetime_obj.astimezone(pytz.timezone(NY_TZ))
    return int(nytz_datetime.timestamp() * 1000)

def get_nanosecs_from_datetime(datetime_str):
    return get_millisecs_from_datetime(datetime_str) * 1000000

def calculate_time_diff(from_, to):
    '''Calculate the time difference between milliseconds

    Args:
        from_ (int): The start timestamp
        to (int): The end timestamp

    Returns:
        int: The difference between from_ and to
    '''
    return to - from_

def calculate_timespan(aggregate_timespan, multipler):
    time_in_seconds = 0
    if aggregate_timespan == 'minute':
        time_in_seconds = 60
    
    if aggregate_timespan == 'hour':
        time_in_seconds = 60 * 60
    
    if aggregate_timespan == 'day':
        time_in_seconds = 60 * 60 * 24
    
    if aggregate_timespan == 'week':
        time_in_seconds = 60 * 60 * 24 * 7
    
    if aggregate_timespan == 'month':
        time_in_seconds = 60 * 60 * 24 * 7 * 30  # Not sure about this yet
        
    if aggregate_timespan == 'quarter':
        time_in_seconds = 60 * 60 * 24 * 7 * 30 * 3
    
    if aggregate_timespan == 'year':
        time_in_seconds = 60 * 60 * 24 * 365  # Not sure about this yet
    
    return time_in_seconds * multipler * 1000

def compare_time(time1, time2):
    '''Compare two time objects

    Args:
        time1 (str): First time
        time2 (str): Second time

    Returns:
        return true if time1 > time2, else return false
    '''
    return get_millisecs_from_datetime(time1) > get_millisecs_from_datetime(time2)