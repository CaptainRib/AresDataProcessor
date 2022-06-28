from numpy import int64
from polygon import RESTClient
from aresdataprocessor.config import creds
from aresdataprocessor.utils import time_utils
from polygon.exceptions import NoResultsError
from aresdataprocessor.exceptions.exceptions import InternalError, InvalidInputException, EmptyResultException


class PolygonDataAccesssor():
    def __init__(self):
        self.client = RESTClient(creds.POLYGON_API_KEY)
    
    def get_aggregated_bars(self,
                            ticker: str,
                            aggregate_timespan: str,
                            multiplier: int,
                            from_: int,
                            to: int):
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
            bars = self.client.get_aggs(ticker=ticker,
                                        multiplier=multiplier,
                                        timespan=aggregate_timespan,
                                        from_=from_,
                                        to=to)
        except NoResultsError:
            raise EmptyResultException('Unable to find the corresponding result data')
        except:
            raise InternalError('Unexpected error happened')
        return bars
    
    def list_trades(self, ticker: str, trade_timestamp_gte: str, trade_timestamp_lte: str, limit: int=50000):
        '''_summary_

        Args:
            ticker (str): Ticker must be in all upper case
            trade_timestamp_lte (str): The start time of the query time range, inclusive
            trade_timestamp_gte (str): The end time of the query time range, inclusive
            limit (int, optional): Number of results to return in each call. Defaults to 50000.
        Returns:
            generator: A generator for trades 
        '''
        self._validate_list_trades(ticker, trade_timestamp_gte, trade_timestamp_lte, limit)
        result = self.client.list_trades(ticker, timestamp_gte=trade_timestamp_gte, timestamp_lte=trade_timestamp_lte, limit=limit)
        return result 

    def _validate_list_trades(self, ticker: str, trade_timestamp_gte: str, trade_timestamp_lte: str, limit: int=50000):
        if not self._validate_ticker(ticker):
            raise InvalidInputException('Ticker is not all upper case')

        if time_utils.compare_time(trade_timestamp_gte, trade_timestamp_lte):
            raise InvalidInputException('The query start time must be before end time')
        
        if limit <= 0 or limit > 50000:
            raise InvalidInputException('The limit is out of range')
    
    def _validate_ticker(self, ticker: str) -> bool:
        return ticker.isupper()