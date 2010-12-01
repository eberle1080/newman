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

class BaseWord(object):
    """
    Represents a base word, or more specifically a word which our grammar will support
    """

    def __init__(self, word, production = None, synsets = None, aliases = None):
        """
        Create a new base word
        """

        self.word = word.strip().lower()
        self.production = production
        self.synsets = []
        self.aliases = []

        if synsets is not None:
            if isinstance(synsets, (list, tuple)):
                for synset in synsets:
                    if synset is not None:
                        self.synsets.append(synset)
            else:
                self.synsets.append(synsets)

        if aliases is not None:
            if isinstance(aliases, (list, tuple)):
                for alias in aliases:
                    self.add_alias(alias)
            else:
                self.add_alias(aliases)

    def add_alias(self, alias):
        """
        Add a simple alias. May or may not be a regex
        """

        if alias is None:
            return False
        alias = alias.strip().lower()
        if len(alias) == 0:
            return False
        alias = '^' + alias + '$'
        return self.add_alias_explicit(alias)

    def add_alias_explicit(self, alias):
        """
        Add an alias which is assumed to be a well-formed regex
        """

        import re
        if alias is None:
            return False
        alias = alias.strip().lower()
        if len(alias) == 0:
            return False
        preg = re.compile(alias)
        if preg is None:
            return False
        self.aliases.append(preg)
        return True

    def get_valid_synsets(self, synset):
        """
        Given a particular synset, see which of my own synsets (if any)
        are valid candidates. To be valid means that it is an ancestor
        (i.e. if I have a synset for "asia" and someone sends me the synset
        for "china", clearly asia is a hypernym, so that one is valid)
        """

        if self.synsets is None or len(self.synsets) == 0 or synset is None:
            return None

        valid_sets = []
        for vsynset in self.synsets:
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

            valid_sets.append(vsynset)

        if len(valid_sets) == 0:
            return None

        return valid_sets


    def is_alias(self, word):
        """
        Determine if a given word is an alias for this word
        """

        import re
        word = word.strip().lower()

        if word == self.word:
            return True
        for alias in self.aliases:
            if alias.match(word):
                return True
        return False

class Word(object):
    """
    Represents a single word, and anything about it
    """
    
    def __init__(self, word, vocabulary, onlyDefine = False):
        """
        Initialize this beeyatch
        """
        self._process(word, vocabulary, onlyDefine)

    def _process(self, word, vocabulary, onlyDefine):
        """
        Reduce a word to something we can more easily process later
        """

        import nltk
        from nltk.corpus import wordnet as wn

        # Normalize the word
        self._original = word
        self._normalized = word.strip().lower()
        self._reduced = None
        if len(self._normalized) == 0 or self._normalized in [',', '"', "'", '?', '!', '.']:
            raise NonWordException(word)

        # Is it a simple word (i.e. just a root word or an alias)?
        if not onlyDefine:
            for baseword in vocabulary:
                if baseword.is_alias(self._normalized):
                    self._reduced = baseword.word
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
            if form is not None:
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

        for baseword in vocabulary:
            if baseword.synsets is None or len(baseword.synsets) == 0:
                continue

            for synset, key in self._pos_forms:
                bsynsets = baseword.get_valid_synsets(synset)
                if bsynsets is None:
                    continue

                # OK, we're related, so let's find out our distance to each other
                for bsynset in bsynsets:
                    score = wn.path_similarity(synset, bsynset)
                    candidates.append((score, baseword))

        # Determine the closest match
        candidates.sort()
        candidates.reverse()

        if len(candidates) == 0:
            raise UnknownWordException(word)

        self._reduced = candidates[0][1].word

    def __str__(self):
        """
        Get a nice string representation for this word object
        """

        return 'Word( "' + self._original + '" -> "' + self._normalized + '" -> "' + self._reduced + '" )'

    def original(self):
        """
        Get the original input string (i.e. "Dude ")
        """

        return self._original

    def normalized(self):
        """
        Get the normalized version of the word (i.e. "dude")
        """

        return self._normalized

    def reduced(self):
        """
        Get the reduced form of the word (i.e. "male")
        """

        return self._reduced

    def definitions(self):
        """
        Get a list of possible definitions for this word
        """

        return self._definitions
