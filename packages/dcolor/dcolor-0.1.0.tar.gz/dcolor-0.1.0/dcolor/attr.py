from enum import Enum
from .deco import _decorate_base


class AttrList(Enum):
    bold = {
        "name": "bold",
        "number": 1,
    }
    dim = {
        "name": "dim",
        "number": 2,
    }
    italic = {
        "name": "italic",
        "number": 3,
    }
    underline = {
        "name": "underline",
        "number": 4,
    }
    blink = {
        "name": "blink",
        "number": 5,
    }
    reverse = {
        "name": "reverse",
        "number": 6,
    }
    hide = {
        "name": "hide",
        "number": 7,
    }
    strike = {
        "name": "strikethrough",
        "number": 8,
    }


class Attr(metaclass=_decorate_base):
    def __init__(
        self,
        kind,
    ):
        self.kind = kind

    @property
    def kind(self):
        return self._kind

    def _kindstr(self, value):
        for x in AttrList:
            if x.value["name"] == value:
                return x
        raise ValueError(
            "invalid kind value. "
            f"valid value(','.join([x.value for x in AttrList]))"
            f"now \"{value}\""
        )
        
    @kind.setter
    def kind(self, value):
        if not isinstance(value, (str, AttrList)):
            raise TypeError(
                "kind must be str or AttrList."
            )
        if isinstance(value, AttrList):
            self._kind = value
        else:
            self._kind = self._kindstr(value)

    def __call__(self):
        return f"\033[{self.kind.value['number']}m"

    def start(self):
        return self.__call__()

    def end(self):
        return "\033[0m"

