# -*- coding: utf-8 -*-
from inspect import stack
from time import time
import string
import random


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


def object_creator(name):
    """
    Return new class stubb

    Usage:
        stub = object_creator(mystub)
        stub.var = "some string"
    """
    return type(name.capitalize(), (object,), {})


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Return a random string
    http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
    """
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

class UnittestRunException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)