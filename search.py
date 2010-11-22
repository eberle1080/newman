#!/usr/bin/env python
# Author: Chris Eberle <eberle1080@gmail.com>

import sys, os, getopt
from word import *
from parser import *

# Lexicon by category
articles = ['a', 'an', 'the', 'some', 'one', 'this']
negation = ['no', 'non', 'without']
conjunctions = ['and', 'with']

# Build the simple lexicon
simple = articles + negation + conjunctions

# Supported vocabulary (don't list non-verbs or non-nouns)
vocabulary = None

def vocab_lookup(word, key):
    """
    Get the synset for a word given its lemma key
    """

    import nltk
    from nltk.corpus import wordnet as wn
    return (word, wn.lemma_from_key(key).synset)

def vocab():
    """
    A list of supported root words and their wordnet lemma key.
    You can invoke the program with "-l WORD" to get a list of
    keys -> definitions for a given word.
    """

    cats = []
    cats.append(vocab_lookup('smiling', 'smiling%1:10:00::'))
    cats.append(vocab_lookup('asian', 'asian%1:18:00::'))
    cats.append(vocab_lookup('male', 'man%1:18:00::'))
    cats.append(vocab_lookup('white', 'white%1:18:00::'))
    cats.append(vocab_lookup('female', 'woman%1:18:00::'))
    cats.append(vocab_lookup('indoor', 'indoor%3:00:00::'))
    cats.append(vocab_lookup('outdoor', 'outdoors%1:15:00::'))
    cats.append(vocab_lookup('child', 'child%1:18:00::'))
    cats.append(vocab_lookup('baby', 'baby%1:18:00::'))
    cats.append(vocab_lookup('glasses', 'glasses%1:06:00::'))

    return cats

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

def search(phrase):
    """
    The actual search method. Tokenizes a string, simplifies the words, and passes
    them along to the parser.
    """

    global simple, vocabulary

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
                    words.append((token, Word(token, simple, vocabulary)))
                except NonWordException:
                    debug('Skipping non-word:', token)
                    words.append((token, None))
                except UnknownWordException:
                    words.append((token, None))
                    unknowns.append(len(words) - 1)

    if len(unknowns) > 0:
        uwords = [words[idx][0] for idx in unknowns]
        print 'Error: unknown words:', '"' + '", "'.join(uwords) + '"'
        sys.exit(1)

    words = [w[1] for w in words if w[1] != None]
    debug("Input:", ' '.join([w.original() for w in words]))
    debug("Reduced:", ' '.join([w.reduced() for w in words]))

    # We now have a list of words in reduced form, let's parse them
    try:
        results = parse(words)
    except ParserException, e:
        print str(e)
        sys.exit(1)

def lookup(word):
    """
    Look up all known definitions and forms for a word
    """

    global simple, vocabulary

    word = word.strip().lower()

    try:
        definitions = Word(word, simple, vocabulary, True).definitions()
    except NonWordException:
        print 'Error: "' + word + '" is not a word'
        sys.exit(1)
    except UnknownWordException:
        print 'Error: "' + word + '" is not a recognized word'
        sys.exit(1)

    keys = definitions.keys()
    keys.sort()

    if len(keys) == 0:
        print 'No definitions found :('
        sys.exit(1)

    for k in keys:
        print k, '=>', definitions[k]

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

    global vocabulary, debugging

    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:l:dh', ['search=', 'lookup=', 'debug', 'help'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)

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

    debug('Initializing...')
    vocabulary = vocab()

    if lookupString != None and len(lookupString) > 0:
        lookup(lookupString)
        sys.exit()

    search(searchString)

if __name__ == '__main__':
    main()
