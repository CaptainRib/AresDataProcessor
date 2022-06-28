from aresdataprocessor.data_access.polygon import data_accessor
from aresdataprocessor.utils import time_utils
from aresdataprocessor.exceptions.exceptions import InvalidInputException

DEFAULT_TRADE_LIMIT = 50000  # Move it to somewhere else

class Orchestrator():
    def __init__(self):
        self.da = data_accessor.PolygonDataAccesssor()
    
    def get_bars(self, ticker: str, aggregate_timespan: str, multiplier: int, from_: str, to: str):
        self._validate_get_bars_input(ticker, aggregate_timespan, multiplier, from_, to)
        result = self.da.get_aggregated_bars(ticker,
                                    aggregate_timespan,
                                    multiplier,
                                    time_utils.get_millisecs_from_datetime(from_),
                                    time_utils.get_millisecs_from_datetime(to))
        return result
    
    def list_trades(self, ticker: str, trade_timestamp_gte: str, trade_timestamp_lte: str):
        self._validate_list_trades(ticker, trade_timestamp_gte, trade_timestamp_lte, DEFAULT_TRADE_LIMIT)
    
    def _validate_get_bars_input(self,
                                ticker: str,
                                aggregate_timespan: str,
                                multipler: int,
                                from_: str,
                                to: str):
        if not self._validate_ticker(ticker):
            raise InvalidInputException('Ticker is not all upper case')
        
        if aggregate_timespan not in ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']:
            raise InvalidInputException('Timespan is not one of the valid')
        
        try:
            start_time = time_utils.get_millisecs_from_datetime(from_)
            end_time = time_utils.get_millisecs_from_datetime(to)
        except:
            raise InvalidInputException('Time is not in valid format')
        
        if start_time >= end_time:
            raise InvalidInputException('Start time must be before end time')
        
        time_diff = time_utils.calculate_time_diff(start_time, end_time)
        
        queried_timespan_in_millsecs = time_utils.calculate_timespan(aggregate_timespan, multipler)

        if time_diff != queried_timespan_in_millsecs:
            raise InvalidInputException('The input timespan does not match the start and end time')
        
        return start_time, end_time
    
    def _validate_list_trades(self, ticker: str, trade_timestamp_gte: str, trade_timestamp_lte: str, limit: int=50000):
        if not self._validate_ticker(ticker):
            raise InvalidInputException('Ticker is not all upper case')

        if time_utils.compare_time(trade_timestamp_gte, trade_timestamp_lte):
            raise InvalidInputException('The query start time must be smaller than end time')
        
        if limit <= 0 or limit > 50000:
            raise InvalidInputException('The limit is out of range')

    def _validate_ticker(self, ticker: str) -> bool:
        return ticker.isupper()
    