# Author: Chris Eberle <eberle1080@gmail.com>

import sys

__all__ = ['debug', 'set_debug', 'get_debug']

# Debugging
debugging = False

def debug(*args):
    """
    Print a message to stderr
    """

    global debugging
    if not debugging:
        return
    for stmt in args:
        print >> sys.stderr, stmt,
    print >> sys.stderr
    sys.stderr.flush()

def set_debug(enable):
    """
    Enable or disable debugging
    """

    global debugging
    debugging = enable

def get_debug():
    """
    Return whether or not debugging was enabled
    """

    global debugging
    return debugging
