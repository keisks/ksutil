#!/usr/bin/env python
#encoding: utf-8

__author__ = ""
__version__ = ""
__copyright__ = ""
__license__ = ""
__descripstion__ = ""
__usage__ = ""

import sys
import os
import datetime
import re
import cPickle as pickle
import argparse


### Here is a pre-defined template for experiments. 
## You may use this by uncommenting out.

# For arguments information
#
#argvs = sys.argv       #argument values
#argc = len(argvs)      #argument length


# For parsing arguments
# See http://docs.python.org/2.7/library/argparse.html#module-argparse
# for help
#
#arg_parser = argparse.ArgumentParser()
#arg_parser.add_argument('-x', action='store', dest='arg_x',
#        help='help_message', required=True)
#arg_parser.add_argument('-y', action='store', dest='arg_y', type=int,
#        help='help_message', required=True)
#arg_parser.add_argument('-A', action='store_true', default=False,
#        dest='bool_A', help='help_message.')
#args = arg_parser.parse_args()


# For logging date and time

#d = datetime.datetime.today()
#exp_time = d.strftime("%Y%m%d_%H%M")



#if __name__ == '__main__':
    # For logging date and time
    #start_time = datetime.datetime.now()
    #print "start at: " + str(start_time)
    
    #log_file = open(exp_time + '_' + str(argvs[0]) + '.log', 'w')
    #log_file.write('script_name: ' + str(argvs) + '\n')
    #log_file.write('start at: ' + str(start_time) + '\n')
    
    # For module tests, write code here.
    
    
    # For logging date and time
    #end_time = datetime.datetime.now()
    #print "end at: " + str(end_time)
    #print "total elapsed time: " + str((end_time - start_time))
    #log_file.write('end at: ' + str(end_time) + '\n')
    #log_file.write('total elapsed time: ' + str((end_time - start_time)) + '\n')

