#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@datecreated: 2019-08-13
@lastupdated: 2019-08-19
@author: luisjba
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.1.0'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'

import os
        
def is_numeric(obj):
    "Function to check if an object is numeric"
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)

def match_as_integer(number_str):
    try:
        int(number_str)
        return True
    except:
        return False
    return False

def file_list(directory, extension='jpg'):
    """
    Function that return a list of file paths for files filtered by extension
        args: 
            directory: the string direcotory to list in
        return:
            list: list of every file found with the extesion provided

    """
    if not os.path.isdir(directory):
        return []
    return [os.path.join(directory,f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) and f.endswith(".{}".format(extension))]

def remove_extension(file_name):
    """
    Get the file name without extension

    :param: file_name:str
    :rtype:str
    """
    return os.path.splitext(file_name)[0]

def extract_extension(file_name):
    """
    Get the file name without extension

    :param: file_name:str
    :rtype:str
    """
    return os.path.splitext(file_name)[1][1:]

def file_list_by_extension(directory, extension=''):
    """
    Function that return a list of file paths for files filtered by extension.
    If no extension is provided, return all files

    :param: directory:str The string direcotory to list in
    :rtype:list The list of file found
    """
    if not os.path.isdir(directory):
        return []
    if extension == '':
        return [os.path.join(directory,f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]
    return [os.path.join(directory,f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) and f.endswith(".{}".format(extension))] 
  
    




