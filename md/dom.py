from abc import ABC, abstractmethod
from typing import Union, List
import collections.abc
import logging
import re


log = logging.getLogger(__name__)

# re's Pattern type (built-in > 3.5)
re.Pattern = type(re.sre_compile.compile('', 0))
# pattern to match whitespace iff followed by newline
_NW_PATTERN = re.compile(r'\A(\s*\n)+', re.MULTILINE)

class DOM:
    def __init__(self):
        # The DOM element tree
        self.content = [] # type: List[Element]

    def __str__(self):
        return self.content.__str__()

    def __repr__(self):
        return '<{0}{1}>'.format(self.__class__.__qualname__, self.__dict__)

class Parsable(ABC):
    @classmethod
    def pattern(cls) -> re.Pattern:
        """Override this method with a regex pattern, including capture groups matching a constructor of this class."""
        raise NotImplementedError

    @classmethod
    def parse(cls, input: List) -> List:
        """Parse input for this type."""
        log.debug('%r.parse: %s', cls, input)
        pass

class Element:
    def __init__(self, value):
        self.values = []
        self._parse_inline(value)

    def _parse_inline(self, input: str):
        input = [input.strip()]
        for valueType in _INLINES:
            input = valueType.parse(input)
        self.values += input

    def __eq__(self, other):
        return self is other or (
            type(self) == type(other) and self.values == other.values)


# Top-level elements, in order of parsing precedence
_ELEMENTS = []
# Inline elements, in order of parsing precedence
_INLINES = []
