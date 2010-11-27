# Author: Chris Eberle <eberle1080@gmail.com>

class ParserException(Exception):
    """
    There was an error during parsing
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Parse error: " + self.reason

class ClassifierCollection(object):
    def __init__(self):
        self._classifiers = []
        self._classifiers.append([])
        self._pos = 0
        self._valid = 0
        self._text = []
    
    def addtext(self, text):
        self._text.append(text)

    def add(self, classifier, score):
        self._classifiers[self._pos].append((classifier, score))

    def next(self):
        if len(self._classifiers[self._pos]) == 0:
            raise ParserException('No classifiers found for text segment: "' + ' '.join(self._text) + '"')
        self._classifiers.append([])
        self._pos += 1
        self._valid += 1
        self._text = []

    def finish(self):
        if len(self._text) > 0 and len(self._classifiers[self._pos]) == 0:
            raise ParserException('No classifiers found for text segment: "' + ' '.join(self._text) + '"')
        elif len(self._classifiers[self._pos]) > 0:
            self._valid += 1
            self._text = []

        if len(self._classifiers) == 0:
            raise ParserException('No classifier words found')

    def valid_count(self):
        return self._valid

    def pprint(self):
        classifiers = []
        for n in xrange(self._valid):
            classifiers.append(', '.join([name + ' => ' + str(score) for (name, score) in self._classifiers[n]]))
        print '(' + ') | ('.join(classifiers) + ')'

def rparse(tree, classifiers, negate, depth = 0):
    import nltk, config

    myneg = negate
    lastneg = myneg

    for tr in tree:
        if isinstance(tr, nltk.Tree):
            val = rparse(tr, classifiers, myneg, depth + 1)
            if val == True:
                lastneg = myneg
                myneg = not myneg
            elif val == False:
                myneg = lastneg
        elif isinstance(tr, basestring):
            name = str(tree.node)
            if name.startswith('CLS_'):
                # Cheap dirty hack so that I know it's a real classifier
                classifier = config.lookup_classifier(name, myneg)
                if(classifier[0] == None):
                    raise ParserException('Unknown grammar classifier: ' + name)
                classifiers.add(classifier[0], classifier[1])
                classifiers.addtext(tr)
            elif name in ('NOT', 'NON', 'NEITHER'):
                classifiers.addtext(tr)
                return True
            elif name == 'NOR':
                classifiers.addtext(tr)
                return True
            elif name == 'OR':
                classifiers.next()
            else:
                classifiers.addtext(tr)

        #print '-' * depth + '> ' + str(myneg)

def parse(wordlist, grammar, debugging):
    """
    Parse this thang
    """

    import nltk

    try:
        gr = nltk.parse_cfg(grammar)
        parts = [w.reduced() for w in wordlist]

        #parser = nltk.RecursiveDescentParser(gr)
        #if debugging:
        #    parser.trace()

        if debugging:
            parser = nltk.BottomUpChartParser(gr, trace = 2)
        else:
            parser = nltk.BottomUpChartParser(gr)
        trees = parser.nbest_parse(parts)

        classifiers = ClassifierCollection()
        for tree in trees:
            rparse(tree, classifiers, False)
            break

        classifiers.finish()
        if classifiers.valid_count() == 0:
            raise ParserException('No parse trees found')

        classifiers.pprint()

    except ValueError, e:
        raise ParserException(str(e))

    return 0
