import pytz
from datetime import datetime
import pandas as pd

def get_common_timezones():
    """Get list of most commonly used timezones."""
    common_timezones = [
        'America/New_York',    # EST/EDT
        'America/Los_Angeles', # PST/PDT
        'Europe/London',       # GMT/BST
        'Europe/Paris',        # CET/CEST
        'Asia/Tokyo',          # JST
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

def convert_timezone(source_datetime, source_tz, target_tz):
    """Convert datetime from source timezone to target timezone."""
    try:
        source_timezone = pytz.timezone(source_tz)
        target_timezone = pytz.timezone(target_tz)
        source_datetime_with_tz = source_timezone.localize(source_datetime)
        target_datetime = source_datetime_with_tz.astimezone(target_timezone)
        return target_datetime, None
    except Exception as e:
        return None, str(e)

def get_top5_timezone_times(est_datetime):
    """
    Get current time in top 5 major timezones based on EST time.
    Returns a list of timezone information and converted times.
    """
    try:
        est_tz = pytz.timezone('America/New_York')
        est_datetime_aware = est_tz.localize(est_datetime)
        
        timezone_info = []
        
        for tz_name in get_common_timezones():
            try:
                target_tz = pytz.timezone(tz_name)
                converted_time = est_datetime_aware.astimezone(target_tz)
                
                # Get UTC offset
                utc_offset = converted_time.utcoffset().total_seconds() / 3600
                
                # Get region/city
                city = get_timezone_display_name(tz_name)
                
                # Get time difference from EST
                time_diff = utc_offset - est_datetime_aware.utcoffset().total_seconds() / 3600
                
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