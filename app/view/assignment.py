from flask import make_response
from flask_login import login_required

from app import app
from app.view import Router
from app.view import request, render, redirect
from app.models import Assignment as model
from app.controller import User
from app.controller import Submission
from app.controller import Assignment

assignment = Router('assignment')

def index():
    return render('assignments.html', assignments=reversed(Assignment.index()), categories=model.categories)
assignment.route('/').GET = index

@User.permission_required
def create():
    label, file = request.files.getlist("file")

    instance = Assignment.create({
        'title': request.form.get('assignmentTitle'),
        'cate': request.form.get('assignmentType'),
        'start': request.form.get('date-from'),
        'due': request.form.get('date-to'),
        'file': Assignment.write_file(file),
        'label': Assignment.write_file(label),
    })
    return redirect('/')
assignment.route('/').POST = create

def show(aid):
    content = Assignment.show(aid)
    if not content:
        return redirect('/')
    if request.args.get('raw', False):
        with open(Assignment.get_file_path(content.file), 'rb') as binary:
            response = make_response(binary.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=%s.pdf'%content.file
        return response
    return render('assignment.html', assignment=content, rankings=Assignment.get_rankings(aid), file='./{}?raw=True'.format(aid))
assignment.route('/<aid>').GET = show

@login_required
def submit(aid):
    file = request.files['file']
    instance = Submission.create({
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
