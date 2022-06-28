import pytest

from aresdataprocessor.utils import time_utils


class TestTimeUtils:
    def test_get_millisecs_from_date(self):
        result = time_utils.get_millisecs_from_datetime('2022-06-20T19:18:07-08:00')
        assert result == 1655781487000
    
    def test_get_millisecs_from_date_wrong_date_format(self):
        with pytest.raises(Exception) as result:
            time_utils.get_millisecs_from_datetime('202')
            
    def test_get_nanosecs_from_datetime(self):
        result = time_utils.get_nanosecs_from_datetime('2022-06-20T19:18:07-08:00')
        assert result == 1655781487000000000
    
    def test_calculate_time_diff(self):
        result = time_utils.calculate_time_diff(1655781487000, 1655781488000)
        assert result == 1000
    
    def test_calculate_timespan(self):
        result1 = time_utils.calculate_timespan('minute', 1)
        result2 = time_utils.calculate_timespan('minute', 4)
        result3 = time_utils.calculate_timespan('day', 10)
        result4 = time_utils.calculate_timespan('hour', 1)
        assert result1 == 60000
        assert result2 == 240000
        assert result3 == 864000000
        assert result4 == 3600000
    