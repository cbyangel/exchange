import os, errno, sys
import argparse

def parse_args(arg_list):
 
    parser = argparse.ArgumentParser()

    for arg in arg_list:
        param = '--' + arg
        parser.add_argument(param, help=arg)

    args = parser.parse_args()

    return args