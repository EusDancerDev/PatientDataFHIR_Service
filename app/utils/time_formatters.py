#----------------#
# Import modules #
#----------------#

from datetime import datetime
from dateutil import parser
import time

# Import project modules #
#------------------------#

from app.config import PANDAS_DATE_UNIT_LIST, NUMPY_DATE_UNIT_LIST

#------------------#
# Define functions #
#------------------#

# Input validation streamliners #
#-------------------------------#

def _validate_option(explanation, option, allowed_options):
    """
    Validate if the given option is within the list of allowed options.

    Parameters
    ----------
    explanation : str
        A brief description or context of the validation.
    option : object
        The option to be validated.
    allowed_options : list/iterable
        A list or iterable of valid options.

    Raises
    ------
    ValueError: 
        If the option is not in the list of allowed options, with a detailed explanation.
    """
    if option not in allowed_options:
        raise ValueError(f"{explanation} '{option}' not supported for this operation. "
                         f"Choose one from {allowed_options}.")
    
    
def _validate_precision(frac_precision, option, min_prec=0, max_prec=6):
    """
    Validate the precision level for a floating-point number and ensure it is within a valid range.
    
    Parameters
    ----------
    frac_precision : int or None
        The desired fractional precision to validate.
    option : str
        Specifies the type of object or library (e.g., "pandas") that supports higher precision.
    min_prec : int, optional
        The minimum allowed precision. Default is 0.
    max_prec : int, optional
        The maximum allowed precision. Default is 9.
    
    Raises
    ------
    ValueError
        If `frac_precision` is outside the range [min_prec, max_prec] or
        `frac_precision` is greater than or equal to 7 but `option` is not "pandas".
    """
    if ((frac_precision is not None) and not (min_prec <= frac_precision <= max_prec)):
        raise ValueError(f"Fractional precision must be between {min_prec} and {max_prec}.")
    if ((7 <= frac_precision <= max_prec) and option != "pandas"):
        raise ValueError(f"Only option 'pandas' supports precision={frac_precision}.")
        
def _validate_unit(unit, module):
    """
    Validates the date unit based on the module.

    Parameters
    ----------
    unit : str
        Time unit for the floated time. 
        Only applicable if the module is 'numpy' or 'pandas'.
    module : {"numpy", "pandas"}
        The module used for parsing the floated time.

    Raises
    ------
    ValueError
        If `unit` is not supported for the specified `module`.
    """
    
    # Define allowed date units for each module    
    if module == "numpy" and unit not in NUMPY_DATE_UNIT_LIST:
        raise ValueError("Unsupported date unit for numpy.datetime64 objects. "
                         f"Choose one from {NUMPY_DATE_UNIT_LIST}.")
        
    if module == "pandas" and unit not in PANDAS_DATE_UNIT_LIST:
        raise ValueError("Unsupported date unit for pandas.Timestamp objects. "
                         f"Choose one from {PANDAS_DATE_UNIT_LIST}.")


def dt_to_string(datetime_obj, dt_fmt_str=None):
    """
    Convert a temporal object to its string representation.
    
    Parameters
    ----------
    datetime_obj : object
        The temporal object to be converted. Can be any object that either:
        - Has a strftime method (e.g., datetime objects)
        - Can be converted to string using str()
    dt_fmt_str : str, optional
        Format string to convert the temporal object to a string.
        Only used if the object has a strftime method.

    Returns
    -------
    str
        The string representation of the temporal object.
        If the object has a strftime method, returns the formatted string.
        Otherwise, returns the string representation using str().
    """

    # Handle individual scalar datetime objects
    if hasattr(datetime_obj, "strftime"):
        return datetime_obj.strftime(dt_fmt_str)

    # Default case
    else:
        return str(datetime_obj)
    
# Simple data parsing #
#---------------------#

# Input format: str #
#~~~~~~~~~~~~~~~~~~~#

