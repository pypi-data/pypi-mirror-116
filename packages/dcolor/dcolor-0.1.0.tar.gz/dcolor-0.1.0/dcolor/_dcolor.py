from .where import ColorWhere
from .mode import ColorMode
from .color import Color
from .attr import Attr, AttrList


def _color(
    color,
    mode=ColorMode.NAME.value(),
):
    _color = Color(
        color=color,
        mode=mode,
        where=ColorWhere.CHARACTER,
    )
    return _color

def _check_string(value):
    if not isinstance(value, str):
        raise TypeError(
            "must be string"
        )
    return value

def colors(
    string,
    color,
    mode=ColorMode.NAME.value(),
):
    _cins = _color(
        color=color,
        mode=mode,
    )
    return (
        _cins.start() + \
        _check_string(string) + \
        _cins.end()
    )


def _background(
    color,
    mode=ColorMode.NAME.value(),
):
    _color = Color(
        color=color,
        mode=mode,
        where=ColorWhere.BACKGROUND,
    )
    return _color


def backgrounds(
    string,
    color,
    mode=ColorMode.NAME.value(),
):
    _cins = _background(
        color=color,
        mode=mode,
    )
    return (
        _cins.start() + \
        _check_string(string) + \
        _cins.end()
    )


def attributes(
    string,
    attr,
):
    _attr = Attr(
        kind=attr,
    )
    return (
        _attr.start() + \
        _check_string(string) + \
        _attr.end()
    )
