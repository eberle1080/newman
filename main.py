#!/usr/bin/env python
# Author: Chris Eberle <eberle1080@gmail.com>

import sys, os, getopt, config
from search import *

def batch(batchFile, vocabulary, grammar, debugging):
    """
    Run a batch search
    """

    searches = []

    fh = open(batchFile, 'r')
    for line in fh:
        line = line.strip()
        if len(line) > 0:
            searches.append(line)
    fh.close()

    if len(searches) == 0:
        print "No searches to batch :("
        sys.exit(1)

    for searchString in searches:
        if debugging:
            print >> sys.stderr, "---- " + searchString + " ----"
        search(searchString, vocabulary, grammar, debugging)

def usage():
    """
    Print out the usage for this program
    """

    print 'Usage: %s OPTIONS' % (os.path.basename(sys.argv[0]))
    print '    -s SEARCH      Search for a phrase'
    print '    -b FILE        Batch search using a file (one search per line)'
    print '    -l WORD        Use wordnet to lookup a word'
    print '    -d             Enable debugging'
    print '    -h             Show this helpful message'

def main():
    """
    The main program method
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'b:s:l:dh', ['batch=', 'search=', 'lookup=', 'debug', 'help'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

    debugging = False
    searchString = None
    batchFile = None
    lookupString = None

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-b', '--batch'):
            batchFile = a
        elif o in ('-s', '--search'):
            searchString = a.strip()
        elif o in ('-l', '--lookup'):
            lookupString = a.strip()
        elif o in ('-d', '--debug'):
            debugging = True
        else:
            assert False, "unhandled option"

    if (searchString == None or len(searchString) == 0) and (lookupString == None or len(lookupString) == 0) \
            and (batchFile == None or len(batchFile) == 0):
        usage()
        sys.exit(1)

    if debugging:
        print >> sys.stderr, "Initializing..."
        sys.stderr.flush()
    vocabulary = config.vocab()
    grammar = config.grammar()

    if lookupString != None and len(lookupString) > 0:
        sys.exit(lookup(lookupString, vocabulary, debugging))
    elif batchFile != None and len(batchFile) > 0:
        batch(batchFile, vocabulary, grammar, debugging)
    else:
        sys.exit(search(searchString, vocabulary, grammar, debugging))

if __name__ == '__main__':
    main()
