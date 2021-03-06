from enum import Enum


class AggregateTimespan(Enum):
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    YEAR = 'year'

TIME_SPLIT_DIVISOR = 10