#!/usr/bin/env python
# Author: Chris Eberle <eberle1080@gmail.com>

class NonWordException(Exception):
    """
    A word which is not
    """
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return str(self.parameter)

class UnknownWordException(Exception):
    """
    A word was encountered which is not in wordnet
    """
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return str(self.parameter)

class Word(object):
    """
    Represents a single word, and anything about it
    """
    
    def __init__(self, word, simple, vocabulary, translations, onlyDefine = False):
        """
        Initialize this beeyatch
        """
        self._process(word, simple, vocabulary, translations, onlyDefine)

    def _process(self, word, simple, vocabulary, translations, onlyDefine):
        """
        Reduce a word to something we can more easily process later
        """

        import nltk
        from nltk.corpus import wordnet as wn

        # Normalize the word
        self._original = word
        self._normalized = word.strip().lower().replace(' ', '_')
        if len(self._normalized) == 0 or self._normalized in [',', '"', "'", '?', '!', '.']:
            raise NonWordException(word)

        # Is it a simple word? Something like 'a', 'the', 'an', etc
        if self._normalized in simple or self._normalized in translations.keys():
            self._reduced = self._normalized
            while translations.has_key(self._reduced):
                self._reduced = translations[self._reduced]
            return

        # Damn, looks like we have some work to do
        self._pos_forms = []
        self._definitions = {}
        for pos in (wn.NOUN, wn.VERB, wn.ADJ, wn.ADV):
            # Find a possible base form for the given form, with the given
            # part of speech, by checking WordNet's list of exceptional forms,
            # and by recursively stripping affixes for this part of speech
            # until a form in WordNet is found.

            form = wn.morphy(self._normalized, pos)
            if form != None:
                synsets = wn.synsets(form, pos)
                for synset in synsets:
                    forms = []
                    for lemma in synset.lemmas:
                         name = lemma.name.replace(' ', '_').lower()
                         if name == self._normalized:
                             forms.append(lemma)
                             self._definitions[lemma.key] = lemma.synset.definition

                    if len(forms) == 0:
                        continue
                    self._pos_forms.append((synset, forms[0].key))

        # Sometimes we just want the definitions
        if onlyDefine:
            return

        # The part-of-speech tagger has failed
        if len(self._pos_forms) == 0:
            raise UnknownWordException(word)

        # OK, now we have a list of the possible synsets for this word, let's find out if
        # we have a word that is close.
        candidates = []
        for vname, vsynset in vocabulary:
            for synset, key in self._pos_forms:
                if vsynset.pos != synset.pos:
                    # Don't compare non-nouns to nouns
                    continue

                # Walk the hypernym paths, make sure I'm your ancestor
                # (who's your daddy?)
                paths = synset.hypernym_paths()
                valid = False
                for path in paths:
                    for p in path:
                        if p == vsynset:
                            valid = True
                            break
                    if valid:
                        break

                # Are we at all related?
                if not valid:
                    # These words have nothing in common
                    continue

                # OK, we're related, so let's find out our distance to eachother
                score = wn.path_similarity(synset, vsynset)
                candidates.append((score, vname))

        # Determine the closest match
        candidates.sort()
        candidates.reverse()

        if len(candidates) == 0 or candidates[0][0] == None or candidates[0][1] == None:
            raise UnknownWordException(word)

        self._reduced = candidates[0][1]
        while translations.has_key(self._reduced):
            self._reduced = translations[self._reduced]

    def __str__(self):
        return 'Word( "' + self._original + '" -> "' + self._normalized + '" -> "' + self._reduced + '" )'

    def original(self):
        return self._original

    def normalized(self):
        return self._normalized

    def reduced(self):
        return self._reduced

    def definitions(self):
        return self._definitions
