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

def add_pars(parses, productions, func):
    pass

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
    add_word(vocab, 'male',   'PROD_MALE',   'man%1:18:00::',   'men')
    add_word(vocab, 'female', 'PROD_FEMALE', 'woman%1:18:00::', ('women', 'chick', 'chicks'))
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

    #add_pars(parse, 'PROD_ANGRY', handle_angry)

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

    return (vocab, grammar)

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

