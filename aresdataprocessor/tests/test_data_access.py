from aresdataprocessor.data_access.polygon.data_accessor import PolygonDataAccesssor
from aresdataprocessor.data_access.exceptions import InvalidInputException
import pytest

class TestGetAggregatedBars:
    def test_success_case(self):
        data_accessor = PolygonDataAccesssor()
        data_accessor.get_aggregated_bars('AAPL', 'minute', 1, '2022-06-21T09:31:00-04:00', '2022-06-21T09:32:00-04:00')
        
    def test_invalid_ticker(self):
        data_accessor = PolygonDataAccesssor()
        with pytest.raises(InvalidInputException) as result:
            data_accessor.get_aggregated_bars('aapl', 'minute', 1, '1989-01-01T00:18:07-05:00', '1989-01-01T00:18:08-05:00')
            
        assert str(result.value) == 'Ticker is not all upper case'
    
    def test_invliad_timespan(self):
        data_accessor = PolygonDataAccesssor()
        with pytest.raises(InvalidInputException) as result:
            data_accessor.get_aggregated_bars('AAPL', 'min', 1, '1989-01-01T00:18:07-05:00', '1989-01-01T00:18:08-05:00')
        
        assert str(result.value) == 'Timespan is not one of the valid'
        
    def test_invalid_timeformat(self):
        data_accessor = PolygonDataAccesssor()
        with pytest.raises(InvalidInputException) as result:
            data_accessor.get_aggregated_bars('AAPL', 'minute', 1, '1989-01-0', '1989-01-01')
        
        assert str(result.value) == 'Time is not in valid format'
        
    def test_mismatch_timespan(self):
        data_accessor = PolygonDataAccesssor()
        with pytest.raises(InvalidInputException) as result:
            data_accessor.get_aggregated_bars('AAPL', 'minute', 1, '2022-06-21T09:31:00-04:00', '2022-06-21T09:31:59-04:00')
        assert str(result.value) == 'The input timespan does not match the start and end time'