# -*- coding: utf-8 -*-
from inspect import stack
from time import time

def function_name():
    return stack()[1][3]

def timing(f):
    """
    Decorator to trace the duration of a function call
    Usage:
        @timing
        def my_method(some_args): do_something()
    """
    def wrap(*args):
        time1 = time()
        ret = f(*args)
        time2 = time()
        print("'%s' function took %0.3f ms to execute" % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap
