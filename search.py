# Author: Chris Eberle <eberle1080@gmail.com>

import sys, os, getopt
from word import *
from parser import *

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

def search(phrase, vocabulary, grammar, dbg):
    """
    The actual search method. Tokenizes a string, simplifies the words, and passes
    them along to the parser.
    """

    global debugging

    debugging = dbg
    phrase = phrase.replace('-', ' ') # A little pre-processing

    import nltk
    from nltk.tokenize import sent_tokenize
    from nltk.tokenize import word_tokenize

    debug('Tokenizing...')
    unknowns = [] # Holds the indices of unknown words
    words = []
    for i, sentenceStr in enumerate(sent_tokenize(phrase)):
        tokens = word_tokenize(sentenceStr)
        for token in tokens:
            if token:
                try:
                    words.append((token, Word(token, vocabulary)))
                except NonWordException:
                    debug('Skipping non-word:', token)
                    words.append((token, None))
                except UnknownWordException:
                    words.append((token, None))
                    unknowns.append(len(words) - 1)

    if len(unknowns) > 0:
        uwords = [words[idx][0] for idx in unknowns]
        print 'Error: unknown words:', '"' + '", "'.join(uwords) + '"'
        return 1

    words = [w[1] for w in words if w[1] != None]
    debug("Input:", ' '.join([w.original() for w in words]))
    debug("Reduced:", ' '.join([w.reduced() for w in words]))

    # We now have a list of words in reduced form, let's parse them
    try:
        results = parse(words, grammar, dbg)
    except ParserException, e:
        print str(e)
        return 1

    return 0

def lookup(word, vocabulary, dbg):
    """
    Look up all known definitions and forms for a word
    """

    global debugging

    debugging = dbg
    word = word.strip().lower()

    try:
        definitions = Word(word, vocabulary, True).definitions()
    except NonWordException:
        print 'Error: "' + word + '" is not a word'
        return 1
    except UnknownWordException:
        print 'Error: "' + word + '" is not a recognized word'
        return 1

    keys = definitions.keys()
    keys.sort()

    if len(keys) == 0:
        print 'No definitions found :('
        return 1

    for k in keys:
        print k, '=>', definitions[k]

    return 0
