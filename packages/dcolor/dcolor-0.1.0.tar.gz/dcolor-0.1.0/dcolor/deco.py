
def _decorate_base(
    metacls,
    bases,
    attributes,
    **kwargs,
):
    all_attributes = set()
    all_attributes |= set(attributes.keys())
    for base in bases:
        all_attributes |= \
            set(base.__dict__.keys())

    if "__call__" not in all_attributes:
        raise NotImplementedError(
            "decorate function must have __call__ function."
        )
    if "start" not in all_attributes:
        raise NotImplementedError(
            "decorate function must have start function."
        )
    if "end" not in all_attributes:
        raise NotImplementedError(
            "decorate function must have end function."
        )
    cls = type(metacls, bases, attributes, **kwargs)
    return cls
