__all__ = ('item_default_val',)


def item_default_val(**default_values):
    """为item的field加入默认值"""

    def wrapper(cls):

        def __init__(self, *args, **kwargs):
            for k, v in default_values.items():
                kwargs.setdefault(k, v if not callable(v) else v())
            super(cls, self).__init__(*args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper