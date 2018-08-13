import glob
from os.path import dirname, basename, isfile

files = glob.glob(dirname(__file__) + "/*.py")
modules = map(basename, filter(lambda f: isfile(f) and not f.startswith('__'), files))
__all__ = list(map(lambda f: f.split('.')[0], modules))

from app.controller.assignment import Assignment
