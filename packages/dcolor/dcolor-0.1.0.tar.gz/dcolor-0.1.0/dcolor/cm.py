
class ColorModeMeta(type):
    def __new__(
        metacls,
        cls,
        bases,
        attributes,
    ):
        if "__str__" not in attributes.keys():
            raise AttributeError(
                "ColorModeMeta must be __str__ value"
            )
        if "__call__" not in attributes.keys():
            raise AttributeError(
                "ColorModeMeta must be __call__ value"
            )

        return super().__new__(
            metacls,
            cls,
            bases,
            attributes,
        )

class CMMember(metaclass=ColorModeMeta):
    def __str__(self):
        raise NotImplementedError(
            "__str__ not define"
        )

    def __call__(self):
        raise NotImplementedError(
            "__call__ not define"
        )
