# NEWMAN: Natural English With Mutating Abridged Nouns
#
# Copyright 2010 Chris Eberle <eberle1080@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You don't even want to know how many dragons be here. Like, 8.

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
    """
    A classifier name and value pair
    (i.e. Male => 1)
    """

    def __init__(self, name, value):
        self._name = name
        self._value = value

    def name(self):
        """
        The final classifier name
        """
        return self._name

    def value(self):
        """
        The final classifer value
        """
        return self._value

class ProductionSymbol(object):
    """
    Used to identify a production symbol coupled
    with a particular negation value. E.g.

    "not male" would be:
        ps = ProductionSymbol('PROD_MALE', True)
    """

    def __init__(self, name, negate):
        """
        Create a new ProductionSymbol object
        """
        self._name = name.strip().upper()
        self._negate = True if negate else False

    def name(self):
        """
        Get the production name
        """
        return self._name

    def negate(self):
        """
        Is this production being negated?
        """
        return self._negate

    def negname(self):
        """
        Used for generating hashes. Don't worry about it.
        """
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
            # It's a lambda expression or something, just add it with no further processing
            self._mapping[key] = classifiers
        elif isinstance(classifiers, UnsupportedSearch):
            # This particular combination is not allowed. So noted.
            self._mapping[key] = classifiers
        else:
            # We've got a list of classifiers. Put them into a list.
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
        Get a mapping for a given set of symbols. Returns None if there is
        no valid mapping (which may change depending on the value of desperate)
        OR returns a list of ClassifierResult objects.
        """

        key = self._get_key(symbols)
        if not self._mapping.has_key(key):
            return None

        if callable(self._mapping[key]):
            # Let the function decide what to do
            syms = self._symbols_to_list(symbols)
            classifiers = self._mapping[key](syms, desperate)

            # It returned an UnsupportedSearch exception... run away!
            if classifiers is not None and isinstance(classifiers, UnsupportedSearch):
                raise classifiers

        elif isinstance(self._mapping[key], UnsupportedSearch):
            # We were told not to allow this combination. Now suffer my wrath.
            raise self._mapping[key]

        elif isinstance(self._mapping[key], (list, tuple)):
            # We've got a list of classifiers to return
            classifiers = [m for m in self._mapping[key]]

        # None just means no mapping found
        if classifiers is None:
            return None

        # OK, we've got something to return. Wrap it up all nice and purdy.
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
