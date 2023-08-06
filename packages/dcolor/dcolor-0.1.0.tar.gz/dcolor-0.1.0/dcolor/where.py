from enum import Enum


class ColorWhere(Enum):
    CHARACTER = "38"
    BACKGROUND = "48"


class BaseWhere:

    @property
    def where(self):
        return self._where

    @where.setter
    def where(self, value):
        if not type(value) is ColorWhere:
            raise TypeError(
                "where must be ColorWhere type."
            )
        self._where = value

    def end(self):
        if self.where == ColorWhere.CHARACTER:
            return "\033[;0m"
        elif self.where == ColorWhere.BACKGROUND:
            return "\033[;0m"
        else:
            return None
