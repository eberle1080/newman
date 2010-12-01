# Author: Chris Eberle <eberle1080@gmail.com>

from generator import *

class ParserException(Exception):
    """
    There was an error during parsing
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Parse error: " + self.reason

class ClassifierCollection(object):
    def __init__(self, generator):
        self._classifiers = []
        self._classifiers.append([])
        self._final = []
        self._pos = 0
        self._valid = 0
        self._text = []
        self._generator = generator
    
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
        for n in xrange(len(self._final)):
            values = []
            for (name, val) in self._final[n]:
                if val > 0:
                    pval = 'Yes'
                else:
                    pval = 'No'
                values.append(name + ' => ' + pval)
            classifiers.append(', '.join(values))
        print '(' + ') | ('.join(classifiers) + ')'

    def _gauntlet(self, cls, desperate):
        import config

        size = len(cls)
        desperate = False

        while size >= 1:
            end = len(cls) - size + 1
            for n in range(0, end):
                # God I love this language
                prods = [ProductionSymbol(p[0], p[1]) for p in cls[n:size+n]]
                ret = self._generator.get_mapping(prods, desperate)
                if ret != None:
                    del cls[n:size+n]
                    return ret
            size -= 1
            if size == 0 and desperate == False:
                size = 1
                desperate = True

        return None

    def _convert(self, n):
        arr = self._final[n]
        cls = self._classifiers[n]

        while True:
            ret = self._gauntlet(cls, False)
            if ret == None:
                if len(cls) > 0:
                    ret = self._gauntlet(cls, True)
                    if ret != None:
                        for r in ret:
                            arr.append(r)
                        continue
                    remaining = '"' + '", "'.join([c[0] for c in cls]) + '"'
                    raise ParserException('Unable to meaningfully parse the production symbols: ' + remaining)
                else:
                    return
            else:
                for r in ret:
                    arr.append(r)

    def _convert_all(self):
        self._final = []
        if self._valid <= 0:
            return
        for n in xrange(self._valid):
            self._final.append([])
            self._convert(n)

        classifiers = []
        for n in xrange(self._valid):
            fc = self._final[n]

            mv = {}
            counter = {}

            for r in fc:
                if not counter.has_key(r.name()):
                    counter[r.name()] = 0
                if not mv.has_key(r.name()):
                    mv[r.name()] = 0

                counter[r.name()] += 1
                mv[r.name()] += r.value()

            keys = mv.keys()
            keys.sort()
            tmp = []
            for k in keys:
                avg = float(mv[k]) / float(counter[k])
                if avg < -0.0001 or avg > 0.0001:
                    tmp.append((k, avg))

            if len(tmp) > 0:
                classifiers.append(tmp)

        self._final = classifiers

def rparse(tree, classifiers, negate, depth = 0):
    import nltk, config

    myneg = negate
    lastneg = myneg

    rv = None
    for tr in tree:
        if isinstance(tr, nltk.Tree):
            name = str(tr.node)

            debug('.'*depth + name + " (negate = " + str(myneg) + ")")
            val = rparse(tr, classifiers, myneg, depth + 1)

            if val == True:
                myneg = not myneg

        elif isinstance(tr, basestring):
            name = str(tree.node)
            if name.startswith('PROD_'):
                # Cheap dirty hack so that I know it's a real classifier
                debug('.'*depth + "Production symbol: " + name + " (negate = " + str(myneg) + ")")
                classifiers.add(name, myneg)
                classifiers.addtext(tr)

            elif name in ('NOT', 'NON', 'NEITHER'):
                debug('.'*depth + 'NEGATE')
                classifiers.addtext(tr)
                myneg = not negate
                rv = True

            elif name == 'NOR':
                debug('.'*depth + 'NEGATE')
                classifiers.addtext(tr)
                myneg = not negate
                rv = True

            elif name == 'OR':
                debug('.'*depth + 'OR')
                classifiers.next()

            else:
                debug('.'*depth + str(tr)+ " (negate = " + str(myneg) + ")")
                classifiers.addtext(tr)

    return rv

def parse(wordlist, grammar, generator):
    """
    Parse this thang
    """

    import nltk

    try:
        gr = nltk.parse_cfg(grammar)
        parts = [w.reduced() for w in wordlist]

        #if debugging:
        #parser = nltk.BottomUpChartParser(gr, trace = 2)
        #else:
        parser = nltk.BottomUpChartParser(gr)

        trees = parser.nbest_parse(parts)

        classifiers = ClassifierCollection(generator)
        ct = 0
        for tree in trees:
            print tree
            rparse(tree, classifiers, False)
            ct += 1
            break

        if ct == 0:
            raise ParserException('No parse trees found')

        classifiers.finish()
        classifiers.pprint()

    except ValueError, e:
        raise ParserException(str(e))

    return 0
