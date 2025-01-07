# test_app.py
import pytest
from datetime import datetime
from timezone_utils import get_top5_timezone_times, get_common_timezones, get_timezone_display_name

class TestTimeZoneConverter:
    def test_common_timezones_list(self):
        """Test that common timezones list contains expected zones."""
        timezones = get_common_timezones()
        assert len(timezones) == 5
        assert "America/New_York" in timezones
        assert "Europe/London" in timezones
        
    def test_timezone_display_names(self):
        """Test timezone display name conversion."""
        assert get_timezone_display_name("America/New_York") == "New York (EST)"
        assert get_timezone_display_name("Europe/London") == "London (GMT)"
        
    def test_top5_timezone_conversion(self):
        """Test conversion to top 5 timezones."""
        est_time = datetime(2024, 1, 1, 12, 0)
        timezone_info, error = get_top5_timezone_times(est_time)
        
        assert error is None
        assert timezone_info is not None
        assert len(timezone_info) == 5
        
        # Check structure of returned data
        for tz_info in timezone_info:
            assert 'timezone' in tz_info
            assert 'city' in tz_info
            assert 'local_time' in tz_info
            assert 'utc_offset' in tz_info
            assert 'time_diff' in tz_info
            
    def test_time_differences(self):
        """Test that time differences are calculated correctly."""
        est_time = datetime(2024, 1, 1, 12, 0)
        timezone_info, error = get_top5_timezone_times(est_time)
        
        for tz_info in timezone_info:
            if tz_info['timezone'] == 'America/New_York':
                assert tz_info['time_diff'] == 0
            elif tz_info['timezone'] == 'America/Los_Angeles':
                assert tz_info['time_diff'] == -3  # PST is 3 hours behind EST
                
    def test_dst_handling(self):
        """Test handling of daylight saving time."""
        # Test during DST period
        dst_time = datetime(2024, 7, 1, 12, 0)
        timezone_info, error = get_top5_timezone_times(dst_time)
        
        assert error is None
        assert timezone_info is not None
        
        # Test during non-DST period
        non_dst_time = datetime(2024, 1, 1, 12, 0)
        timezone_info, error = get_top5_timezone_times(non_dst_time)
        
        assert error is None
        assert timezone_info is not None