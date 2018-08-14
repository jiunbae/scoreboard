from flask import request, render_template, redirect
from flask_login import login_required

from app import app
from app.view import Router
from app.controller import Assignment as controller

assignment = Router('assignment')

def index():
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

def submit(aid):
    data = request.form['description']
    file = request.files['file']
    print (data, file)
    return redirect('/')
assignment.route('/<aid>').POST = submit

def destroy(aid):
    instance = controller.delete(aid)
    return redirect('/')
assignment.route('/<aid>').DELETE = destroy