def parse_dt_string(datetime_str, dt_fmt_str, module="datetime", unit="ns"):
    """
    Convert a temporal string (time, date, or datetime) to a date/time object using a specified library.
    
    Parameters
    ----------
    datetime_str : str
        A string representing the date and/or time.    
    dt_fmt_str : str
        A format string that defines the structure of `datetime_str`. 
        Must follow the format required by the chosen module.   
    module : {"datetime", "dateutil", "pandas", "numpy", "arrow"}, default 'datetime'
        Specifies the library used for conversion. 
        If 'numpy', datetime_str must be in ISO 8601 date or datetime format.
    unit : str, optional
        Applies only if ``module`` is either 'numpy' or 'pandas'.
        Denotes which unit ``floated_time`` is expressed in.
        
        For Pandas, allowed units are {'D', 's', 'ms', 'us', 'ns'}.
        For NumPy, allowed units are {'Y', 'M', 'D', 'h', 'm', 's' , 'ms', 'us', 'ns'}.
       
        According the standards, this parameter defaults to 'ns' for Pandas 
        and 'us' for NumPy.
        Then, in order to maintain compatibility, the largest common time unit 'us'
        has been defined as default in this function.
    
    Returns
    -------
    datetime_obj : object
        The converted date/time object, as per the chosen module.
    
    Raises
    ------
    ValueError
        - If the module is not supported
        - If no time string is provided or if it does not match the provided format.
    """
    
    # Input validation #
    ####################
    
    # Module #
    allowed_modules = list(TIME_STR_PARSING_DICT.keys())
    _validate_option("Module", module, allowed_modules)
    
    # Formatting string #
    if not dt_fmt_str:
        raise ValueError("A datetime format string must be provided.")
        
    # Time string parsing #
    #######################
    
    try:
        parse_func = TIME_STR_PARSING_DICT.get(module)
        datetime_obj = parse_func(datetime_str, dt_fmt_str, unit) \
                       if module == "pandas"\
                       else parse_func(datetime_str, dt_fmt_str)
    except ValueError:
        raise ValueError("The time string does not match the format string provided.")
    else:
        return datetime_obj
    
# Input format: int, float #
#~~~~~~~~~~~~~~~~~~~~~~~~~~#

def parse_float_dt(datetime_float, 
                   frac_precision=None,
                   origin="unix", 
                   unit="us", 
                   dt_fmt_str=None, 
                   module="datetime"):
    """
    Converts an integer or float time to a date/time object.
    It also converts to a string representation if requested.
    
    datetime_float : int or float
        Time representing a time unit relative to an origin.
    frac_precision : int [0,9] or None 
        Precision of the fractional part of the seconds.
        If not None, this part is rounded to the desired number of decimals,
        which must be between 0 and 9. For decimals in [7,9], nanoscale
        datetime is generated, supported only by 'pandas'.
        Raises a ValueError if 7 <= frac_precision <= 9 and module is not 'pandas'.        
        Defaults to None, i.e., the original precision is used.
    origin : {"arbitrary", "unix"}, default 'unix'
        Determines whether to compute time relative to an arbitrary origin 
        or to the Unix epoch start (1970-01-01 00:00:00).
        For example, the elapsed time for a program to execute has its origin at 
        the moment of execution, whereas for clock times, seconds are counted 
        from the epoch time.
    unit : str, optional
        Applies only if ``origin='unix'`` and ``convert_to={'numpy', 'pandas'}``.
        Denotes which unit ``datetime_str`` is expressed in. 
        
        For Pandas, allowed units are {'D', 's', 'ms', 'us', 'ns'}.
        For NumPy, allowed units are {'Y', 'M', 'D', 'h', 'm', 's', 'ms', 'us', 'ns'}.
        Defaults to 'ns' for Pandas and 'us' for NumPy.
    dt_fmt_str : str
        Format string to convert the date/time object to a string.
    module : {"datetime", "time", "pandas", "numpy", "arrow", "str"}, default 'datetime'.
         The module or class used to parse the floated time. 
         If 'numpy', datetime_float represents an offset from the Unix epoch start.
      
    Returns
    -------
    object
        The converted date/time object or string representation.
    
    Raises
    ------
    ValueError
        If parameters are invalid or the conversion fails.
    """        
    
    # Input validation #
    ####################
    
    # Module #
    allowed_modules = ["str"] + list(FLOATED_TIME_PARSING_DICT.keys())
    _validate_option("Object type conversion", module, allowed_modules)
    
    # Time formatting string #
    if module != "str" and not dt_fmt_str:
        raise ValueError("You must provide a formatting string.")

    # Fractional second precision #
    _validate_precision(frac_precision, module)

    # Date unit #
    _validate_unit(unit, module)

    # Floated time parsing #
    ########################

    if module == "str":
        return _parse_float_to_string(datetime_float,
                                      frac_precision, 
                                      origin,
                                      dt_fmt_str,
                                      unit,
                                      module)
    else:
        return _float_dt_parser(datetime_float, module, unit)
    
    
# Auxiliary functions #
#-#-#-#-#-#-#-#-#-#-#-#

