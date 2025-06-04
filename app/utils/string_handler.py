#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import os
from pathlib import Path
from sys import maxsize

from numpy import array, vectorize, char

import re

#------------------------#
# Import project modules #
#------------------------#

from app.utils.introspection_utils import get_type_str, get_caller_args

#------------------#
# Define functions #
#------------------#

# String pattern management #
#---------------------------#

# Main method #
#-#-#-#-#-#-#-#

def find_substring_index(string,
                         substring, 
                         start=0,
                         end=None,
                         return_match_index="lo",
                         return_match_str=False,
                         advanced_search=False,
                         case_sensitive=False,
                         find_whole_words=False,
                         all_matches=False):
    """
    Finds the index and/or matched string for a specified substring within a given string,
    with support for advanced pattern matching.
    
    Parameters
    ----------
    string : str, list, np.ndarray, or tuple
        The input object to search within.
    substring : str or list-like of str
        The substring or list of substrings to search for. Can be a regex pattern.
    start : int, optional
        Start index for search. Default is 0.
    end : int, optional
        End index for search. If None, it searches to the end of the string or collection. 
    return_match_index :  {"lo", "hi", "both"}
        Defines which match index to return.
    return_match_str : bool, optional
        If True, returns the matched substring instead of the index.
    advanced_search : bool, optional
        If True, uses advanced search with support for regex and special options.
    case_sensitive : bool, optional
        Specifies whether the search should be case-sensitive.
        Defaults to False (case-insensitive).
    find_whole_words : bool, optional
        Ensures that only whole words are matched, avoiding partial word matches.
    all_matches : bool, optional
        If True, finds all occurrences of the substring.
        Otherwise, only the first match is returned.
    
    Returns
    -------
    int, list, or str
        Returns the index or the matching substring depending on the arguments passed
    
    Notes
    -----
    This method relies on the internal `_advanced_pattern_searcher` 
    to perform the pattern search, which itself uses `_return_search_obj_spec` 
    for handling regular expression matching and result extraction.
    """
    # Argument validation #
    #######################
    
    param_keys = get_caller_args()
    match_index_pos = param_keys.index("return_match_index")
        
    if not (return_match_index in match_obj_index_option_keys):
        raise ValueError(f"Invalid '{param_keys[match_index_pos]}' value. "
                         f"Choose from {match_obj_index_option_keys}.")
        
    if not (isinstance(return_match_str, bool)):
        raise ValueError("Argument '{param_keys[match_index_str_pos]}' "
                         "must be a boolean.")
    
    # Case studies #
    ################
    
    if (isinstance(string, str) and isinstance(substring, str)):
        if advanced_search:
            substr_match_obj = _advanced_pattern_searcher(string, substring, 
                                                          return_match_index,
                                                          return_match_str,
                                                          case_sensitive,
                                                          find_whole_words,
                                                          all_matches)
        else:
            return string.find(substring)

    
    elif get_type_str(string) in ["list", "ndarray", "tuple"]:
        if isinstance(substring, str):
    
            # Simple search without advanced features
            if not advanced_search:
                if get_type_str(string) == "ndarray":
                    match_indices = char.find(string, substring, start=start, end=end)
                    return [idx for idx in match_indices if idx != -1]
                
                else:
                    if end is None:
                        end = maxsize # Highest defined index for a tuple
                    substr_match_obj = string.index(substring, start, end)
                    
                
            else:
                match_indices = _advanced_pattern_searcher(string, substring,
                                                           return_match_index,
                                                           return_match_str,
                                                           case_sensitive, 
                                                           find_whole_words,
                                                           all_matches)
      
                return [n for n in match_indices if n != -1]
                
        elif get_type_str(substring) in ["list", "ndarray", "tuple"]:
            if not advanced_search:
                return char.find(string, substring, start=start, end=end)  
            else:   
                match_indices = _advanced_pattern_searcher(string, substring,
                                                           return_match_index,
                                                           return_match_str,
                                                           case_sensitive, 
                                                           find_whole_words,
                                                           all_matches)
      
            return [n for n in match_indices if n != -1]

    # Handle the return based on the result type #    
    if isinstance(substr_match_obj, list):
        if len(substr_match_obj) == 0:
            return -1
        elif len(substr_match_obj) == 1:
            return substr_match_obj[0]
        else:
            return substr_match_obj
    else:
        return substr_match_obj


# Core method #
#-#-#-#-#-#-#-#

