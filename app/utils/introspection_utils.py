#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import inspect
import sys

#------------------#
# Define functions # 
#------------------#

# General frame #
#-#-#-#-#-#-#-#-#

def get_func_name(lib="inspect"):
    """
    Retrieves the name of the caller function using the specified library.

    Parameters
    ----------
    lib : str, optional
        Library to use for function name retrieval. Must be one of 'inspect' or 'sys'.
        Defaults to 'inspect'.

    Returns
    -------
    str
        Name of the caller function.

    Raises
    ------
    ValueError
        If `lib` is not a supported library.
    """
    if lib not in NAME_RESOLUTION_LIBRARIES :
        raise ValueError(f"Unsupported library. Choose from {NAME_RESOLUTION_LIBRARIES }.")
    if lib == "inspect":
        return inspect.getframeinfo(inspect.currentframe().f_back).function
    return sys._getframe(1).f_code.co_name


# Function arguments #
#--------------------#

# Caller's frame #
#-#-#-#-#-#-#-#-#-

def get_caller_args():
    """
    Retrieves the required argument names of the caller function.

    Returns
    -------
    list of str
        List of argument names used in the caller function.

    Example
    -------
    >>> def example_func(arg1, arg2): get_caller_args()
    ['arg1', 'arg2']
    """
    caller_frame = inspect.currentframe().f_back
    caller_args, _, _, _ = inspect.getargvalues(caller_frame)
    return list(caller_args)


# Object types #
#--------------#

def get_type_str(obj, lowercase=False):
    """
    Returns the type of an object as a string.

    Parameters
    ----------
    obj : any
        Object whose type is returned as a string.
    lowercase : bool, optional
        If True, returns the type string in lowercase. Defaults to False.

    Returns
    -------
    str
        String representation of the object's type.
    """
    return type(obj).__name__.lower() if lowercase else type(obj).__name__

#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported library list for method name retrievals
NAME_RESOLUTION_LIBRARIES  = ["inspect", "sys"]