def _parse_float_to_string(floated_time, 
                           frac_precision, 
                           origin, 
                           dt_fmt_str, 
                           unit,
                           module):
    """        
    Converts a floated time to its string representation.

    Parameters
    ----------
    floated_time : int or float
        Time in seconds representing a time unit relative to an origin.
    frac_precision : int [0,9] or None
        Precision of the fractional seconds.
        Only supported by 'pandas' for high precision.
    origin : {"arbitrary", "unix"}
        Origin of the time measurement.
    dt_fmt_str : str
        Format string for the string representation.
    unit : str, optional
        Time unit for `floated_time` if `origin='unix'` and `module` in {'numpy', 'pandas'}.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}
        Module used for parsing.

    Returns
    -------
    str
        The formatted string representation of the floated time.
    """
    
    if origin == "arbitrary":
        return _format_arbitrary_dt(floated_time, frac_precision)
       
    elif origin == "unix":
        # Accommodation of the fractional second #
        if frac_precision is not None:
            dt_seconds = round(floated_time)
            dt_obj = _float_dt_parser(dt_seconds, module, unit)
            dt_str = dt_obj.strftime(dt_fmt_str)
        # Keep the original precision #
        else:
            dt_str = _float_dt_parser(floated_time, module, unit).strftime(dt_fmt_str)
    
        return dt_str  

    
def _float_dt_parser(floated_time, module, unit):
    """
    Parses a floated time into a date/time object.
    
    Parameters
    ----------
    floated_time : int or float
        Time representing a time unit relative to an origin.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}
        Module used for parsing.
    unit : str, optional
        Time unit for `floated_time` if `module` in {'numpy', 'pandas'}.
    
    Returns
    -------
    datetime_obj : object
        The parsed date/time object.
    """
    
    # Input validation #
    ####################
    
    # Module #
    allowed_modules = list(FLOATED_TIME_PARSING_DICT.keys())
    _validate_option("Object type conversion", module, allowed_modules)

    # Date unit #
    _validate_unit(unit, module)
    
    # Calculate datetime object #
    #############################
    
    datetime_obj = FLOATED_TIME_PARSING_DICT.get(module)(floated_time, unit)
    return datetime_obj


def _format_arbitrary_dt(floated_time, frac_precision):
    """
    Formats an arbitrary time into a string representation
    based on the provided format.
    
    Parameters
    ----------
    floated_time : int or float
        Time in seconds representing a time unit relative to an arbitrary origin.
    frac_precision : int [0,6] or None
        Precision of the fractional seconds.
        This parameter is originally set in 'parse_float_dt' function,
        which allows integers in [0,9], because for 6 < frac_precision <=9 
        it performs optional nanoscale time computing, unlike this internal function.
        So in order to maintain organisation, the upper bound for the precision
        will be 6.
    
    Returns
    -------
    str
        The formatted time string.
    
    Raises
    ------
    ValueError
        If the format string is invalid or not supported.
        
    Notes
    -----
    Negative times or hours over 24 represent seconds matching 
    the next day's midnight. If so, set the hour to zero instead of 24.
    """

    # Compute time components #
    days, hours = divmod(floated_time // 3600, 24)
    minutes, seconds = divmod(floated_time % 3600, 60)
    
    # Maintain precisions higher than 6 in the upper bound #
    if frac_precision > 6:
        frac_precision = 6
        
    seconds = round(seconds, frac_precision)
   
    # Format time parts #
    try:
        if days > 0:
            time_tuple = (days, hours, minutes, seconds)
            time_parts_formatted = _TIME_STR_PARTS_TEMPLATES[0].format(*time_tuple)
        elif hours > 0:
            time_tuple = (hours, minutes, seconds)
            time_parts_formatted = _TIME_STR_PARTS_TEMPLATES[1].format(*time_tuple)
        elif minutes > 0:
            time_tuple = (minutes, seconds)
            time_parts_formatted = _TIME_STR_PARTS_TEMPLATES[2].format(*time_tuple)
        else:
            time_tuple = (seconds,)
            time_parts_formatted = _TIME_STR_PARTS_TEMPLATES[3].format(*time_tuple)
    except (KeyError, IndexError, ValueError) as e:
        raise ValueError(f"Invalid format string or time components: {e}")
    return time_parts_formatted 
        

#--------------------------#
# Parameters and constants #
#--------------------------#

# Switch case dictionaries #
#--------------------------#

# Time parsing #
#--------------#

# String #    
#-#-#-#-#-

TIME_STR_PARSING_DICT = {
    "datetime" : lambda datetime_str, dt_fmt_str: datetime.strptime(datetime_str, dt_fmt_str),
    "dateutil" : lambda datetime_str, dt_fmt_str: parser.parse(datetime_str, dt_fmt_str),
}


# Floated #
#-#-#-#-#-#

FLOATED_TIME_PARSING_DICT = {
    "datetime" : lambda floated_time, _ : datetime.fromtimestamp(floated_time),
    "time"     : lambda floated_time : datetime(*tuple(time.localtime(floated_time))[:6]),
}

# Template strings #
#------------------#

_TIME_STR_PARTS_TEMPLATES = [
    "{} days {} hours {} minutes {} seconds",
    "{} hours {} minutes {} seconds",
    "{} minutes {} seconds",
    "{} seconds",
]