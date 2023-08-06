from .cm import CMMember
from .where import BaseWhere, ColorWhere

class Index(CMMember, BaseWhere):
    _MODESTR="index"
    def __new__(
        cls,
        *args,
        **kwargs
    ):
        if len(args) == 0 and len(kwargs) == 0:
            return Index._MODESTR
        
        return super().__new__(
            cls
        )

    def __init__(
        self,
        index,
        where=ColorWhere.CHARACTER,
    ):
        self.index = index
        self.where = where

    def __str__(self):
        return "index"

    @staticmethod
    def index_string(index, where):
        return f"\033[;{where.value};5;{index}m"

    def __call__(self):
        return self.index_string(
            index=self.index,
            where=self.where,
        )

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "index must be int type."
            )
        if value > 255 or value < 0:
            raise ValueError(
                "index must be 0~255(int)."
            )
        self._index = value
