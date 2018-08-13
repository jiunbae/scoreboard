import glob
from os.path import dirname, basename, isfile
from typing import Callable
from collections import defaultdict
from urllib.parse import urljoin
from functools import partial 

from flask import render_template, request

from app import app
from app.lib.attrcallback import AttrCallback

class Router:
    routers = list()
    def __init__(self, route: str = '/'):
        self.routes = defaultdict(dict)
        self.url = None
        self.attr = AttrCallback(self.setter, ['GET', 'POST', 'PUT', 'DELETE'])
        Router.routers.append((route, self.routes))

    def setter(self, method: str, handler: Callable) -> None:
        self.routes[self.url][method] = handler

    def route(self, url: str = '/') -> AttrCallback:
        self.url = url
        return self.attr

# import submodule of view
files = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f).split('.')[0] for f in files if isfile(f) and not f.startswith('__')]

from app.view.assignment import assignment

for route, router in Router.routers:
    for url, handler in router.items():
        view = partial(lambda h, *args, **kwargs: h[request.method](*args, **kwargs), handler)
        name = urljoin('//'+route, url)[1:]
        view.__name__ = view.__qualname__ = '_route_' + name
        app.route(name, methods=handler.keys())(view)

@app.route('/')
def index():
    return render_template('index.html')
