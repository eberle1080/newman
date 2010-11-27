# Author: Chris Eberle <eberle1080@gmail.com>

__all__ = ['vocab', 'grammar', 'lookup_classifier']

def vocab_lookup(word, key):
    """
    Get the synset for a word given its lemma key
    """

    import nltk
    from nltk.corpus import wordnet as wn

    if key is not None:
        return (word, wn.lemma_from_key(key).synset)
    else:
        return (word, None)

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

    # Simple words            Word            Lemma

    vocab.append(vocab_lookup('(',            None))
    vocab.append(vocab_lookup('[',            None))
    vocab.append(vocab_lookup('{',            None))
    vocab.append(vocab_lookup('}',            None))
    vocab.append(vocab_lookup(']',            None))
    vocab.append(vocab_lookup(')',            None))

    vocab.append(vocab_lookup('a',            None))
    vocab.append(vocab_lookup('an',           None))
    vocab.append(vocab_lookup('the',          None))
    vocab.append(vocab_lookup('some',         None))
    vocab.append(vocab_lookup('one',          None))
    vocab.append(vocab_lookup('this',         None))
    vocab.append(vocab_lookup('of',           None))
    vocab.append(vocab_lookup('no',           None))
    vocab.append(vocab_lookup('non',          None))
    vocab.append(vocab_lookup('not',          None))
    vocab.append(vocab_lookup('neither',      None))
    vocab.append(vocab_lookup('nor',          None))
    vocab.append(vocab_lookup('without',      None))
    vocab.append(vocab_lookup('or',           None))
    vocab.append(vocab_lookup('in',           None))
    vocab.append(vocab_lookup('and',          None))
    vocab.append(vocab_lookup('with',         None))
    vocab.append(vocab_lookup('has',          None))
    vocab.append(vocab_lookup('his',          None))
    vocab.append(vocab_lookup('her',          None))
    vocab.append(vocab_lookup('having',       None))
    vocab.append(vocab_lookup('is',           None))
    vocab.append(vocab_lookup('person',       None))
    vocab.append(vocab_lookup('people',       None))
    vocab.append(vocab_lookup('someone',      None))
    vocab.append(vocab_lookup('somebody',     None))
    vocab.append(vocab_lookup('human',        'human%3:01:01::'))

    vocab.append(vocab_lookup('who',          None))
    vocab.append(vocab_lookup('image',        None))
    vocab.append(vocab_lookup('visage',       None))
    vocab.append(vocab_lookup('face',         None))
    vocab.append(vocab_lookup('photo',        'photo%1:06:00::'))

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

    # Genders                 Word            Lemma
    vocab.append(vocab_lookup('male',         'man%1:18:00::'))
    vocab.append(vocab_lookup('men',          None))
    vocab.append(vocab_lookup('female',       'woman%1:18:00::'))
    vocab.append(vocab_lookup('women',        None))
    vocab.append(vocab_lookup('girl',         'girl%1:18:02::'))
    vocab.append(vocab_lookup('boy',          'boy%1:18:00::'))

    # Age                     Word            Lemma
    vocab.append(vocab_lookup('child',        'child%1:18:00::'))
    vocab.append(vocab_lookup('baby',         'baby%1:18:00::'))
    vocab.append(vocab_lookup('adult',        'adult%1:18:00::'))
    vocab.append(vocab_lookup('teenager',     'teenager%1:18:00::'))
    vocab.append(vocab_lookup('old',          'old%3:00:02::'))
    vocab.append(vocab_lookup('young',        'young%3:00:00::'))
    vocab.append(vocab_lookup('young',        'youth%1:14:00::'))
    vocab.append(vocab_lookup('senior',       'senior%5:00:00:old:02'))
    vocab.append(vocab_lookup('middle-aged',  'middle-aged%5:00:00:old:02'))
    vocab.append(vocab_lookup('middle',       None))
    vocab.append(vocab_lookup('aged',         None))
    vocab.append(vocab_lookup('age',          None))

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

    return vocab

