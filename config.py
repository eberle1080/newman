# Author: Chris Eberle <eberle1080@gmail.com>

__all__ = ['vocab', 'grammar']

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
    vocab.append(vocab_lookup('without',      None))
    vocab.append(vocab_lookup('or',           None))
    vocab.append(vocab_lookup('in',           None))
    vocab.append(vocab_lookup('and',          None))
    vocab.append(vocab_lookup('with',         None))
    vocab.append(vocab_lookup('person',       None))
    vocab.append(vocab_lookup('image',        None))
    vocab.append(vocab_lookup('visage',       None))
    vocab.append(vocab_lookup('face',         None))
    vocab.append(vocab_lookup('photo',        None))

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

    # Genders                 Word            Lemma
    vocab.append(vocab_lookup('male',         'man%1:18:00::'))
    vocab.append(vocab_lookup('female',       'woman%1:18:00::'))
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
    vocab.append(vocab_lookup('sideburns',    None))

    # Race                    Word            Lemma
    vocab.append(vocab_lookup('black',        'black%1:18:00::'))
    vocab.append(vocab_lookup('asian',        'asian%1:18:00::'))
    vocab.append(vocab_lookup('white',        'white%1:18:00::'))
    vocab.append(vocab_lookup('indian',       None))

    # Place                   Word            Lemma
    vocab.append(vocab_lookup('indoor',       'indoor%3:00:00::'))
    vocab.append(vocab_lookup('outdoor',      'outdoors%1:15:00::'))

    # Accessories
    vocab.append(vocab_lookup('wearing',      None))
    vocab.append(vocab_lookup('hat',          'hat%1:06:00::'))
    vocab.append(vocab_lookup('lipstick',     None))
    vocab.append(vocab_lookup('glasses',      'glasses%1:06:00::'))
    vocab.append(vocab_lookup('sunglasses',   None))
    #vocab.append(vocab_lookup('eyewear',      None))
    #vocab.append(vocab_lookup('eyeglasses',   None))

    # Body type               Word            Lemma
    vocab.append(vocab_lookup('attractive',   'attractive%3:00:01::'))
    vocab.append(vocab_lookup('unattractive', 'unattractive%3:00:00::'))
    vocab.append(vocab_lookup('unattractive', 'ugly%3:00:00::'))
    vocab.append(vocab_lookup('chubby',       None))

    # Image features          Word            Lemma
    vocab.append(vocab_lookup('focused',      None))
    vocab.append(vocab_lookup('blurry',       None))
    vocab.append(vocab_lookup('color',        None))
    vocab.append(vocab_lookup('flash',        None))
    vocab.append(vocab_lookup('harsh',        None))
    vocab.append(vocab_lookup('lighting',     None))
    vocab.append(vocab_lookup('posed',        None))
    vocab.append(vocab_lookup('natural',      None))
    vocab.append(vocab_lookup('soft',         None))

    return vocab

def grammar():
    """
    This is where we define our grammar
    """

    grammar = []
    grammar.append('S -> NP | NP CONJ NP')
    grammar.append('CONJ -> "and" | "or" | "with" | "but"')
    

    return '\n'.join(grammar)

