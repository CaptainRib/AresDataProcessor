from numpy import int64
from polygon import RESTClient
from aresdataprocessor.config import creds
from aresdataprocessor.utils import time_utils
from polygon.exceptions import NoResultsError
from aresdataprocessor.data_access.exceptions import InvalidInputException, EmptyResultException


class PolygonDataAccesssor():
    def __init__(self):
        self.client = RESTClient(creds.POLYGON_API_KEY)
    
    def get_aggregated_bars(self,
                            ticker: str,
                            aggregate_timespan: str,
                            multipler: int,
                            from_: str,
                            to: str):
        '''Get aggregated bar

        Args:
            ticker (str): Stock ticker in all UPPER CASE
            aggreate_timespan (str): Supported strings are minute|hour|day|week|month|quarter|year
            multipler (int): Has to be integer
            from_ (str): RFC3339 datetime format including timezone info. Ex: 2022-06-20T19:18:07-08:00
            to (str): RFC3339 datetime format including timezone info. Ex: 2022-06-20T19:18:07-08:00

        Returns:
            _type_: Return the aggregated bar information
        '''
        try:
            start_time, end_time = self._validate_get_aggregated_bar_input(
                ticker,
                aggregate_timespan,
                multipler,
                from_,
                to)
        
            bars = self.client.get_aggs(ticker=ticker,
                                        multiplier=multipler,
                                        timespan=aggregate_timespan,
                                        from_=start_time,
                                        to=end_time)
        except NoResultsError:
            raise EmptyResultException('Unable to find the corresponding result data')
        except:
            raise
        return bars

    
    def list_trades(self, ticker: str, trade_timestamp_gte: str, trade_timestamp_lte: str, limit: int=50000):
        '''_summary_

        Args:
            ticker (str): Ticker must be in all upper case
            trade_timestamp_lte (str): The start time of the query time range, inclusive
            trade_timestamp_gte (str): The end time of the query time range, inclusive
            limit (int, optional): Number of results to return in each call. Defaults to 50000.
        '''
        result = self.client.list_trades(ticker, timestamp_gte=trade_timestamp_gte, timestamp_lte=trade_timestamp_lte, limit=limit)
        count = 0
        for _ in result:
            count += 1
        print(count)
        
        
    def _validate_get_aggregated_bar_input(self,
                                           ticker: str,
                                           aggregate_timespan: str,
                                           multipler: int,
                                           from_: str,
                                           to: str):
        if not ticker.isupper():
            raise InvalidInputException('Ticker is not all upper case')
        
        if aggregate_timespan not in ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']:
            raise InvalidInputException('Timespan is not one of the valid')
        
        try:
            start_time = time_utils.get_millisecs_from_datetime(from_)
            end_time = time_utils.get_millisecs_from_datetime(to)
        except:
            raise InvalidInputException('Time is not in valid format')
        
        time_diff = time_utils.calculate_time_diff(start_time, end_time)
        
        queried_timespan_in_millsecs = time_utils.calculate_timespan(aggregate_timespan, multipler)

        if time_diff != queried_timespan_in_millsecs:
            raise InvalidInputException('The input timespan does not match the start and end time')
        
        return start_time, end_time
