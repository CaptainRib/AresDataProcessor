from aresdataprocessor.data_access.polygon.data_accessor import PolygonDataAccesssor
from aresdataprocessor.exceptions.exceptions import InvalidInputException
import pytest

class TestGetAggregatedBars:
    def test_success_case(self):
        data_accessor = PolygonDataAccesssor()
        data_accessor.get_aggregated_bars('AAPL', 'minute', 1, 1655818260000, 1655818260000)

class TestListTrades:
    def test_success_case(self):
        data_accessor = PolygonDataAccesssor()
        data_accessor.list_trades('AAPL', '2022-06-20T09:31:00-04:00', '2022-06-20T09:31:02-04:00')
