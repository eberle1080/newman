# Author: Chris Eberle <eberle1080@gmail.com>

class ParserException(Exception):
    """
    There was an error during parsing
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Parse error: " + self.reason

def parse(wordlist, grammar):
    """
    Parse this thang
    """

    #import nltk
    #from nltk.parse.chart import *

    for word in wordlist:
        print ' --> ' + word.reduced()
