#!/usr/bin/env python
################################################################################
# ftwn_search.py
# Author: Chris Eberle
# Date: 10/2/2010
#
# FaceTracer+WordNet search interface
#
# Run the following just once by hand before you run this program:
# $ python [ENTER]
# >>> import nltk [ENTER]
# >>> nltk.download() [ENTER]
# Downloader> d [ENTER]
#  Identifier> brown [ENTER]
# Downloader> d [ENTER]
#  Identifier> punkt [ENTER]
################################################################################

#http://honnibal.wordpress.com/

import sys
import nltk
import pprint
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

def tokenizeAndTag(text):

    print "Tokenizing..."
    words = []
    for i, sentenceStr in enumerate(sent_tokenize(text)):
        tokens = word_tokenize(sentenceStr)
        for token in tokens:
            term = token.lower()
            if term:
                words.append(term)

    print "Loading the brown corpus..."
    brown_train = nltk.corpus.brown.tagged_sents()

    print "Bigramming it up..."

    unigram_tagger = nltk.UnigramTagger(brown_train)
    tagger = nltk.BigramTagger(brown_train, backoff = unigram_tagger)
    #tagger = nltk.UnigramTagger(brown_train)

    tagged = tagger.tag(words)
    tagged.sort(lambda x,y:cmp(x[1],y[1]))
    return tagged

def getNP(tags):
    grammar = """
        NP:   {<DT>?<JJ.*>*<NN.*>+}
        P:    {<IN>}
        PP:   {<P> <NP>}
        V:    {<V.*>}
        VP:   {<V> <NP|PP>*}
        """

    cp = nltk.RegexpParser(grammar)
    print cp.parse(tags)

def main():
    try:
        searchTerms = sys.argv[1]
        tagged = tokenizeAndTag(searchTerms)

        #l = list(set(tagged))
        #l.sort(lambda x,y:cmp(x[1],y[1]))
        #pprint.pprint(l)

        getNP(tagged)


    except IndexError:
        print 'Usage: '

if __name__ == '__main__':
    main()
