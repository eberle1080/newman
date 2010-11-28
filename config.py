# Author: Chris Eberle <eberle1080@gmail.com>

__all__ = ['vocab', 'grammar', 'parse']

class ConfigException(Exception):
    """
    There was an error while setting things up
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Config error: " + self.reason

def add_word(vocab, word, production_rule, keys, aliases):
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

def vocab():
    """
    A list of supported root words and their wordnet lemma key.
    You can invoke the program with "-l WORD" to get a list of
    keys -> definitions for a given word.
    """

    vocab = []

    # Supported vocabulary
    #
    # BE CAREFUL ABOUT WHAT YOU PUT HERE.
    #
    # Oh sure, "person" might seem like a good candidate, but just
    # remember that Nazis, Kings, Blacksmiths, and Gary Busey are
    # all technically a person. If it's TOO generic, give it a
    # lemma of None.

    #
    # Simple words
    #

    #               Word       Production    Lemma      Aliases
    add_word(vocab, '(',       'LPAREN',     None,      (r'\(', r'\[', r'\{'))
    add_word(vocab, ')',       'RPAREN',     None,      (r'\)', r'\]', r'\}'))
    add_word(vocab, 'person',  'ANON',       None,      ('somebody', 'someone', 'people', 'human', 'face', 'anyone', 'anybody'))
    add_word(vocab, 'face',    'ANON',       ('face%1:08:00::', 'visage%1:08:00::'), ('face', 'visage'))
    add_word(vocab, 'a',       'DET',        None,      ('an', 'one', 'this', 'that', 'some', 'the', 'these', 'those', 'his',
                                                         'her', 'its', 'their'))
    add_word(vocab, 'of',      'PREP',       None,      ('in', 'on', 'from'))
    add_word(vocab, 'is',      'DVERB',      None,      ('is', 'was', 'be', 'been', 'being', 'are'))
    add_word(vocab, 'very',    'ADV',        None,      ('really', 'quite', 'understandably', 'noticibly', 'obviously',
                                                        'irritatingly', 'overtly', 'exactly', 'mostly', 'entirely', 'too'))
    add_word(vocab, 'pair',    'PAIR',       None,      ('set'))
    add_word(vocab, 'and',     'AND',        None,      ('but', 'with', 'holding', 'wearing', 'having', 'has', 'had', 'containing', 'has'))
    add_word(vocab, 'or',      'OR',         None,      None)
    add_word(vocab, 'not',     'NOT',        None,      ('no', 'without', 'lacking', 'missing', 'anti', "n't"))
    add_word(vocab, 'non',     'NON',        None,      None)
    add_word(vocab, 'both',    'BOTH',       None,      None)
    add_word(vocab, 'neither', 'NEITHER',    None,      None)
    add_word(vocab, 'nor',     'NOR',        None,      None)
    add_word(vocab, 'which',   'PRONOUN',    None,      ('he', 'she', 'who', 'it', 'they'))
    add_word(vocab, 'image',   'PROD_IMAGE', ('image%1:06:00::', 'photo%1:06:00::', 'photograph%1:06:00::', 'picture%1:06:00::'),
                                              ('photo', 'photograph', 'picture'))

    #
    # Colors
    #

    add_word(vocab, 'black',  'PROD_BLACK',  'black%1:07:00::', None)
    add_word(vocab, 'blond',  'PROD_BLONDE', 'blond%1:18:00::', ('light-haired'))
    add_word(vocab, 'brown',  'PROD_BROWN',  None, None)
    add_word(vocab, 'gray',   'PROD_GRAY',   None, None)
    add_word(vocab, 'white',  'PROD_WHITE',  None, None)    

    #
    # Genders
    #

    add_word(vocab, 'male',   'PROD_MALE',   'man%1:18:00::',   'men')
    add_word(vocab, 'female', 'PROD_FEMALE', 'woman%1:18:00::', ('women', 'chick', 'chicks'))
    add_word(vocab, 'girl',   'PROD_GIRL',   'girl%1:18:02::',  'girls')
    add_word(vocab, 'boy',    'PROD_BOY',    'boy%1:18:00::',   'boys')

    #
    # Races
    #

    add_word(vocab, 'black',  'PROD_BLACK',  ('black%1:18:00::'), None)                        # Insert slurs here
    add_word(vocab, 'asian',  'PROD_ASIAN',  ('asian%1:18:00::', 'asia%1:14:00::'), None)      # Or here
    add_word(vocab, 'white',  'PROD_WHITE',  ('white%1:18:00::'), None)                        # Or here
    add_word(vocab, 'indian', 'PROD_INDIAN', ('indian%1:18:01::', 'india%1:15:00::'), None)    # Or here

    #
    # Facial expressions
    #

    add_word(vocab, 'smiling',  'PROD_SMILING',  ('smiling%1:10:00::', 'smile%2:29:00::', 'smile%2:32:00::'), None)
    add_word(vocab, 'frowning', 'PROD_FROWNING', ('frowning%5:00:00:displeased:00', 'frown%1:10:00::', 'frown%2:29:00::'), None)

    #
    # Words for attractive
    #

    add_word(vocab, 'attractive',   'PROD_ATTRACTIVE',   ('attractive%3:00:01::', 'hot%5:00:00:sexy:00',
                                                          'sexy%3:00:00::', 'beautiful%3:00:00::'), None)
    add_word(vocab, 'unattractive', 'PROD_UNATTRACTIVE', ('unattractive%3:00:00::', 'ugly%3:00:00::'), 'fugly')

    #
    # Age
    #

    add_word(vocab, 'child', 'PROD_CHILD', ('child%1:18:00::'), ('children', 'kid', 'kids', 'adolescent',
                                                                 'adolescents', 'preteen', 'preteens', 'tween', 'tweens'))
    add_word(vocab, 'baby',  'PROD_BABY',  ('baby%1:18:00::'), None)
    add_word(vocab, 'adult', 'PROD_ADULT', ('adult%1:18:00::', 'middle-aged%5:00:00:old:02'), ('middle-aged'))
    add_word(vocab, 'youth', 'PROD_YOUTH', ('teenager%1:18:00::', 'young%3:00:00::', 'youth%1:14:00::'), ('teen', 'teens'))

    # Age                     Word            Lemma
    #vocab.append(vocab_lookup('teenager',     'teenager%1:18:00::'))
    #vocab.append(vocab_lookup('old',          'old%3:00:02::'))
    #vocab.append(vocab_lookup('young',        'young%3:00:00::'))
    #vocab.append(vocab_lookup('young',        'youth%1:14:00::'))
    #vocab.append(vocab_lookup('senior',       'senior%5:00:00:old:02'))
    #vocab.append(vocab_lookup('middle-aged',  'middle-aged%5:00:00:old:02'))
    #vocab.append(vocab_lookup('middle',       None))
    #vocab.append(vocab_lookup('aged',         None))
    #vocab.append(vocab_lookup('age',          None))

    """

    # Colors                  Word            Lemma
    vocab.append(vocab_lookup('black',        'black%1:07:00::'))
    vocab.append(vocab_lookup('blond',        'blond%1:18:00::'))
    vocab.append(vocab_lookup('light',        None))
    vocab.append(vocab_lookup('brown',        None))
    vocab.append(vocab_lookup('gray',         None))

    # Facial features         Word            Lemma
    vocab.append(vocab_lookup('eyes',         None))
    vocab.append(vocab_lookup('mouth',        None))
    vocab.append(vocab_lookup('teeth',        None))
    vocab.append(vocab_lookup('eyebrows',     None))
    vocab.append(vocab_lookup('nose',         None))
    vocab.append(vocab_lookup('cheeks',       None))
    vocab.append(vocab_lookup('cheekbones',   None))
    vocab.append(vocab_lookup('chin',         None))
    vocab.append(vocab_lookup('forehead',     None))
    vocab.append(vocab_lookup('skin',         None))
    vocab.append(vocab_lookup('jaw',          None))
    vocab.append(vocab_lookup('nose-mouth',   None))
    vocab.append(vocab_lookup('lines',        None))
    
    # Facial feature desc     Word            Lemma
    vocab.append(vocab_lookup('smiling',      'smiling%1:10:00::'))
    vocab.append(vocab_lookup('frowning',     None))
    vocab.append(vocab_lookup('narrow',       None))
    vocab.append(vocab_lookup('squinty',      None))
    vocab.append(vocab_lookup('squinting',    None))
    vocab.append(vocab_lookup('open',         None))
    vocab.append(vocab_lookup('closed',       None))
    vocab.append(vocab_lookup('slightly',     None))
    vocab.append(vocab_lookup('wide',         None))
    vocab.append(vocab_lookup('fully',        None))
    vocab.append(vocab_lookup('visible',      None))
    vocab.append(vocab_lookup('arched',       None))
    vocab.append(vocab_lookup('bags',         None))
    vocab.append(vocab_lookup('under',        None))
    vocab.append(vocab_lookup('big',          None))
    vocab.append(vocab_lookup('rosy',         None))
    vocab.append(vocab_lookup('round',        None))
    vocab.append(vocab_lookup('bushy',        None))
    vocab.append(vocab_lookup('thin',         None))
    vocab.append(vocab_lookup('double',       None))
    vocab.append(vocab_lookup('high',         None))
    vocab.append(vocab_lookup('low',          None))
    vocab.append(vocab_lookup('obstructed',   None))
    vocab.append(vocab_lookup('oval',         None))
    vocab.append(vocab_lookup('pale',         None))
    vocab.append(vocab_lookup('partially',    None))
    vocab.append(vocab_lookup('pointy',       None))
    vocab.append(vocab_lookup('shiny',        None))
    vocab.append(vocab_lookup('square',       None))
    vocab.append(vocab_lookup('strong',       None))
    vocab.append(vocab_lookup('angry',        None))


    # Hair                    Word            Lemma
    vocab.append(vocab_lookup('bald',         None))
    vocab.append(vocab_lookup('balding',      None))
    vocab.append(vocab_lookup('bangs',        None))
    vocab.append(vocab_lookup('hair',         None))
    vocab.append(vocab_lookup('receding',     None))
    vocab.append(vocab_lookup('hairline',     None))
    vocab.append(vocab_lookup('curly',        None))
    vocab.append(vocab_lookup('wavy',         None))
    vocab.append(vocab_lookup('straight',     None))

    # Facial hair             Word            Lemma
    vocab.append(vocab_lookup('goatee',       None))
    vocab.append(vocab_lookup('beard',        None))
    vocab.append(vocab_lookup('mustache',     'mustache%1:08:00::'))
    #vocab.append(vocab_lookup('moustache',    None))
    vocab.append(vocab_lookup('sideburns',    None))

    # Race                    Word            Lemma
    vocab.append(vocab_lookup('black',        'black%1:18:00::'))
    vocab.append(vocab_lookup('asian',        'asian%1:18:00::'))
    vocab.append(vocab_lookup('white',        'white%1:18:00::'))
    vocab.append(vocab_lookup('indian',       None))

    # Place                   Word            Lemma
    vocab.append(vocab_lookup('indoor',       'indoor%3:00:00::'))
    vocab.append(vocab_lookup('outdoor',      'outdoors%1:15:00::'))
    vocab.append(vocab_lookup('outdoor',      'outside%3:00:04::'))

    # Accessories
    vocab.append(vocab_lookup('wearing',      None))
    vocab.append(vocab_lookup('hat',          'hat%1:06:00::'))
    vocab.append(vocab_lookup('lipstick',     None))
    vocab.append(vocab_lookup('glasses',      'glasses%1:06:00::'))
    vocab.append(vocab_lookup('pair',         None))
    vocab.append(vocab_lookup('set',          None))
    vocab.append(vocab_lookup('sunglasses',   None))
    #vocab.append(vocab_lookup('eyewear',      None))
    #vocab.append(vocab_lookup('eyeglasses',   None))

    # Body type               Word            Lemma
    vocab.append(vocab_lookup('attractive',   'attractive%3:00:01::'))
    vocab.append(vocab_lookup('attractive',   'hot%5:00:00:sexy:00'))
    vocab.append(vocab_lookup('attractive',   'sexy%3:00:00::'))
    vocab.append(vocab_lookup('unattractive', 'unattractive%3:00:00::'))
    vocab.append(vocab_lookup('unattractive', 'ugly%3:00:00::'))
    vocab.append(vocab_lookup('chubby',       None))
    vocab.append(vocab_lookup('skinny',       None))

    # Image features          Word            Lemma
    vocab.append(vocab_lookup('focused',      None))
    vocab.append(vocab_lookup('blurry',       None))
    vocab.append(vocab_lookup('color',        None))
    vocab.append(vocab_lookup('flash',        None))
    vocab.append(vocab_lookup('harsh',        None))
    vocab.append(vocab_lookup('lighting',     None))
    vocab.append(vocab_lookup('posed',        None))
    vocab.append(vocab_lookup('candid',       None))
    vocab.append(vocab_lookup('natural',      None))
    vocab.append(vocab_lookup('soft',         None))
    """

    return vocab

def grammar():
    """
    This is where we define our grammar
    """

    grammar = []    

    # Sentences
    grammar.append('S -> PART | S CONJ S | PART S')
    grammar.append('PART -> SEG | NOT SEG | NEITHER SEG NOR SEG | BOTH SEG LAND SEG')
    grammar.append('SEG -> DESC | "(" S ")" | "[" S "]" | "{" S "}"')
    grammar.append('DESC -> NON COREWORD | COREWORD | DROPWORD')

    # Negation and conjugation
    grammar.append('CONJ -> AND | OR')
    grammar.append('AND -> LAND | "but" | "with" | "holding" | "wearing"  | "has" | "had"' +
                   ' | "having" | "containing"')
    grammar.append('LAND -> "and"')
    grammar.append('OR -> "or"')
    grammar.append('NOT -> "no" | "not" | "without" | "missing" | "lacking"')
    grammar.append('NON -> "non"')
    grammar.append('BOTH -> "both"')
    grammar.append('NEITHER -> "neither"')
    grammar.append('NOR -> "nor"')

    # Drop words
    grammar.append('DROPWORD -> DET | PRONOUN | ADV | PREP | DVERB | ANON | SET')
    grammar.append('ANON -> "someone" | "somebody" | "people" | "person" | "human"' +
                   ' | "face" | "anyone" | "anybody"')
    grammar.append('DET -> "a" | "an" | "one" | "this" | "some" | "the" | "these"')
    grammar.append('PREP -> "in" | "on" | "of"')
    grammar.append('PRONOUN -> "he" | "she" | "who" | "it" | "they" | "which" | "that"')
    grammar.append('DVERB -> "is" | "was" | "be" | "been" | "being"')
    grammar.append('ADV -> "very" | "really" | "quite" | "understandably" | "noticibly"' +
                   ' | "obviously" | "irritatingly" | "exactly" | "barely"')
    grammar.append('SET -> "pair" "of" | "pairs" "of" | "set" "of"')
    
    # Core words
    grammar.append('COREWORD -> GENDER | RACE | ATTRACTIVE | COLOR | HAIR | PHOTO | ITEMS | FACE')

    # Gender
    grammar.append('GENDER -> PROD_MALE | PROD_FEMALE | PROD_BOY | PROD_GIRL')
    grammar.append('PROD_BOY -> "boy" | "boys"')
    grammar.append('PROD_GIRL -> "girl" | "girls"')
    grammar.append('PROD_MALE -> "male" | "men"')
    grammar.append('PROD_FEMALE -> "female" | "women"')

    grammar.append('ATTRACTIVE -> PROD_ATTRACTIVE | PROD_UNATTRACTIVE')
    grammar.append('PROD_ATTRACTIVE -> "attractive"')
    grammar.append('PROD_UNATTRACTIVE -> "unattractive"')

    # Color / race / hair
    grammar.append('COLOR -> PROD_BLACK | PROD_WHITE | PROD_GRAY | PROD_BLONDE | PROD_BROWN')
    grammar.append('PROD_BLACK -> "black"')
    grammar.append('PROD_WHITE -> "white"')
    grammar.append('PROD_GRAY -> "gray" | "grey"')
    grammar.append('PROD_BLONDE -> "blond" | "blonde" | "yellow"')
    grammar.append('PROD_BROWN -> "brown" | "dark"')

    # Race
    grammar.append('RACE -> PROD_ASIAN | PROD_INDIAN')
    grammar.append('PROD_ASIAN -> "asian"')
    grammar.append('PROD_INDIAN -> "indian"')

    # Hair
    grammar.append('HAIR -> PROD_CURLY | PROD_STRAIGHT | PROD_WAVY | PROD_HAIR | PROD_BALDING | PROD_BALD')
    grammar.append('PROD_CURLY -> "curly"')
    grammar.append('PROD_STRAIGHT -> "straight"')
    grammar.append('PROD_WAVY -> "wavy"')
    grammar.append('PROD_HAIR -> "hair" | "hairline" | "haired"')
    grammar.append('PROD_BALD -> "bald"')
    grammar.append('PROD_BALDING -> "balding" | "receding"')

    # Photo types
    grammar.append('PHOTO -> PROD_PHOTO | PHOTOTYPE')
    grammar.append('PHOTOTYPE -> PROD_POSED | PROD_NOT_POSED | PROD_COLOR | PROD_NOT_COLOR')
    grammar.append('PROD_PHOTO -> "photo" | "image"')
    grammar.append('PROD_POSED -> "posed"')
    grammar.append('PROD_NOT_POSED -> "candid" | "surprise" | "surprised"')
    grammar.append('PROD_COLOR -> "color" | "colored"')
    grammar.append('PROD_NOT_COLOR -> "black" "and" "white"')

    # Items (hats, etc)
    grammar.append('ITEMS -> GLASSES')
    grammar.append('GLASSES -> PROD_GLASSES | PROD_SUNGLASSES')
    grammar.append('PROD_GLASSES -> "glasses"')
    grammar.append('PROD_SUNGLASSES -> "sunglasses"')
    
    # Facial features
    grammar.append('FACE -> PROD_SMILING | PROD_FROWNING | PROD_DOUBLECHIN | PROD_CHUBBY' +
                   ' | PROD_NOT_CHUBBY | PROD_ANGRY')
    grammar.append('PROD_SMILING -> "smiling"')
    grammar.append('PROD_FROWNING -> "frowning"')
    grammar.append('PROD_DOUBLECHIN -> "double" "chin"')
    grammar.append('PROD_CHUBBY -> "chubby"')
    grammar.append('PROD_NOT_CHUBBY -> "skinny"')
    grammar.append('PROD_ANGRY -> "angry"')

    return '\n'.join(grammar)

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
        return (('Female', dnegToScore(neg)))
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

