# Author: Chris Eberle <eberle1080@gmail.com>

class ParserException(Exception):
    """
    There was an error during parsing
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Parse error: " + self.reason

def parse(wordlist, grammar, debugging):
    """
    Parse this thang
    """

    import nltk

    try:
        gr = nltk.parse_cfg(grammar)
        parts = [w.reduced() for w in wordlist]
        #parser = nltk.ChartParser(gr)        
        parser = nltk.RecursiveDescentParser(gr)
        if debugging:
            parser.trace()
        trees = parser.nbest_parse(parts)
        ct = 0
        for tree in trees:
            print tree
            ct += 1
        if ct == 0:
            raise ParserException('No parse trees found')

    except ValueError, e:
        raise ParserException(str(e))

    return 0
