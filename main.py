#!/usr/bin/env python
# Author: Chris Eberle <eberle1080@gmail.com>

import sys, os, getopt
from search import *

def usage():
    """
    Print out the usage for this program
    """

    print 'Usage: %s OPTIONS' % (os.path.basename(sys.argv[0]))
    print '    -s SEARCH      Search for a phrase'
    print '    -l WORD        Use wordnet to lookup a word'
    print '    -d             Enable debugging'
    print '    -h             Show this helpful message'

def main():
    """
    The main program method
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:l:dh', ['search=', 'lookup=', 'debug', 'help'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    debugging = False
    searchString = None
    lookupString = None
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-s', '--search'):
            searchString = a.strip()
        elif o in ('-l', '--lookup'):
            lookupString = a.strip()
        elif o in ('-d', '--debug'):
            debugging = True
        else:
            assert False, "unhandled option"

    if (searchString == None or len(searchString) == 0) and (lookupString == None or len(lookupString) == 0):
        usage()
        sys.exit(1)

    if debugging:
        print >> sys.stderr, "Initializing..."
        sys.stderr.flush()
    vocabulary = vocab()

    if lookupString != None and len(lookupString) > 0:
        lookup(lookupString, vocabulary, debugging)
    else:
        search(searchString, vocabulary, debugging)

if __name__ == '__main__':
    main()
