from flask_login import login_required

from app import app
from app.view import Router
from app.view import request, render, redirect, flash, jsonify
from app.controller import User
from app.controller import Submission

user = Router('user')

@login_required
def profile():
    instance = User.current()
    return render('user.html', submissions=User.submissions())
user.route('/').GET = profile

def create():
    instance = User.create(request.get_json())
    return redirect(user)
user.route('/').POST = create

def change():
    response = {'status': 'ok'}
    try:
        User.update(**request.get_json())
    except Exception as e:
        response.update({'status': 'failed', 'error': str(e)})
    return jsonify(response)
user.route('/').PUT = change

def destroy(uid):
    instance = User.destroy(uid)
    return redirect(user)
user.route('/').DELETE = destroy

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render('login.html', user=User.current())
    elif request.method == 'POST':
        studentid = request.form.get('studentid')
        password = request.form.get('password')
        try:
            instance = User.login(studentid, password)
        except Exception as e:
            flash(str(e))
            return render('login.html')
        return redirect(user)

@app.route('/logout/', methods=['POST'])
@login_required
def logout():
    User.logout()
    return redirect(user)
