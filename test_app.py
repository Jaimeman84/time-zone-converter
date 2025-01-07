# test_timezone_utils.py
import pytest
from datetime import datetime, date
import pytz
from timezone_utils import (
    get_current_est_time,
    get_common_timezones,
    get_timezone_display_name,
    validate_time_input,
    create_datetime_from_components,
    get_top5_timezone_times
)

class TestTimeZoneConverter:
    def test_get_current_est_time(self):
        """Test that current EST time is returned with correct timezone."""
        current_time = get_current_est_time()
        assert current_time.tzinfo is not None
        assert 'America/New_York' in str(current_time.tzinfo)

    def test_get_common_timezones(self):
        """Test that common timezones list contains expected zones."""
        timezones = get_common_timezones()
        assert len(timezones) == 5
        assert "America/New_York" in timezones
        assert "Europe/London" in timezones
        assert "Asia/Tokyo" in timezones

    def test_timezone_display_names(self):
        """Test timezone display name conversion."""
        assert get_timezone_display_name("America/New_York") == "New York (EST)"
        assert get_timezone_display_name("Europe/London") == "London (GMT)"
        assert get_timezone_display_name("Unknown/Zone") == "Unknown/Zone"

    def test_validate_time_input_valid(self):
        """Test time input validation with valid values."""
        assert validate_time_input(0, 0) is True
        assert validate_time_input(23, 59) is True
        assert validate_time_input(12, 30) is True

    def test_validate_time_input_invalid_hours(self):
        """Test time input validation with invalid hours."""
        with pytest.raises(ValueError):
            validate_time_input(24, 0)
        with pytest.raises(ValueError):
            validate_time_input(-1, 0)

    def test_validate_time_input_invalid_minutes(self):
        """Test time input validation with invalid minutes."""
        with pytest.raises(ValueError):
            validate_time_input(0, 60)
        with pytest.raises(ValueError):
            validate_time_input(0, -1)

    def test_create_datetime_from_components(self):
        """Test datetime creation from components."""
        test_date = date(2024, 1, 1)
        result, error = create_datetime_from_components(test_date, 12, 30)
        
        assert error is None
        assert result.hour == 12
        assert result.minute == 30
        assert result.tzinfo is not None
        assert 'America/New_York' in str(result.tzinfo)

    def test_create_datetime_invalid_components(self):
        """Test datetime creation with invalid components."""
        test_date = date(2024, 1, 1)
        result, error = create_datetime_from_components(test_date, 24, 0)
        assert result is None
        assert "Invalid time components" in error

    def test_get_top5_timezone_times(self):
        """Test conversion to top 5 timezones."""
        est_time = datetime(2024, 1, 1, 12, 0)
        est_tz = pytz.timezone('America/New_York')
        est_time = est_tz.localize(est_time)
        
        timezone_info, error = get_top5_timezone_times(est_time)
        
        assert error is None
        assert len(timezone_info) == 5
        
        # Check structure of each timezone info
        for tz_info in timezone_info:
            assert all(key in tz_info for key in [
                'timezone',
                'city',
                'local_time',
                'utc_offset',
                'time_diff'
            ])
            assert isinstance(tz_info['local_time'], datetime)
            assert tz_info['local_time'].tzinfo is not None

    def test_get_top5_timezone_times_dst(self):
        """Test timezone conversions during DST."""
        # Test during DST (summer time)
        dst_time = datetime(2024, 7, 1, 12, 0)
        est_tz = pytz.timezone('America/New_York')
        dst_time = est_tz.localize(dst_time)
        
        timezone_info, error = get_top5_timezone_times(dst_time)
        
        assert error is None
        assert len(timezone_info) == 5
        
        # Verify DST offsets are correct
        for tz_info in timezone_info:
            if tz_info['timezone'] == 'America/New_York':
                assert abs(tz_info['utc_offset'] - (-4)) < 0.1  # EDT is UTC-4
            elif tz_info['timezone'] == 'Europe/London':
                assert abs(tz_info['utc_offset'] - 1) < 0.1  # BST is UTC+1

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with naive datetime
        naive_time = datetime.now()
        timezone_info, error = get_top5_timezone_times(naive_time)
        assert error is None  # Should handle naive datetime by localizing it
        
        # Test with invalid timezone
        result, error = create_datetime_from_components(date(2024, 1, 1), 12, 0, "Invalid/Timezone")
        assert result is None
        assert "Invalid timezone" in error