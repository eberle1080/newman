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

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset, Lemma

def tokenizeAndTag(text):

    print "Tokenizing..."
    words = []
    for i, sentenceStr in enumerate(sent_tokenize(text)):
        tokens = word_tokenize(sentenceStr)
        for token in tokens:
            if token:
                words.append(token)

    # Now we normalize them
    words = [n for n in [w.strip().lower().replace(' ', '_') for w in words]
             if n != ""]
    words = [w for w in words if w not in [",", '"', "'", '?', '!']]

    # No words found
    if len(words) == 0:
        print "No words found :("
        sys.exit(1)

    # Now we tag the words
    print "Tagging..."
    tagged = []
    unknown = False
    for word in words:
        pos_forms = {}
        for pos in (wn.NOUN, wn.VERB, wn.ADJ, wn.ADV):
            # Find a possible base form for the given form, with the given
            # part of speech, by checking WordNet's list of exceptional forms,
            # and by recursively stripping affixes for this part of speech
            # until a form in WordNet is found.

            form = wn.morphy(word, pos)
            if form != None:
                pos_forms[pos] = form

        # Apparently this word is not known
        if len(pos_forms) == 0:
            print " ERROR Unknown word:", word
            unknown = True
            continue

        # Prefer the noun forms
        noun = False
        for t,l in pos_forms.items():
            if t == 'n':
                noun = True
                tagged.append((t, l))
                break
        if not noun:
            for t, l in pos_forms.items():
                tagged.append((t, l))
                break

    if unknown:
        sys.exit(1)

    return tagged

def getCategorySynsets():
    cats = []
    cats.append(('smiling', wn.lemma_from_key('smiling%1:10:00::').synset))
    cats.append(('asian', wn.lemma_from_key('asian%1:18:00::').synset))
    cats.append(('white', wn.lemma_from_key('white%1:18:00::').synset))
    cats.append(('male', wn.lemma_from_key('man%1:18:00::').synset))
    cats.append(('female', wn.lemma_from_key('woman%1:18:00::').synset))
    cats.append(('indoor', wn.lemma_from_key('indoor%3:00:00::').synset))
    cats.append(('outdoor', wn.lemma_from_key('outdoors%1:15:00::').synset))
    cats.append(('child', wn.lemma_from_key('child%1:18:00::').synset))
    cats.append(('baby', wn.lemma_from_key('baby%1:18:00::').synset))

    return cats

def getSynsets(tagged):
    synsetset = []

    print "Looking up synsets..."

    unknown = False
    count = 0

    for (pos, w) in tagged:
        msyn = []
        synsets = wn.synsets(w, pos)
        for synset in synsets:
            forms = []
            for lemma in synset.lemmas:
                name = lemma.name.replace(' ', '_').lower()
                if name == w:
                    forms.append(lemma)
                    #print lemma.key, "=>", lemma.synset.definition

            if len(forms) == 0:
                print " ERROR Unknown synset for word:", w
                unknown = True

            count += 1
            msyn.append((synset, forms[0].key))

        synsetset.append((w, pos, msyn))

    if unknown:
        sys.exit(1)

    print "Found", count, "synsets"
    return synsetset

def processSynsets(synsetset):
    print "Processing synsets..."

    catSynsets = getCategorySynsets()
    mapped = []
    unknown = False

    for word, pos, synsets in synsetset:
        scores = []
        for synset, key in synsets:
            for catname, catsyn in catSynsets:
                if catsyn.pos != synset.pos:
                    continue
                score = wn.lch_similarity(synset, catsyn)
                scores.append((score, catname, catsyn))
        scores.sort()
        scores.reverse()

        if len(scores) == 0 or scores[0][0] == None:
            print " ERROR Unknown mapping for word:", word
            unknown = True
            continue

        best_cat = scores[0][1]
        best_syn = scores[0][2]

        mapped.append((word, best_cat, best_syn))

    if unknown:
        sys.exit(1)

    return mapped

def main():
    try:
        searchTerms = sys.argv[1]
        tagged = tokenizeAndTag(searchTerms)
        sets = getSynsets(tagged)
        if len(sets) == 0:
            sys.exit(0)
        mapped = processSynsets(sets)

        before = ' '.join([w for w,c,s in mapped])
        after = ' '.join([c for w,c,s, in mapped])

        print "Input: " + before
        print "Output: " + after

    except IndexError:
        print 'Usage: '

if __name__ == '__main__':
    main()
