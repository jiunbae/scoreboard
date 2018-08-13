import glob
from os.path import dirname, basename, isfile
from typing import Callable
from collections import defaultdict
from urllib.parse import urljoin

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
        view = lambda *args: handler[request.method](*args)
        view.__name__ = str(id(view))
        app.add_url_rule(urljoin('//'+route, url)[1:],
                        view_func = view,
                        methods   = handler.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/site-map")
def site_map():
    print (app.url_map)
    return [(url_for(rule.endpoint, **(rule.defaults or {})), rule.endpoint) for rule in app.url_map.iter.rules()]
