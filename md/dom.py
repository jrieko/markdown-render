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
        output = []
        while input:
            item = input.pop(0)
            if isinstance(item, str):
                # find first match
                parts = cls.pattern().split(item, 1)
                if parts[0]:
                    # prefix of match (full item if no match)
                    log.debug('%r.parse: prefix=%s', cls, parts[0])
                    output.append(parts[0])
                match = parts[1:-1]
                if match:
                    # parsed object
                    log.debug('%r.parse: match=%s', cls, match)
                    output.append(cls(match))
                    if parts[-1]:
                        # trim leading newline-whitespace
                        log.debug('%r: suffix untrimmed: %s', cls, parts[-1])
                        parts[-1] = _NW_PATTERN.sub('', parts[-1], 1)
                        log.debug('%r: suffix trimmed: %s', cls, parts[-1])
                        # suffix of match, return to input for next iteration
                        input.insert(0, parts[-1])
            else:
                # item is already parsed
                output.append(item)
        return output

class Text(Parsable):
    """A text value"""
    _PATTERN = re.compile(r'(.+)', re.DOTALL) # match until end of input

    def __init__(self, match: List[str]):
        self.text = match[0]

    @classmethod
    def pattern(cls) -> re.Pattern:
        return cls._PATTERN

    def __eq__(self, other):
        return self is other or (
            type(self) == type(other) and self.text == other.text)

class Element:
    def __init__(self, value):
        super().__init__()
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

class ParagraphElement(Element, Parsable):
    _PATTERN = re.compile(
        r'\A' # start of input only
        r'(.+?)(?:\n{2,}|\Z)', # match until >= 2 newlines or end of input
        re.MULTILINE | re.DOTALL)

    def __init__(self, match: List[str]):
        super().__init__(match[0])

    @classmethod
    def pattern(cls) -> re.Pattern:
        return cls._PATTERN


# Top-level elements, in order of parsing precedence
_ELEMENTS = [ParagraphElement]
# Inline elements, in order of parsing precedence
_INLINES = [Text]
