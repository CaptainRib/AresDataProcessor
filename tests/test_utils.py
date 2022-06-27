import pytest

from aresdataprocessor.utils import time_utils


class TestTimeUtils:
    def test_get_millisecs_from_date(self):
        result = time_utils.get_millisecs_from_datetime('2022-06-20T19:18:07-08:00')
        assert result == 1655781487000
    
    def test_get_millisecs_from_date_wrong_date_format(self):
        with pytest.raises(Exception) as result:
            time_utils.get_millisecs_from_datetime('202')
            
    