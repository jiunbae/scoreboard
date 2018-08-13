import glob
from os.path import dirname, basename, isfile

from app import app

class Router:
    class REST:
        def __init__(self, routes):
            self.routes = routes
            self.url = None

        def __setattr__(self, method, handler):
            if method in ['get', 'post', 'put', 'delete']:
                self.routes[self.url] = (method, handler)
            else:
                super(Router.REST, self).__setattr__(method, handler)

    def __init__(self, route: str = ''):
        self.routes = dict()
        self.setter = Router.REST(self.routes)

    def route(self, url):
        self.setter.url = url
        return self.setter

files = glob.glob(dirname(__file__) + "/*.py")
modules = map(basename, filter(lambda f: isfile(f) and not f.startswith('__'), files))
__all__ = list(map(lambda f: f.split('.')[0], modules))

@app.route('/')
def index():
    return render_template('index.html')
