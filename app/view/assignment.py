from flask_login import login_required

from app import app
from app.view import Router
from app.view import request, render, redirect
from app.controller import User
from app.controller import Submission
from app.controller import Assignment

assignment = Router('assignment')

def index():
    return render('assignments.html', assignments=reversed(Assignment.index()))
assignment.route('/').GET = index

def create():
    instance = Assignment.create(request.get_json())
    return redirect('/')
assignment.route('/').POST = create

def show(aid):
    content = Assignment.show(aid)
    # case of assignment not found
    if not content:
        pass
    return render('assignment.html', aid=aid, assignment=Assignment.show(aid))
assignment.route('/<aid>').GET = show

@login_required
def submit(aid):
    file = request.files['file']
    submission = Submission.create({
        'desc': request.form.get('description'),
        'file': Submission.write_file(file),
        'aid': Assignment.show(aid).id,
        'uid': User.current().id,
    })
    return redirect('/')
assignment.route('/<aid>').POST = submit

def destroy(aid):
    instance = Assignment.delete(aid)
    return redirect('/')
assignment.route('/<aid>').DELETE = destroy