def _advanced_pattern_searcher(string, substring,
                               return_match_index,
                               return_match_str,
                               case_sensitive,
                               find_whole_words,
                               all_matches):
    """
    Performs an advanced pattern search based on specified criteria,
    with options for regex, case-sensitivity, and whole word matching,
    and returns indices and/or match strings.
    
    Parameters
    ----------
    string : str, list, np.ndarray, or tuple
        The input object to search within.
    substring : str or list-like of str
        The substring or list of substrings to search for. Can include regex patterns.
    return_match_index : {"lo", "hi", "both"}
        Defines which match index to return.
    return_match_str : bool
        If True, returns the matched substring instead of the index.
    case_sensitive : bool
        Whether the search is case-sensitive. Defaults to False.
    find_whole_words : bool
        If True, matches whole words only.
    all_matches : bool
        If True, finds all matches; otherwise, only the first is returned.
    
    Returns
    -------
    list or tuple
        A list or tuple of matching indices and/or matched substrings.
        
    Notes
    -----    
    This method serves as an auxiliary to `find_substring_index`, 
    utilizing `_return_search_obj_spec` for detailed pattern matching and result extraction.
    """    
    # Determine if the input string is multi-line #
    ###############################################

    multiline = '\n' in string \
                if isinstance(string, str) \
                else any('\n' in s for s in string)
    flags = re.MULTILINE if multiline else 0

    # Case studies #
    ################

    # No option selected #
    if not case_sensitive and not all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.search(substring, 
                                                         string, 
                                                         re.IGNORECASE | flags)
        iterator_considered = False

    # One option selected #
    elif case_sensitive and not all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.search(substring, string, flags)
        iterator_considered = False
        
    elif not case_sensitive and all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.finditer(substring,
                                                           string, 
                                                           re.IGNORECASE | flags)
        iterator_considered = True        
        
    elif not case_sensitive and not all_matches and find_whole_words:
        re_obj_str = lambda substring, string: re.fullmatch(substring,
                                                            string, 
                                                            re.IGNORECASE | flags)
        iterator_considered = False

    # Two options selected #
    elif case_sensitive and all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.finditer(substring, string, flags)
        iterator_considered = True        
        
    elif case_sensitive and not all_matches and find_whole_words:
        re_obj_str = lambda substring, string: re.fullmatch(substring, string, flags)
        iterator_considered = False

    # Extract the matching information #
    ####################################

    arg_list = [
        string, substring, re_obj_str,
        return_match_index, return_match_str,
        iterator_considered
    ]
    
    if get_type_str(string) in ["list", "ndarray", "tuple"]:        
        match_obj_spec = vectorize(_return_search_obj_spec)(*arg_list)
    else:
        match_obj_spec = _return_search_obj_spec(*arg_list)
        
    return match_obj_spec
       

# Auxiliary functions #
#-#-#-#-#-#-#-#-#-#-#-#

def _return_search_obj_spec(string, substring, re_obj_str,
                            return_match_index, return_match_str,
                            iterator_considered):
    """
    Handles the regular expression search and result extraction for advanced search.
    
    Parameters
    ----------
    string : str
        The string to search in.
    substring : str
        The pattern or substring to search for.
    re_obj_str : callable
        A callable that performs the actual pattern search using regex or custom logic.
    return_match_index :  {"lo", "hi", "both"}
        Defines which match index to return.
    return_match_str : bool
        If True, returns the matched substrings.
    iterator_considered : bool
        If True, collects all matches in an iterable.
    
    Returns
    -------
    tuple
        A tuple of indices and matched substrings. Its components are:
        - indices : list of int
              The start positions of matches.
        - match_strings : list of str
              The matched substrings.
              
    Notes
    -----
    This is a helper function used by `_advanced_pattern_searcher`
    to finalise the search and process the results.
    """
    
    # Create the match object using the provided regex search function
    match_obj = re_obj_str(substring, string)
    
    # If iterator is considered, extract all matches; otherwise, handle single match
    if iterator_considered:
        matches = [m for m in match_obj]
    else:
        matches = [match_obj] if match_obj else []
    
    # Use the appropriate action for returning indices based on return_match_index
    if return_match_index in match_index_action_dict:
        indices = match_index_action_dict[return_match_index](matches)
    else:
        indices = []
    
    if return_match_str:
        match_strings = [m.group() for m in matches] if matches else []
    else:
        match_strings = []
    
    # Adjust return values based on the number of matches
    if not indices:
        return (-1, -1) if return_match_str else -1
    elif len(indices) == 1:
        return (indices[0], match_strings[0]) if return_match_str else indices[0]
    else:
        return (indices, match_strings) if return_match_str else indices
 
# %%
   

# Substring replacements #
#------------------------#

def substring_replacer(string, substr2find, substr2replace, count_std=-1,
                       advanced_search=False,
                       count_adv=0,
                       flags=0):
    """
    Replaces occurrences of a specified substring in a given object
    (string, list or numpy.ndarray) 
    using either a simple replace method or advanced regex techniques.

    Parameters
    ----------
    string : str, list or numpy.ndarray
        The input object where the substring will be replaced.
    substr2find : str
        The substring to search for in the input object.
    substr2replace : str
        The substring to replace the found occurrences.
    count_std : int, optional
        The maximum number of occurrences to replace in standard replace mode. 
        Default is -1, which means replace all occurrences.
    advanced_search : bool, optional
        If True, uses regular expressions for more complex search and replace. Default is False.
    count_adv : int, optional
        The maximum number of occurrences to replace when using advanced search. Default is 0.
        If 0, all occurrences will be replaced.
    flags : int, optional
        Flags to modify the behavior of the regex operation. Default is 0.

    Returns
    -------
    str, list or numpy.ndarray
        Returns the modified object with the specified replacements.

    Notes
    -----
    - If `advanced_search` is True, the function employs regex substitutions, which can be 
      used for strings only. For lists and numpy.ndarray,
      the built-in `replace` method is applied, allowing more flexibility in replacements.
    - If `advanced_search` is False, the function uses the built-in `replace` method 
      for all supported input types, enabling straightforward substring replacements.
    """
    
    obj_type = get_type_str(string, lowercase=True)
    
    if obj_type not in str_repl_obj_types:
        raise TypeError("Input object must be of type 'string', 'list' or 'numpy.ndarray'")
            
    if not advanced_search:
        string_replaced = replace_actions[obj_type](string, substr2find, substr2replace, count_std)
        return string_replaced
            
    else:
        if isinstance(string, str):
            string_replaced = re.sub(substr2find, substr2replace, 
                                     string, count_adv, flags)
        else:
            # Apply regex replacement to each element in lists/arrays
            string_replaced = [
                re.sub(substr2find, substr2replace, elem, count_adv, flags) 
                for elem in string
            ]
        return string_replaced
    
