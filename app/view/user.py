from flask import request, render_template, redirect
from flask_login import login_required

from app import app
from app.view import Router
from app.controller import User as controller

user = Router('user')

def profile():
    instance = controller.current()
    return redirect('/')
user.route('/').GET = profile

def create():
    instance = controller.create(request.get_json())
    return redirect('/')
user.route('/').POST = create

def destroy(uid):
    instance = controller.destroy(uid)
    return redirect('/')
user.route('/').DELETE = destroy

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        studentid = request.form.get('studentid')
        password = request.form.get('password')
        instance = controller.login(studentid, password)

        # no user registered
        if not instance:
            pass
        return redirect('/')

@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    if request.method == 'GET':
        controller.logout()
        return redirect('/')
