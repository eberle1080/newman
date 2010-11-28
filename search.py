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

def run_preprocess(parts, vocabulary):
    """
    Find the first thing to replace, replace it, and return
    """

    size = len(parts)
    while size >= 1:
        end = len(parts) - size + 1
        prange = range(0, end)
        prange.reverse()
        for n in prange:
            pre = ' '.join(parts[n:size+n])

            for vword in vocabulary:
                if vword.word == pre:
                    continue
                if vword.is_alias(pre):
                    del parts[n:size+n]
                    parts.insert(n, vword.word)
                    return True
                    
        size -= 1
    return False

def preprocess(phrase, vocabulary):
    """
    Preprocess a sentence
    """

    # Break it apart on whitespace
    parts = [p.strip() for p in phrase.split()]
    while run_preprocess(parts, vocabulary):
        pass

    # Split words on '-' boundaries, but only when they're not
    # known vocab words. 'Middle-aged' is an example of a known
    # vocab word which we don't want split.

    preprocessed = []
    for p in parts:
        tmp = p.split('-')
        if len(tmp) > 1:
            baseword = False
            for vword in vocabulary:
                if p == vword.word:
                    baseword = True
                    break
            if not baseword:
                for t in tmp:
                    preprocessed.append(t)
            else:
                preprocessed.append(p)
        else:
            preprocessed.append(p)

    # Finally stitch it all back up
    parts = [p for p in preprocessed if p is not None and len(p) > 0]
    return ' '.join(parts)

def search(phrase, vocabulary, grammar, dbg):
    """
    The actual search method. Tokenizes a string, simplifies the words, and passes
    them along to the parser.
    """

    global debugging
    debugging = dbg

    orig = ' '.join([o for o in phrase.split() if len(o) > 0])
    debug('Original: ' + orig)

    # Preprocess this thing. Could get messy.
    phrase = preprocess(phrase, vocabulary)

    # Because I'm a cautious bastard
    debug('Preprocessed: ' + phrase)
    if len(phrase) == 0 and len(orig) > 0:
        print "Preprocessing has destroyed everything :("
        sys.exit(1)

    import nltk
    from nltk.tokenize import sent_tokenize
    from nltk.tokenize import word_tokenize

    unknowns = [] # Holds the indices of unknown words
    words = []
    toklist = []
    for i, sentenceStr in enumerate(sent_tokenize(phrase)):
        tokens = word_tokenize(sentenceStr)
        for token in tokens:
            if token:
                toklist.append(token)
                try:
                    words.append((token, Word(token, vocabulary)))
                except NonWordException:
                    debug('Skipping non-word:', token)
                    words.append((token, None))
                except UnknownWordException:
                    words.append((token, None))
                    unknowns.append(len(words) - 1)

    debug('Tokens: ' + "'" + "', '".join(toklist) + "'")

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
        wd = Word(word, vocabulary, True)
        definitions = wd.definitions()
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

    try:
        wd = Word(word, vocabulary, False)
        reduced = wd.reduced()
        if reduced != None:
            print '-' * 80
            print '"' + word + '" currently maps to "' + reduced + '"'
    except:
        pass

    return 0
