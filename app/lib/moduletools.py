from pkgutil import iter_modules
from os.path import dirname, abspath, relpath, split
import inspect
import sys

def submodules(path):
    for package, module, *_ in iter_modules(path):
        yield package.find_module(module).load_module(module)

def members(module, flag=inspect.isclass):
    yield from inspect.getmembers(module, flag)

def import_subclass(path, base, scope):
    package = list(split(relpath(path[0], dirname(abspath(sys.argv[0])))))
    for module in submodules(path):
        module.__package__ = '.'.join(package)
        module.__name__ = '.'.join(package + [module.__name__])
        sys.modules[module.__name__] = module
        scope[module.__name__] = module
        yield module
        for name, obj in members(module):
            if issubclass(obj, base) and name != base.__name__:
                obj.__module__ = module.__name__
                scope[name] = obj
