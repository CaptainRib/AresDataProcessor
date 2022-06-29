import datetime, pytz
import pandas as pd
import iso8601
import rfc3339



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

def get_datetime_from_timestamp(timestamp):
    # Timestamp has to be in ms
    dt = pd.to_datetime(timestamp, unit='ms', utc=True).to_pydatetime()
    nytz_dt = dt.astimezone(pytz.timezone(NY_TZ))
    return nytz_dt.isoformat()

def get_microseconds_from_datetime(datetime_str):
    return get_millisecs_from_datetime(datetime_str) * 1000

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
    '''Given a timespan and multipler, return timespan in milliseconds

    Args:
        aggregate_timespan (str): timespan
        multipler (int): multipler

    Returns:
        int: timespan in milliseconds
    '''
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

def split_timespan(from_: str, to: str, divisor: int):
    start = get_millisecs_from_datetime(from_)
    end = get_millisecs_from_datetime(to)
    diff = calculate_time_diff(start, end)
    interval = diff // divisor
    time_paritions = [start]
    for _ in range(divisor):
        start += interval
        time_paritions.append(start)
    return _construct_time_range_pair_from_partition(time_paritions) 

def _construct_time_range_pair_from_partition(partition: list):
    partition_dt = [get_datetime_from_timestamp(timestamp) for timestamp in partition]
    result = list(zip(partition_dt[:-1], partition_dt[1:]))
    return result