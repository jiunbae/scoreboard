from typing import Callable, List, Any

class AttrCallback:
    def __init__(self, setter: Callable = None, getter: Callable = None, attrs: List = None):
        self._attrs = attrs or list()
        self._setter = setter or (lambda: None)
        self._getter = getter or (lambda: None)

    def __setattr__(self, attr: str, value: Any):
        if not attr.startswith('_') and (not self._attrs or attr in self._attrs):
            self._setter(attr, value)
        else:
            super(AttrCallback, self).__setattr__(attr, value)

    def __getattr__(self, attr: str):
        if not attr.startswith('_') and (not self._attrs or attr in self._attrs):
            return self._getter(attr)
        else:
            return super(AttrCallback, self).__getattr__(attr)
