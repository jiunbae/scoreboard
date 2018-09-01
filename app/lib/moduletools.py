import inspect
from pkgutil import iter_modules

def submodules(path):
    for package, module, *_ in iter_modules(path):
        yield package.find_module(module).load_module(module)

def members(module, flag=inspect.isclass):
    yield from inspect.getmembers(module, flag)

def import_subclass(path, base, scope):
    for module in submodules(path):
        yield module
        for name, obj in members(module):
            if issubclass(obj, base) and name != base.__name__:
                scope[name] = obj