def grammar():
    """
    This is where we define our grammar
    """

    grammar = []

    # Sentences
    grammar.append('S -> PART | PART CONJ S')
    grammar.append('PART -> SEG | NOT SEG | NEITHER SEG NOR SEG')
    grammar.append('SEG -> DESC | "(" S ")" | "[" S "]" | "{" S "}"')
    grammar.append('DESC -> NP | VP | NP VP | ADV SENT')

    # Negation and conjugation
    grammar.append('CONJ -> AND | OR')
    grammar.append('AND -> "and" | "but" | "with"')
    grammar.append('OR -> "or"')
    grammar.append('NOT -> "no" | "not" | "without"')
    grammar.append('NON -> "non"')
    grammar.append('NEITHER -> "neither"')
    grammar.append('NOR -> "nor"')
    
    # Nouns
    grammar.append('NP -> MNP | MNP P MNP')
    grammar.append('MNP -> DET NOMINAL | NOMINAL | PRONOUN | DET NOMINAL MNP | NOMINAL MNP | PRONOUN MNP')
    grammar.append('DET -> SINGULAR | PLURAL')
    grammar.append('SINGULAR -> "a" | "an" | "one" | "this" | "some" | "the"')
    grammar.append('PLURAL -> "some" | "these"')
    grammar.append('NOMINAL -> NOUN')
    grammar.append('NOUN -> NON N | N | ADJP N')
    grammar.append('PRONOUN -> "he" | "she" | "who" | "it" | "they" | "which" | "that"')
    grammar.append('N -> ANON | GENDER | RACE | PHOTO | ITEMS')

    # Verbs
    grammar.append('VP -> MVP | MVP VP')
    grammar.append('MVP -> NON VERB | VERB NP | VERB')
    grammar.append('VERB -> VB_FACIAL')

    # Adjectives
    grammar.append('ADJP -> ADJ | ADV ADJP')
    grammar.append('ADJ -> "big" | "small" | "red"')
    grammar.append('ADV -> "very" | "really"')

    # Prepositions
    grammar.append('P -> "in" | "on" | "of"')

    # Noun classifiers
    grammar.append('ANON -> "someone" | "somebody" | "people" | "person" | "human" | "face" | "anyone" | "anybody"')

    grammar.append('GENDER -> CLS_MALE | CLS_FEMALE')
    grammar.append('CLS_MALE -> "male" | "men"')
    grammar.append('CLS_FEMALE -> "female" | "women"')

    grammar.append('RACE -> BLACK | CLS_WHITE | CLS_ASIAN | INDIAN')
    grammar.append('BLACK -> CLS_BLACK_HAIR | CLS_BLACK')
    grammar.append('CLS_BLACK_HAIR -> "black" "hair" | "black" "haired"')
    grammar.append('CLS_BLACK -> "black"')
    grammar.append('CLS_WHITE -> "white"')
    grammar.append('CLS_ASIAN -> "asian"')
    grammar.append('CLS_INDIAN -> "indian"')

    grammar.append('PHOTO -> PHOTOWORD | PHOTODESC PHOTOWORD | PHOTODESC')
    grammar.append('PHOTODESC -> PHOTOCLASS | PHOTOCLASS CONJ PHOTODESC')
    grammar.append('PHOTOWORD -> "photo" | "image"')
    grammar.append('PHOTOCLASS -> CLS_POSED | CLS_NOT_POSED | CLS_COLOR | CLS_NOT_COLOR')
    grammar.append('CLS_POSED -> "posed"')
    grammar.append('CLS_NOT_POSED -> "candid"')
    grammar.append('CLS_COLOR -> "color"')
    grammar.append('CLS_NOT_COLOR -> "black" "and" "white"')

    grammar.append('ITEMS -> GLASSES')
    grammar.append('SET -> "pair" "of" | "pairs" "of" | "set" "of"')
    grammar.append('GLASSES -> CLS_GLASSES | SET CLS_GLASSES | SET CLS_SUNGLASSES')
    grammar.append('CLS_GLASSES -> "glasses"')
    grammar.append('CLS_SUNGLASSES -> "sunglasses"')

    # Verb classifiers
    grammar.append('VB_FACIAL -> CLS_SMILING | CLS_FROWNING')
    grammar.append('CLS_SMILING -> "smiling"')
    grammar.append('CLS_FROWNING -> "frowning"')

    # Adjective classifiers
    grammar.append('BODY -> CLS_CHUBBY | CLS_NOT_CHUBBY')
    grammar.append('CLS_CHUBBY -> "chubby"')
    grammar.append('CLS_NOT_CHUBBY -> "skinny"')

    return '\n'.join(grammar)

def lookup_classifier(cls, negate):
    if cls == 'CLS_POSED':
        return ('Posed Photo', -1 if negate else 1)
    elif cls == 'CLS_NOT_POSED':
        return ('Posed Photo', 1 if negate else -1)
    elif cls == 'CLS_COLOR':
        return ('Color Photo', -1 if negate else 1)
    elif cls == 'CLS_NOT_COLOR':
        return ('Color Photo', 1 if negate else -1)
    elif cls == 'CLS_SMILING':
        return ('Smiling', -1 if negate else 1)
    elif cls == 'CLS_FROWNING':
        return ('Frowning', -1 if negate else 1)
    elif cls == 'CLS_MALE':
        return ('Male', -1 if negate else 1)
    elif cls == 'CLS_FEMALE':
        return ('Male', 1 if negate else -1)
    elif cls == 'CLS_CHUBBY':
        return ('Chubby', -1 if negate else 1)
    elif cls == 'CLS_NOT_CHUBBY':
        return ('Chubby', 1 if negate else -1)
    elif cls == 'CLS_GLASSES':
        if negate:
            return ('No Eyewear', 1)
        else:
            return ('Eyeglasses', 1)

    elif cls == 'CLS_SUNGLASSES':
        return ('Sunglasses', -1 if negate else 1)
    elif cls == 'CLS_ASIAN':
        return ('Asian', -1 if negate else 1)
    elif cls == 'CLS_BLACK':
        return ('Black', -1 if negate else 1)
    elif cls == 'CLS_WHITE':
        return ('White', -1 if negate else 1)
    elif cls == 'CLS_ASIAN':
        return ('Asian', -1 if negate else 1)
    elif cls == 'CLS_INDIAN':
        return ('Indian', -1 if negate else 1)

    return (None, 0)
