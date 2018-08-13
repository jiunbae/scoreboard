from flask import request, render_template, redirect, url_for

from app import app
from app.view import Router
from app.controller import Assignment as controller

assignment = Router('assignment')

def index():
    print (controller.index())
    return render_template('list.html', assignments=controller.index())
assignment.route('/').GET = index

def create():
    instance = controller.create(request.get_json())
    return redirect('/')
assignment.route('/').POST = create

def show(aid):
    content = controller.show(aid)
    # case of assignment not found
    if not content:
        pass
    return render_template('assignment.html', aid=aid, assignment=controller.show(aid))
assignment.route('/<aid>').GET = show

def destroy(aid):
    pass
assignment.route('/<aid>').DELETE = destroy
