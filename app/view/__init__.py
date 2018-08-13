import glob
from os.path import dirname, basename, isfile
from typing import Callable
from collections import defaultdict

from app import app
from app.lib.attrcallback import AttrCallback

class Router:
    routers = list()

    def __init__(self, route: str = ''):
        self.routes = defaultdict(dict)
        self.url = None
        self.attr = AttrCallback(self.setter, ['get', 'post', 'put', 'delete'])
        Router.routers.append((route, self.routes))

    def setter(self, method: str, handler: Callable) -> None:
        self.routes[self.url][method] = handler

    def route(self, url) -> AttrCallback:
        self.url = url
        return self.attr

# import submodule of view
files = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f).split('.')[0] for f in files if isfile(f) and not f.startswith('__')]

@app.route('/')
def index():
    return render_template('index.html')
