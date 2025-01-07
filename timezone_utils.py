# timezone_utils.py
import pytz
from datetime import datetime, timedelta

def get_current_est_time():
    """Get current time in EST."""
    est_tz = pytz.timezone('America/New_York')
    return datetime.now(est_tz)

def get_common_timezones():
    """Get list of most commonly used timezones."""
    common_timezones = [
        'America/New_York',    # EST/EDT
        'America/Los_Angeles', # PST/PDT
        'Europe/London',       # GMT/BST
        'Europe/Paris',        # CET/CEST
        'Asia/Tokyo'          # JST
    ]
    return common_timezones

def get_timezone_display_name(tz_name):
    """Convert timezone name to display name."""
    display_names = {
        'America/New_York': 'New York (EST)',
        'America/Los_Angeles': 'Los Angeles (PST)',
        'Europe/London': 'London (GMT)',
        'Europe/Paris': 'Paris (CET)',
        'Asia/Tokyo': 'Tokyo (JST)'
    }
    return display_names.get(tz_name, tz_name)

def validate_time_input(hours, minutes):
    """Validate time input values."""
    if not (0 <= hours <= 23):
        raise ValueError("Hours must be between 0 and 23")
    if not (0 <= minutes <= 59):
        raise ValueError("Minutes must be between 0 and 59")
    return True

def create_datetime_from_components(date, hours, minutes, timezone='America/New_York'):
    """Create timezone-aware datetime from components."""
    try:
        validate_time_input(hours, minutes)
        time_str = f"{hours:02d}:{minutes:02d}"
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        naive_dt = datetime.combine(date, time_obj)
        
        try:
            tz = pytz.timezone(timezone)
            return tz.localize(naive_dt), None
        except pytz.exceptions.UnknownTimeZoneError:
            return None, f"Invalid timezone: {timezone}"
            
    except ValueError as e:
        return None, f"Invalid time components: {str(e)}"

def get_top5_timezone_times(est_datetime):
    """Get time in top 5 major timezones based on EST time."""
    try:
        # Ensure EST datetime is timezone-aware
        est_tz = pytz.timezone('America/New_York')
        if est_datetime.tzinfo is None:
            est_datetime = est_tz.localize(est_datetime)
        
        timezone_info = []
        
        for tz_name in get_common_timezones():
            try:
                target_tz = pytz.timezone(tz_name)
                converted_time = est_datetime.astimezone(target_tz)
                
                # Get UTC offset
                utc_offset = converted_time.utcoffset().total_seconds() / 3600
                
                # Get region/city
                city = get_timezone_display_name(tz_name)
                
                # Get time difference from EST
                time_diff = utc_offset - est_datetime.utcoffset().total_seconds() / 3600
                
                timezone_info.append({
                    'timezone': tz_name,
                    'city': city,
                    'local_time': converted_time,
                    'utc_offset': utc_offset,
                    'time_diff': time_diff
                })
                
            except Exception:
                continue
        
        return timezone_info, None
    except Exception as e:
        return None, str(e)