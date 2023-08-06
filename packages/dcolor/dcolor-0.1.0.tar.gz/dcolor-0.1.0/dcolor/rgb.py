import re
from .cm import CMMember
from .where import BaseWhere, ColorWhere

class RGB(CMMember, BaseWhere):
    _MODESTR="rgb"
    def __new__(
        cls,
        *args,
        **kwargs,
    ):
        if len(args) == 0 and len(kwargs) == 0:
            return RGB._MODESTR
        
        return super().__new__(
            cls
        )
    def __init__(
        self,
        rgb,
        where=ColorWhere.CHARACTER,
    ):
        self.rgb = rgb
        self.where = where

    @property
    def rgb(self):
        return (
            self._r,
            self._g,
            self._b
        )

    @rgb.setter
    def rgb(self, value):
        if not isinstance(value, (str, dict, list, tuple)):
            raise TypeError(
                "rbg must be str or dict,list type."
            )
        if isinstance(value, str):
            self._rgb_string(self, value)
        if isinstance(value, dict):
            self._rgb_dict(self, value)
        if isinstance(value, (list, tuple)):
            self._rgb_list(self, value)
    
    @staticmethod
    def _instance(cls):
        # check if the class is an instance
        if type(cls) is type:
            raise ValueError(
                "cls must be instance."
            )

    @staticmethod
    def _rgb_string(cls, value):
        RGB._instance(cls)
        if not isinstance(value, str):
            raise ValueError(
                "value must be str."
                f"now ({type(value)})"
            )
        rgb_strings = re.finditer(
            r"(\w+|.)\s*=\s*\d+\s*,?",
            value,
        )
        for string in rgb_strings:
            if re.search(r"[rR]|[gG]|[bB]", string.group()) is None:
                raise ValueError(
                    f"invalid rgb value.({string.group()}?)"
                    f"now value ({value})"
                )
        devide = re.finditer(
            r"(([rR]|[gG]|[bB])\s*=\s*)?(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(,?)(\s*)",
            value,
        )
        rgb = dict()
        left = list()
        for part in devide:
            string = re.search(
                r"[rR]|[gG]|[bB]",
                part.group(),
            )
            number = re.search(
                r"(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])",
                part.group(),
            )
            number = int(number.group())
            if string is not None:
                _lower = string.group().lower()
                rgb.setdefault(_lower, number)
            else:
                left.append(number)

        if len(rgb) + len(left) != 3:
            raise ValueError(
                "rgb string is invalid value. "
                f"\"R=255,G=255,B=255\".now {value}"
            )
        for i in left:
            for color in "rgb":
                if color in rgb.keys():
                    continue
                rgb.setdefault(color, i)
                break

        RGB._rgb_dict(cls, rgb)

    @staticmethod
    def _rgb_dict(cls, value):
        RGB._instance(cls)
        if not isinstance(value, dict):
            raise ValueError(
                "value must be dict."
                f"now ({type(value)})"
            )
        keys = list(set(value.keys()))
        lower_keys = dict()
        for key in keys:
            if not isinstance(key, str):
                raise TypeError(
                    "RGB dict key must be str type."
                )
            if not isinstance(value[key], int):
                raise TypeError(
                    "RGB dict value must be int type. "
                    f"now {type(value[key])}"
                )
            number = RGB._valid_value(value[key])
            lower_keys[key.lower()] = number

        if len(lower_keys) != 3:
            raise ValueError(
                "rgb dict keys must be 'R', 'G', 'B'. "
                f"now {list(value.keys())}."
            )
        if "r" not in lower_keys or "g" not in lower_keys or \
                "b" not in lower_keys:
            raise KeyError(
                "rgb invalid key."
                f"valid key(r, g, b). "
                f"now ({','.join(keys)})"
            )
        cls._r = lower_keys["r"]
        cls._g = lower_keys["g"]
        cls._b = lower_keys["b"]

    @staticmethod
    def _rgb_list(cls, value):
        RGB._instance(cls)
        if len(value) != 3:
            raise ValueError(
                "rgb list must be [R, G, B]. "
                f"now {value}"
            )
        cls._r = RGB._valid_value(value[0])
        cls._g = RGB._valid_value(value[1])
        cls._b = RGB._valid_value(value[2])
    
    @staticmethod
    def _valid_value(number):
        if not isinstance(number, int):
            raise TypeError(
                "rgb list's element must be int type."
            )
        if number > 255 or number < 0:
            raise ValueError(
                "rgb must be 0~255."
            )
        return number
        

    def __str__(self):
        return "rgb"

    def __call__(self):
        return f"\033[{self.where};2;{self._r}:{self._g}:{self._b}"

