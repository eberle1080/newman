# Author: Chris Eberle <eberle1080@gmail.com>

from debug import *

class ClassifierGeneratorException(Exception):
    """
    There was an error while adding or getting a mapping
    """
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return "Classifier generation error: " + self.reason

class UnsupportedSearch(Exception):
    """
    An unsupported combination of terms were entered.
    """
    def __init__(self, search_desc):
        self.desc = search_desc
    def __str__(self):
        return str(self.desc)

class ClassifierResult(object):
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def name(self):
        return self._name

    def value(self):
        return self._value

class ProductionSymbol(object):
    def __init__(self, name, negate):
        self._name = name.strip().upper()
        self._negate = True if negate else False

    def name(self):
        return self._name

    def negate(self):
        return self._negate

    def negname(self):
        return "1" if self._negate else "0"

class ClassifierGenerator(object):
    """
    Generate classifiers based on production symbols
    """

    def __init__(self):
        """
        Construct a new ClassifierGenerator
        """
        self._mapping = {}

    def _symbols_to_list(self, symbols):
        """
        Convert something with ProductionSymbol objects into
        something a little easier to digest
        """
        if isinstance(symbols, (list, tuple)):
            return [sym for sym in symbols
                    if sym is not None]
        else:
            if symbols is None:
                return []
            return [symbols]

    def _symbols_to_key(self, symbols):
        """
        Create a string from one or more ProductionSymbol objects
        to be used to index into the mapping dictionary.
        """
        if symbols is None:
            return None
        symbols = self._symbols_to_list(symbols)
        tmp = [s.name() + ':' + s.negname() for s in symbols
               if s is not None and len(s.name()) > 0]
        if len(tmp) == 0:
            return None
        tmp.sort()
        return ';'.join(tmp)

    def _get_key(self, symbols):
        """
        Given one or more production symbols, get the key.
        The only way key is None is if symbols is invalid.
        """
        key = self._symbols_to_key(symbols)
        if key is None:
            raise ClassifierGeneratorException('invalid symbol(s)')
        return key

    def add_mapping(self, symbols, classifiers):
        """
        symbols: A tuple of ProductionSymbol objects (or a singular of said type)
        classifiers:
            (1) A callable which accepts a list of ProductionSymbol objects and
                a desperate flag (see the parser for details), and returns a list
                of ClassifierResult objects:

                Example:
                def mapSpecial(syms, desperate):
                    if len(syms) == 1 and syms[0].name == 'PROD_MALE':
                        return ClassifierResult('Male', -1 if syms[0].negate else 1)
                    return None

            (2) A list of ClassifierResult objects to map (or a singular of said type)
        """

        key = self._get_key(symbols)
        if self._mapping.has_key(key):
            raise ClassifierGeneratorException('duplicate mapping: ' + key)

        if callable(classifiers):
            self._mapping[key] = classifiers
        elif isinstance(classifiers, UnsupportedSearch):
            self._mapping[key] = classifiers
        else:
            tmp = []
            if isinstance(classifiers, (list, tuple)):
                for cls in classifiers:
                    if not isinstance(cls, ClassifierResult):
                        raise ClassifierGeneratorException('invalid classifier mapping')
                    tmp.append(cls)
            elif isinstance(classifiers, ClassifierResult):
                tmp = [classifiers]
            else:
                raise ClassifierGeneratorException('invalid classifier mapping')

            self._mapping[key] = tmp

    def get_mapping(self, symbols, desperate):
        """
        Get a mapping for a given set of symbols
        """

        key = self._get_key(symbols)
        if not self._mapping.has_key(key):
            return None

        if callable(self._mapping[key]):
            syms = self._symbols_to_list(symbols)
            classifiers = self._mapping[key](syms, desperate)
            if classifiers is not None and isinstance(classifiers, UnsupportedSearch):
                raise classifiers
        elif isinstance(self._mapping[key], UnsupportedSearch):
            raise self._mapping[key]
        elif isinstance(self._mapping[key], (list, tuple)):
            classifiers = [m for m in self._mapping[key]]

        if classifiers is None:
            return None

        if isinstance(classifiers, (list, tuple)):
            tmp = [cls for cls in classifiers
                   if cls is not None and
                   len(cls.name()) > 0 and
                   cls.value() != 0]
            if len(tmp) == 0:
                return None
            return tmp
        elif isinstance(classifiers, ClassifierResult):
            return [classifiers]

        raise ClassifierGeneratorException('invalid result: ' + str(classifiers))
