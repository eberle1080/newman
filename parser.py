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
        self._final = []
        self._pos = 0
        self._valid = 0
        self._text = []
    
    def addtext(self, text):
        self._text.append(text)

    def add(self, classifier, negate):
        self._classifiers[self._pos].append((classifier, negate))

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

        if len(self._classifiers) == 0 or self._valid == 0:
            raise ParserException('No classifier words found')

        self._convert_all()

    def valid_count(self):
        return self._valid

    def pprint(self):
        classifiers = []
        for n in xrange(self._valid):
            classifiers.append(', '.join([name + ' => ' + str(negate) for (name, negate) in self._final[n]]))
        print '(' + ') | ('.join(classifiers) + ')'

    def _gauntlet(self, cls, force):
        import config

        size = len(cls)
        while size >= 1:
            end = len(cls) - size + 1
            for n in range(0, end):
                ret = config.parse(cls[n:size], True if (size <= 1 or force) else False)
                if ret != None:
                    del cls[n:size]
                    return ret
            size -= 1
        return None

    def _extract(self, ret, arr):
        if ret == None:
            return 0
        if isinstance(ret, (list, tuple)):
            if len(ret) == 0:
                return 0
            if isinstance(ret[0], (list, tuple)):
                num = 0
                for item in ret:
                    num += self._extract(item, arr)
                return
            if len(ret) < 2:
                return 0
            arr.append((ret[0], ret[1]))
            return 1
        return 0

    def _convert(self, n):
        arr = self._final[n]
        cls = self._classifiers[n]

        while True:
            ret = self._gauntlet(cls, False)
            if ret == None:
                if len(cls) > 0:
                    ret = self._gauntlet(cls, True)
                    if ret != None:
                        self._extract(ret, arr)
                        continue
                    raise ParserException('Unable to meaningfully parse the production symbols')
                else:
                    return
            else:
                self._extract(ret, arr)

    def _convert_all(self):
        self._final = []
        if self._valid <= 0:
            return
        for n in xrange(self._valid):
            self._final.append([])
            self._convert(n)

def rparse(tree, classifiers, negate, depth = 0):
    import nltk, config

    myneg = negate
    lastneg = myneg

    rv = None
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
            if name.startswith('PROD_'):
                # Cheap dirty hack so that I know it's a real classifier
                classifiers.add(name, myneg)
                classifiers.addtext(tr)
                rv = None
            elif name in ('NOT', 'NON', 'NEITHER'):
                classifiers.addtext(tr)
                myneg = not negate
                rv = True
            elif name == 'NOR':
                classifiers.addtext(tr)
                myneg = not negate
                rv = True
            elif name == 'OR':
                classifiers.next()
            else:
                classifiers.addtext(tr)

    return rv

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

        #if debugging:
        #    parser = nltk.BottomUpChartParser(gr, trace = 2)
        #else:
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
