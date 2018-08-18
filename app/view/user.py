from flask_login import login_required

from app import app
from app.view import Router
from app.view import request, render, redirect, flash
from app.controller import User as controller

user = Router('user')

@login_required
def profile():
    instance = controller.current()
    return render('user.html', submissions=instance.submissions)
user.route('/').GET = profile

def create():
    instance = controller.create(request.get_json())
    return redirect('/')
user.route('/').POST = create

def change():
    instance = controller.current()
    return redirect('/')
user.route('/').PUT = change

def destroy(uid):
    instance = controller.destroy(uid)
    return redirect('/')
user.route('/').DELETE = destroy

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render('login.html', user=controller.current())
    elif request.method == 'POST':
        studentid = request.form.get('studentid')
        password = request.form.get('password')
        instance = controller.login(studentid, password)

        if not instance:
            flash('Not registered!')
            flash('Not registered!')
            flash('Not registered!')
            return render('login.html')
        return redirect('/')

@app.route('/logout/', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        controller.logout()
        return redirect('/')
