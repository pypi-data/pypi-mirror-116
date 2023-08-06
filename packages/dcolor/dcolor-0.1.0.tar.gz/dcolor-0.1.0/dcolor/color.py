from .mode import ColorMode
from .where import BaseWhere
from .deco import _decorate_base


class Color(BaseWhere, metaclass=_decorate_base):
    def __init__(
        self,
        color,
        mode,
        where,
    ):
        self.mode = mode
        self._color = color
        self.where = where
    
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, (str, ColorMode)):
            raise TypeError(
                "mode must be str type."
            )
        if isinstance(value, str):
            # check valid mode value
            self._mode = ColorMode.mode(value)
        else:
            self._mode = value

    def __call__(self):
        return self.mode(
            color=self._color,
            where=self.where,
        )()

    def start(self):
        return self.__call__()
