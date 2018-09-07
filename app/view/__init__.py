from os.path import join

from flask import Blueprint
from flask import render_template, redirect
from flask import request, Markup, jsonify, flash

from app import app
from app.lib.attrcallback import AttrCallback
from app.controller import default_params

def render(page, **params):
    return render_template(page, **(params.update(default_params()) or params))

class Router(Blueprint):
    s = list()

    def __init__(self, *args, **kwargs):
        name = args[0]
        super().__init__(*args, **{
            'url_prefix': join('/', name),
            'template_folder': join('../', 'templates', name),
            'import_name': name,
            **kwargs
        })
        Router.s.append(self)

    def __str__(self) -> str:
        return self.name

from app.lib.moduletools import import_subclass
__all__ = list(map(lambda x: x.__name__, import_subclass(__path__, Router, locals())))

any(map(app.register_blueprint, Router.s))

@app.route('/')
def index():
    return render('index.html')
