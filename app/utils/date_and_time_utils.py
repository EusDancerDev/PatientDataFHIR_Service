#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from datetime import datetime, timedelta, timezone
import time

# Try to import `pytz` and set a flag for availability
try:
    import pytz
    pytz_installed = True
except ImportError:
    pytz_installed = False

#------------------------#
# Import project modules #
#------------------------#

from app.utils.time_formatters import dt_to_string

#------------------#
# Define functions #
#------------------#

# Display and Conversion Utilities #
#----------------------------------#

def display_user_timestamp(user_timestamp, user_timezone_str):
    """
    Converts a UTC timestamp to the user's local timezone and formats it for display.
    
    Parameters
    ----------
    user_timestamp : datetime.datetime or str
        The timestamp to be converted. If a string, it should be in ISO format (e.g., "2023-01-01T12:00:00Z").
        The function assumes `user_timestamp` is in UTC if naive (no timezone).
        
    user_timezone_str : str
        The IANA timezone name (e.g., "America/New_York", "Europe/London") for the target timezone.

    Returns
    -------
    datetime.datetime or str
        The timestamp converted to the specified timezone.
        Returns as a `datetime` object if conversion is successful; otherwise, as a string with error details.

    Notes
    -----
    - If the `pytz` library is available, it is used for timezone conversion, providing extensive IANA timezone support.
    - If `pytz` is unavailable, the function defaults to using `datetime`'s built-in `astimezone()` mechanism, but limited to standard UTC offset conversions.
    
    Example
    -------
    >>> display_user_timestamp(datetime.now(timezone.utc), "America/New_York")
    datetime.datetime(2023, 1, 1, 7, 0, tzinfo=<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)
    
    >>> display_user_timestamp("2023-01-01T12:00:00Z", "Europe/London")
    datetime.datetime(2023, 1, 1, 12, 0, tzinfo=<DstTzInfo 'Europe/London' GMT0:00:00 STD>)
    """
    # Ensure user_timestamp is a datetime object in UTC
    if isinstance(user_timestamp, str):
        try:
            user_timestamp = datetime.fromisoformat(user_timestamp.replace("Z", "+00:00"))
        except ValueError:
            return "Invalid timestamp format. Expected ISO format (e.g., '2023-01-01T12:00:00Z')."
    elif not isinstance(user_timestamp, datetime):
        return "Invalid timestamp type. Expected `datetime` or ISO format string."
    
    if user_timestamp.tzinfo is None:
        user_timestamp = user_timestamp.replace(tzinfo=timezone.utc)

    # Convert timestamp using pytz if available, or fallback otherwise
    try:
        if pytz_installed:
            try:
                user_timezone = pytz.timezone(user_timezone_str)
            except pytz.UnknownTimeZoneError:
                raise ValueError(f"Invalid timezone: {user_timezone_str}")
            localized_timestamp = user_timestamp.astimezone(user_timezone)
        else:
            offset_hours = int(user_timezone_str.split("UTC")[-1].split(":")[0])
            offset_minutes = int(user_timezone_str.split(":")[1]) if ":" in user_timezone_str else 0
            offset = timedelta(hours=offset_hours, minutes=offset_minutes)
            localized_timestamp = user_timestamp.astimezone(timezone(offset))
            
    except Exception as e:
        raise RuntimeError(f"Error converting timestamp: {e}")

    return localized_timestamp

        
# General-scale dates and times #
#-------------------------------#

