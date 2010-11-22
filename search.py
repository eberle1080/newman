#!/usr/bin/env python
# Author: Chris Eberle <eberle1080@gmail.com>

import sys, os, getopt
from word import *
from parser import *

# Simple words that don't exist in wordnet that we still need to support
articles = ['a', 'an', 'the', 'some', 'one', 'this']
functions = ['of']
negation = ['no', 'non', 'without']
conjunctions = ['and', 'with']
pointless = ['person', 'image']

# Build the simple lexicon
simple = articles + functions + negation + conjunctions + pointless

# Any last minute translations you want go here
translations = {'visage': 'face', 'face': 'person', 'photo': 'image', 'photograph': 'image', 'picture': 'image'}

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

    # Supported vocabulary (don't list non-verbs or non-nouns)
    #
    # BE CAREFUL ABOUT WHAT YOU PUT HERE.
    #
    # Oh sure, "person" might seem like a good candidate, but just
    # remember that Nazis, Kings, Blacksmiths, and gary busey are
    # all technically a person. If it's TOO generic, put it into
    # the simple list above.

    cats.append(vocab_lookup('smiling',      'smiling%1:10:00::'))
    cats.append(vocab_lookup('asian',        'asian%1:18:00::'))
    cats.append(vocab_lookup('male',         'man%1:18:00::'))
    cats.append(vocab_lookup('white',        'white%1:18:00::'))
    cats.append(vocab_lookup('female',       'woman%1:18:00::'))
    cats.append(vocab_lookup('girl',         'girl%1:18:02::'))
    cats.append(vocab_lookup('boy',          'boy%1:18:00::'))
    cats.append(vocab_lookup('indoor',       'indoor%3:00:00::'))
    cats.append(vocab_lookup('outdoor',      'outdoors%1:15:00::'))
    cats.append(vocab_lookup('child',        'child%1:18:00::'))
    cats.append(vocab_lookup('baby',         'baby%1:18:00::'))
    cats.append(vocab_lookup('glasses',      'glasses%1:06:00::'))
    cats.append(vocab_lookup('teenager',     'teenager%1:18:00::'))
    cats.append(vocab_lookup('adult',        'adult%1:18:00::'))
    cats.append(vocab_lookup('old',          'old%3:00:02::'))
    cats.append(vocab_lookup('young',        'young%3:00:00::'))
    cats.append(vocab_lookup('middle-aged',  'middle-aged%5:00:00:old:02'))
    cats.append(vocab_lookup('senior',       'senior%5:00:00:old:02'))
    cats.append(vocab_lookup('mustache',     'mustache%1:08:00::'))

    # TODO: Hair colors, hair words, skin colors (races), sunglasses, lighting words, 

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

def search(phrase, vocabulary, dbg):
    """
    The actual search method. Tokenizes a string, simplifies the words, and passes
    them along to the parser.
    """

    global simple, debugging

    debugging = dbg

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
                    words.append((token, Word(token, simple, vocabulary, translations)))
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

    sys.exit()

def lookup(word, vocabulary, dbg):
    """
    Look up all known definitions and forms for a word
    """

    global simple, debugging

    debugging = dbg
    word = word.strip().lower()

    try:
        definitions = Word(word, simple, vocabulary, translations, True).definitions()
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

    sys.exit()