# Case handling #
#---------------#
        
def case_modifier(string, case=None):    
    """
    Function to modify the given string case.
    
    Parameters
    ----------
    case : {'lower', 'upper', 'capitalize' 'title'}, optional.
        Case to which modify the string's current one.
            
    Returns
    -------
    String case modified accordingly
    """
    
    if (case is None or case not in case_modifier_option_keys):
        raise ValueError("You must select a case modifying option from "
                         "the following list:\n"
                         f"{case_modifier_option_keys}")
        
    else:
        str_case_modified = case_modifier_option_dict.get(case)(string)
        return str_case_modified

    
# String polisher #
#-----------------#

def strip(string, strip_option='strip', chars=None):
    
    """
    Removes the white spaces -or the given substring- 
    surrounding the string, except the inner ones.
    
    Parameters
    ----------
    strip_option: {'strip', 'lstrip', 'lstrip' 'title'} or None
        Location of the white spaces or substring to strip.
        Default option is the widely used 'strip'.
        
    Raises
    ------
    ValueError
        If 'strip_option' is not within the allowed options.
          
    Returns
    -------
    string_stripped : str
        String with the specified characters surrounding it removed.
    """
    
    if (strip_option is None or strip_option not in strip_option_keys):
        raise ValueError("You must select a case strip option from "
                         f"the following list: {strip_option_keys}")
        
    else:
        string_stripped = strip_option_dict.get(strip_option)(string, chars)
        return string_stripped
    

#--------------------------#
# Parameters and constants #
#--------------------------#

# Allowed options #
#-----------------#

# Standard and essential name lists #
obj_specs_keylist = ['parent', 'name', 'name_noext', 'name_noext_parts', 'ext']

# Search matching object's indexing options #
match_obj_index_option_keys = ["lo", "hi", "both"]

# String case handling options #
case_modifier_option_keys = ["lower", "upper", "capitalize", "title"]

# String stripping options #
strip_option_keys = ["strip", "lstrip", "rstrip"]

# Object types for string replacements #
str_repl_obj_types = ["str", "list", "ndarray"]

# Switch case dictionaries #
#--------------------------#

# String case handling #
case_modifier_option_dict = {
    case_modifier_option_keys[0] : lambda string : string.lower(),
    case_modifier_option_keys[1] : lambda string : string.upper(),
    case_modifier_option_keys[2] : lambda string : string.capitalize(),
    case_modifier_option_keys[3] : lambda string : string.title()
    }

case_modifier_option_keys = list(case_modifier_option_dict.keys())

# String stripping #
strip_option_dict = {
    strip_option_keys[0] : lambda string, chars: string.strip(chars),
    strip_option_keys[1] : lambda string, chars: string.lstrip(chars),
    strip_option_keys[2] : lambda string, chars: string.rstrip(chars),
}

# File or directory path specifications retrieval #
path_functions = {
    'os': lambda obj_path : {
        'parent': os.path.dirname(obj_path),
        'name': os.path.basename(obj_path),
        'name_noext': os.path.splitext(os.path.basename(obj_path))[0],
        'ext': os.path.splitext(os.path.basename(obj_path))[1][1:]
    },
    'Path': lambda obj_path : {
        'parent': Path(obj_path).parent,
        'name': Path(obj_path).name,
        'name_noext': Path(obj_path).stem,
        'ext': Path(obj_path).suffix[1:]
    }
}

# Index return types for pattern matches #
match_index_action_dict = {
    "lo" : lambda matches : [m.start() for m in matches] if matches else [],
    "hi" : lambda matches : [m.end() for m in matches] if matches else [],
    "both" : lambda matches : [m.span() for m in matches] if matches else [],
    }

# Substring replacement actions using simpler methods #
replace_actions = {
    "str": lambda s, sb2find, sb2replace, count_std : s.replace(sb2find, sb2replace, count_std),
    "list": lambda s, sb2find, sb2replace, _ : char.replace(array(s), sb2find, sb2replace),
    "ndarray": lambda s, sb2find, sb2replace, _ : char.replace(s, sb2find, sb2replace),
}