def get_current_datetime(time_fmt_str=None, tz_arg=None):    
    """
    Returns the current date and time as a datetime.datetime object or its string representation.

    Parameters
    ----------
    time_fmt_str : str, optional
        Optional format string for datetime formatting using the external `dt_to_string` function.
        Default is None.
    tz_arg : timezone or str, optional
        Optional timezone object or string for specifying the timezone.
        If a string is provided, it will be converted to a timezone using pytz.

    Returns
    -------
    current_time : str or datetime.datetime
        Current date and time object based on the dtype.
        If 'time_fmt_str' is provided, returns a formatted string representation.
    """
    # Handle timezone argument
    if tz_arg is None:
        tz = None
    
    elif isinstance(tz_arg, str):
        if pytz_installed:
            try:
                tz_arg = pytz.timezone(tz_arg)
            except pytz.UnknownTimeZoneError:
                raise ValueError(f"Invalid timezone: {tz_arg}")
        else:
            raise ValueError("'pytz' library is required for string timezone arguments.")
    elif isinstance(tz_arg, int):
        tz = timezone(timedelta(hours=tz_arg))
    elif isinstance(tz_arg, timezone):
        tz = tz_arg
    else:
        raise TypeError("'tz_arg' must be a timezone object, string, or integer for UTC offset.")
    
    # Get the current date and time with the specified timezone
    current_time = datetime.now(tz=tz_arg)
    
    # Format the object based on 'time_fmt_str' variable, if provided
    if time_fmt_str is not None:
        current_time = dt_to_string(current_time, dt_fmt_str=time_fmt_str)
    
    return current_time


# Nanoscale datetimes #
#---------------------#

def get_nano_datetime(t=None):
    """
    Get the current or specified time in nanoseconds, formatted as a datetime string.
    
    Parameters
    ----------
    t : int, float, or None, optional
        Time value in nanoseconds. If None, the current time is used.

    Returns
    -------
    nano_dt_str : str
        The formatted datetime string with nanoseconds.
    """
    if t is not None and not isinstance(t, (float, int)):
        raise TypeError("Time value must either be integer or float.")
    
    # Use current time if none is provided
    if t is None:
        t = time.time_ns()  # Get current time in nanoseconds
    
    # Ensure we handle floating-point times by converting to int
    if isinstance(t, float):
        t = int(str(t).replace(".", ""))
        
    floated_nanotime_str = _nano_floated_time_str(t)
    nano_dt_str = _convert_floated_time_to_datetime(floated_nanotime_str)
    return nano_dt_str


def _convert_floated_time_to_datetime(floated_time):
    """
    Convert a floated time value to a datetime object with nanosecond precision.

    Parameters
    ----------
    floated_time : float or int
        The floated time value to be converted.

    Returns
    -------
    nano_dt_str : str
        The formatted datetime string with nanoseconds.
    """
    # Convert to float if input is a string
    if isinstance(floated_time, str):
        floated_time = float(floated_time)
        
    # Split into seconds and nanoseconds
    seconds = int(floated_time)
    nanoseconds = int((floated_time - seconds) * 1_000_000_000)

    # Convert the seconds part into a datetime object
    dt = datetime.fromtimestamp(floated_time)
    
    # Add the nanoseconds part and return the formatted string
    dt_with_nanos = dt + timedelta(microseconds=nanoseconds / 1_000)
    dt_with_nanos_str = dt_to_string(dt_with_nanos, dt_fmt_str="%Y-%m-%dT%H:%M:%S")
    nano_dt_str = f"{dt_with_nanos_str}.{nanoseconds:09d}"
    return nano_dt_str


def _nano_floated_time_str(time_ns):
    """
    Convert a time value in nanoseconds to a formatted floating-point time string.

    Parameters
    ----------
    time_ns : int
        Time value in nanoseconds.

    Returns
    -------
    str
        The floating-point time string with nanosecond precision.
    """
    # Convert nanoseconds to seconds and nanoseconds parts
    seconds = time_ns // 1_000_000_000
    nanoseconds = time_ns % 1_000_000_000

    # Format the floating-point time with nanosecond precision
    return f"{seconds}.{nanoseconds:09d}"


#--------------------------#
# Parameters and constants #
#--------------------------#

# Option lists #
DT_DTYPE_OPTIONS = ["datetime", "str"]

# Dictionary mapping current time provider methods to the corresponding methods
CURRENT_DATETIME_DICT = {
    DT_DTYPE_OPTIONS[0] : lambda tz_arg: datetime.datetime.now(tz_arg),
    DT_DTYPE_OPTIONS[1] : lambda tz_arg: time.ctime(tz_arg)
}
