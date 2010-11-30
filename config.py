# Author: Chris Eberle <eberle1080@gmail.com>

__all__ = ['configure', 'parse']

class ConfigException(Exception):
    """
    There was an error while setting things up
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Config error: " + self.reason

def add_rule(grammar, rule):
    """
    Purely to make the code look nicer
    """

    grammar.append(rule)

def add_word(vocab, word, production_rule, keys = None, aliases = None):
    """
    Get the synset for a word given its lemma key
    """

    if word is None or len(word.strip()) == 0:
        raise ConfigException("word can't be blank")

    word = word.strip().lower()

    import nltk, re
    from nltk.corpus import wordnet as wn
    from word import BaseWord

    synsets = []
    if keys != None:
        if isinstance(keys, (list, tuple)):
            for k in keys:
                k = k.strip()
                s = wn.lemma_from_key(k).synset
                if s is None:
                    raise ConfigException('lemma_from_key("%s") returned None' % (keys.strip()))
                elif s not in synsets:
                    synsets.append(s)
        else:
            s = wn.lemma_from_key(keys.strip()).synset
            if s is None:
                raise ConfigException('lemma_from_key("%s") returned None' % (keys.strip()))
            elif s not in synsets:
                synsets.append(s)                

    alias_list = []

    try:
        re.compile(word)
        alias_list.append(word)
    except:
        pass

    if aliases != None:
        if isinstance(aliases, (list, tuple)):
            for a in aliases:
                a = a.strip()
                if len(a) > 0 and a not in alias_list:
                    alias_list.append(a)
        else:
            a = aliases.strip()
            if len(a) > 0 and a not in alias_list:
                alias_list.append(a)

    baseword = BaseWord(word, production_rule, synsets, aliases)
    vocab.append(baseword)

def symplify(sym, negate):
    """
    Turn one or more literal production symbol names into a
    list of ProductionSymbol objectes
    """

    from generator import ProductionSymbol as ps
    if isinstance(sym, (list, tuple)):
        return [ps(s, negate) for s in sym]
    else:
        return [ps(sym, negate)]

def simple_map(gen, sym, cls, val = 1, nval = -1):
    """
    An easier way to call gen.add_mapping when you
    need to handle both the positive AND negative
    cases for something.
    """

    from generator import ProductionSymbol as ps
    from generator import ClassifierResult as cr
    from generator import UnsupportedSearch

    if callable(cls) or isinstance(cls, UnsupportedSearch):
        gen.add_mapping(symplify(sym, False), cls)
        gen.add_mapping(symplify(sym, True), cls)
    else:
        norm = []
        neg = []
        if isinstance(cls, (list, tuple)):
            for c in cls:
                if c is not None and len(c.strip()) > 0:
                    norm.append(cr(c.strip(), val))
                    neg.append(cr(c.strip(), nval))
        else:
            norm.append(cr(cls.strip(), val))
            neg.append(cr(cls.strip(), nval))

        gen.add_mapping(symplify(sym, False), norm)
        gen.add_mapping(symplify(sym, True), neg)

def configure():
    """
    A list of supported root words and their wordnet lemma key.
    Also the corresponding grammar mixed in there, mostly for
    easier configuration (NOT for readability, thou foul readability
    nazis). You can invoke the program with "-l WORD" to get a list
    of 'lemma keys' -> 'definitions' for a given word.
    """

    # Supported vocabulary
    #
    # BE CAREFUL ABOUT WHAT YOU PUT HERE.
    #
    # Oh sure, "person" might seem like a good candidate, but just
    # remember that Nazis, Kings, Blacksmiths, and Gary Busey are
    # all technically a person. If it's TOO generic, give it a
    # lemma of None.

    vocab = []

    # Supported grammar
    gramm = []

    # Classifier generator -- rules for generating classifiers
    from generator import ClassifierGenerator
    gen = ClassifierGenerator()

    # Sentences
    add_rule(gramm, 'S -> PART | S CONJ S | PART S')
    add_rule(gramm, 'PART -> SEG | NOT SEG | NEITHER SEG NOR SEG | BOTH SEG AND SEG')
    add_rule(gramm, 'SEG -> DESC | LPAREN S RPAREN')
    add_rule(gramm, 'DESC -> NON COREWORD | COREWORD | NON DROPWORD | DROPWORD')
    add_word(vocab, '(',       'LPAREN',     None,      (r'\(', r'\[', r'\{'))
    add_word(vocab, ')',       'RPAREN',     None,      (r'\)', r'\]', r'\}'))

    # Negation and conjugation
    add_rule(gramm, 'CONJ -> AND | OR')
    add_word(vocab, 'and',     'AND',        None,      ('but', 'with', 'holding', 'wearing', 'having', 'has', 'had', 'containing', 'has'))
    add_word(vocab, 'not',     'NOT',        None,      ('no', 'without', 'lacking', 'missing', 'anti', "n't"))
    add_word(vocab, 'or',      'OR')
    add_word(vocab, 'non',     'NON')
    add_word(vocab, 'both',    'BOTH')
    add_word(vocab, 'neither', 'NEITHER')
    add_word(vocab, 'nor',     'NOR')

    # Drop words (words that we just ignore)
    add_rule(gramm, 'DROPWORD -> DET | PRONOUN | ADV | PREP | DVERB | ANON | PAIR')
    add_word(vocab, 'person',  'ANON',       None,      ('somebody', 'someone', 'people', 'human', 'face', 'anyone', 'anybody'))
    add_word(vocab, 'face',    'ANON',       ('face%1:08:00::', 'visage%1:08:00::'), ('face', 'visage'))
    add_word(vocab, 'a',       'DET',        None,      ('an', 'one', 'this', 'that', 'some', 'the', 'these', 'those', 'his',
                                                           'her', 'its', 'their'))
    add_word(vocab, 'of',      'PREP',       None,      ('in', 'on', 'from'))
    add_word(vocab, 'is',      'DVERB',      None,      ('is', 'was', 'be', 'been', 'being', 'are'))
    add_word(vocab, 'very',    'ADV',        None,      ('really', 'quite', 'understandably', 'noticibly', 'obviously',
                                                        'irritatingly', 'overtly', 'exactly', 'mostly', 'entirely', 'too'))
    add_word(vocab, 'pair',    'PAIR',       None,      ('set'))
    add_word(vocab, 'which',   'PRONOUN',    None,      ('he', 'she', 'who', 'it', 'they'))

    # Core words
    add_rule(gramm, 'COREWORD -> GENDER | RACE | ATTRACTIVE | COLOR | HAIR | PHOTO | ITEMS | FACE')

    # Gender
    add_rule(gramm, 'GENDER -> PROD_MALE | PROD_FEMALE | PROD_BOY | PROD_GIRL')
    add_word(vocab, 'male',   'PROD_MALE',   'man%1:18:00::',   ('man', 'men'))
    add_word(vocab, 'female', 'PROD_FEMALE', 'woman%1:18:00::', ('woman', 'women', 'chick', 'chicks'))
    add_word(vocab, 'girl',   'PROD_GIRL',   'girl%1:18:02::',  'girls')
    add_word(vocab, 'boy',    'PROD_BOY',    'boy%1:18:00::',   'boys')

    # Attractive
    add_rule(gramm, 'ATTRACTIVE -> PROD_ATTRACTIVE | PROD_UNATTRACTIVE')
    add_word(vocab, 'attractive',   'PROD_ATTRACTIVE',   ('attractive%3:00:01::', 'hot%5:00:00:sexy:00',
                                                          'sexy%3:00:00::', 'beautiful%3:00:00::'), None)
    add_word(vocab, 'unattractive', 'PROD_UNATTRACTIVE', ('unattractive%3:00:00::', 'ugly%3:00:00::'), 'fugly')

    # Colors
    add_rule(gramm, 'COLOR -> PROD_BLACK | PROD_WHITE | PROD_GRAY | PROD_BLONDE | PROD_BROWN')
    add_word(vocab, 'black',  'PROD_BLACK',  'black%1:07:00::')
    add_word(vocab, 'blond',  'PROD_BLONDE', 'blond%1:18:00::', ('light-haired'))
    add_word(vocab, 'brown',  'PROD_BROWN',  'brown%1:07:00::')
    add_word(vocab, 'gray',   'PROD_GRAY',   'gray%1:07:00::')
    add_word(vocab, 'white',  'PROD_WHITE',  'white%1:07:00::')

    # Race
    add_rule(gramm, 'RACE -> PROD_ASIAN | PROD_INDIAN | PROD_WHITE | PROD_BLACK')
    add_word(vocab, 'black',  'PROD_BLACK',  ('black%1:18:00::'))                        # Insert slurs here
    add_word(vocab, 'asian',  'PROD_ASIAN',  ('asian%1:18:00::', 'asia%1:14:00::'))      # Or here
    add_word(vocab, 'white',  'PROD_WHITE',  ('white%1:18:00::'))                        # Or here
    add_word(vocab, 'indian', 'PROD_INDIAN', ('indian%1:18:01::', 'india%1:15:00::'))    # Or here

    # Hair
    add_rule(gramm, 'HAIR -> PROD_CURLY | PROD_STRAIGHT | PROD_WAVY | PROD_HAIR | PROD_BALDING | PROD_BALD')
    add_word(vocab, 'curly',    'PROD_CURLY')
    add_word(vocab, 'straight', 'PROD_STRAIGHT')
    add_word(vocab, 'wavy',     'PROD_WAVY')
    add_word(vocab, 'bald',     'PROD_BALD', ('bald%5:00:00:hairless:00', 'hairless%3:00:00::'))
    add_word(vocab, 'balding',  'PROD_BALDING', None, ('receding hairline', 'hairline receding'))

    # Photo types
    add_rule(gramm, 'PHOTO -> PROD_IMAGE | PHOTOTYPE')
    add_rule(gramm, 'PHOTOTYPE -> PROD_POSED | PROD_NOT_POSED | PROD_COLOR | PROD_NOT_COLOR')
    add_word(vocab, 'image',   'PROD_IMAGE', ('image%1:06:00::', 'photo%1:06:00::', 'photograph%1:06:00::', 'picture%1:06:00::'),
                                              ('photo', 'photograph', 'picture'))
    add_word(vocab, 'posed',   'PROD_POSED', None, 'prepared')
    add_word(vocab, 'candid',  'PROD_NOT_POSED', None, ('surprised?'))
    add_word(vocab, 'color',   'PROD_COLOR', 'color%1:07:01::', ('colorful', 'vibrant'))
    add_word(vocab, 'b&w',     'PROD_NOT_COLOR', 'monochromatic%5:00:00:colored:00', ('colorless', 'black and white', 'monochromatic'))

    # Items (hats, etc)
    add_rule(gramm, 'ITEMS -> GLASSES')
    add_rule(gramm, 'GLASSES -> PROD_GLASSES | PROD_SUNGLASSES')
    add_word(vocab, 'glasses',    'PROD_GLASSES', 'glasses%1:06:00::')
    add_word(vocab, 'sunglasses', 'PROD_SUNGLASSES', 'sunglasses%1:06:00::')
    
    # Facial features
    add_rule(gramm, 'FACE -> PROD_SMILING | PROD_FROWNING | PROD_DOUBLECHIN | PROD_CHUBBY' +
                   ' | PROD_NOT_CHUBBY | PROD_ANGRY')
    add_word(vocab, 'smiling',     'PROD_SMILING',  ('smiling%1:10:00::', 'smile%2:29:00::', 'smile%2:32:00::'), None)
    add_word(vocab, 'frowning',    'PROD_FROWNING', ('frowning%5:00:00:displeased:00', 'frown%1:10:00::', 'frown%2:29:00::'), None)
    add_word(vocab, 'double-chin', 'PROD_DOUBLECHIN', None, ('double[ -]chin(ned)?', 'two chins', 'two-chinned'))
    add_word(vocab, 'chubby',      'PROD_CHUBBY')
    add_word(vocab, 'skinny',      'PROD_NOT_CHUBBY')
    add_word(vocab, 'angry',       'PROD_ANGRY', 'angry%3:00:00::', ('upset', 'pissed off'))

    # Generator rules
    from generator import ClassifierResult as cr
    from generator import ProductionSymbol as ps
    from generator import UnsupportedSearch

    # This is a wicked powerful statement, lemme explain
    # When the PROD_MALE symbol is encountered, it calls this labmda function with two paramters:
    #   s: a tuple of ProductionSymbol objects (in this case, just PROD_MALE)
    #   d: desperate (boolean). Hard to explain, but basically this affects wheter or not
    #      to defer processing of the symbol until later. If this is false, the parser is
    #      not desperate, and it's up to the lambda function to defer. If it's true, well
    #      it's time to give it up. Very useful for things like "attractive female".
    simple_map(gen, 'PROD_MALE', lambda s,d: cr('Male', -1 if s[0].negate() else 1) if d else None)
    simple_map(gen, 'PROD_FEMALE', lambda s,d: cr('Male', 1 if s[0].negate() else 1) if d else None)

    # Since attractive female is a multi-symbol concept, simple_map won't work, here's how to
    # call off to this thing for something more complicated. Note that this only looks for
    # attractive / unattractive FEMALE (see the negating of PROD_MALE?). Any queries for an
    # attractive MALE will fail. Heh. Male fail. God it's late.
    attractive_female = cr('Attractive Woman', 1)
    unattractive_female = cr('Attractive Woman', -1)
    gen.add_mapping( (ps('PROD_MALE', True), ps('PROD_ATTRACTIVE', False)),    (attractive_female) )
    gen.add_mapping( (ps('PROD_FEMALE', False), ps('PROD_ATTRACTIVE', False)), (attractive_female) )
    gen.add_mapping( (ps('PROD_MALE', True), ps('PROD_ATTRACTIVE', True)),     (unattractive_female) )
    gen.add_mapping( (ps('PROD_FEMALE', False), ps('PROD_ATTRACTIVE', True)),  (unattractive_female) )

    # And now you know the hard stuff, so here's a really simple one. This will automatically
    # take care of the positive and negative cases. The values, by default, map to 1 and -1.
    simple_map(gen, 'PROD_SMILING', 'Smiling')
    simple_map(gen, 'PROD_ASIAN', 'Asian')

    # Glasses. God I hate you glasses.
    eyeglasses = cr('Eyeglasses', 1)
    sunglasses = cr('Sunglasses', 1)
    no_glasses = cr('No Eyewear', 1)
    gen.add_mapping( ps('PROD_GLASSES',    False), eyeglasses ) # A search for "glasses"
    gen.add_mapping( ps('PROD_GLASSES',    True),  no_glasses ) # A search for "no glasses"
    gen.add_mapping( ps('PROD_SUNGLASSES', False), sunglasses ) # A search for "sunglasses"
    gen.add_mapping( ps('PROD_SUNGLASSES', True),  no_glasses ) # A search for "no sunglasses"

    # Returning multiple classifiers
    gen.add_mapping( ps('PROD_BOY', False), ( cr('Male', 1), cr('Child', 1) ) )
    gen.add_mapping( ps('PROD_GIRL', False), ( cr('Male', -1), cr('Child', 1) ) )

    # Disallowing certain searches. In this case, "not boy" is actually impossible
    # to search for, thanks to the way the classifiers are set up. Same with "not girl".
    gen.add_mapping( ps('PROD_BOY', True),  UnsupportedSearch('non-boy') )
    gen.add_mapping( ps('PROD_GIRL', True), UnsupportedSearch('non-girl') )


    # The rest of this builds our grammar from our vocab
    productions = {}
    for baseword in vocab:
        if baseword is None or baseword.production is None or len(baseword.production.strip()) == 0:
            continue
        prod = baseword.production.strip().upper()
        if not productions.has_key(prod):
            productions[prod] = []
        if baseword.word not in productions[prod]:
            productions[prod].append(baseword.word)

    keys = productions.keys()
    keys.sort()
    for prod in keys:
        line = prod + ' -> '
        items = productions[prod]
        items.sort()
        line += '"' + '" | "'.join(items) + '"'
        add_rule(gramm, line)

    grammar = '\n'.join(gramm)

    return (vocab, grammar, gen)

def negToScore(negate):
    if negate:
        return -1
    else:
        return 1

def dnegToScore(negate):
    if negate:
        return 1
    else:
        return -1

def parse1(productions, force):
    name = productions[0][0]
    neg = productions[0][1]
    if name == 'PROD_SMILING':
        return (('Smiling', negToScore(neg)))
    elif name == 'PROD_ASIAN':
        return (('Asian', negToScore(neg)))
    elif name == 'PROD_GLASSES':
        if neg:
            return (('No Eyewear', 1))
        return (('Eyeglasses', 1))
    elif name == 'PROD_SUNGLASSES':
        if neg:
            return (('No Eyewear', 1))
        return (('Sunglasses', 1))
    elif name == 'PROD_MALE':
        if not force:
            return None
        return (('Male', negToScore(neg)))
    elif name == 'PROD_FEMALE':
        # Since this could be an attractive female or... you know... the regular kind
        if not force:
            return None
        return (('Male', dnegToScore(neg)))
    elif name == 'PROD_BOY':
        return ( ('Male', negToScore(neg)), ('Child', negToScore(neg)) )
    elif name == 'PROD_GIRL':
        return ( ('Male', dnegToScore(neg)), ('Child', dnegToScore(neg)) )

    return None

def parse2(productions, force):
    p = {}
    for prod in productions:
        p[prod[0]] = prod[1]

    if p.has_key('PROD_ATTRACTIVE'):
        if p.has_key('PROD_MALE') and p['PROD_MALE'] == True or \
           p.has_key('PROD_FEMALE') and p['PROD_FEMALE'] == False:
            return (('Attractive Woman', negToScore(p['PROD_ATTRACTIVE'])))
    elif p.has_key('PROD_UNATTRACTIVE'):
        if p.has_key('PROD_MALE') and p['PROD_MALE'] == True or \
           p.has_key('PROD_FEMALE') and p['PROD_FEMALE'] == False:
            return (('Attractive Woman', dnegToScore(p['PROD_UNATTRACTIVE'])))

    return None

def parse(productions, force):
    if len(productions) == 2:
        return parse2(productions, force)
    if len(productions) == 1:
        return parse1(productions, force)
    return None

