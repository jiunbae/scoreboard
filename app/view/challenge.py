from os.path import join
from datetime import datetime

from flask import make_response, send_file
from flask_login import login_required

from app import app
from app.lib.file import File
from app.view import Router
from app.view import request, render, redirect, flash
from app.controller import User
from app.controller import Submission
from app.controller import Challenge

challenge = Router('challenge')

def index():
    return render('challenges.html',
                  challenges=Challenge.formatter(Challenge.index(sort_by=Challenge.model.id, reverse=True),
                                                 target=lambda k, v: isinstance(v, datetime),
                                                 format=lambda v: str(v)[:10]),
                  categories=Challenge.model.categories)
challenge.route('/').GET = index

@User.permission_required
def create():
    try:
        instance = Challenge.create({
            'title': request.form.get('challengeTitle'),
            'cate': request.form.get('challengeType'),
            'start': request.form.get('date-from'),
            'due': request.form.get('date-to'),
            'desc': request.files.get('desc'),
            'label': request.files.get('label'),
            'train': request.files.get('train'),
            'test': request.files.get('test'),
        })
    except Exception as e:
        flash(str(e))
    finally:
        return redirect(challenge)
challenge.route('/').POST = create

def show(cid):
    content = Challenge.show(cid)
    if not content:
        return redirect('/')
    if 'raw' in request.args:
        cate = request.args.get('raw')
        if cate == 'description':
            response = make_response(File(Challenge.model.directory, content.desc).read('rb'))
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=%s.pdf'%content.desc
            return response
        else:
            file = File(Challenge.model.directory, getattr(content, cate))
            return send_file(join('..', str(file)),\
                             as_attachment=True, attachment_filename='{}.{}'.format(cate, file.ext))
    return render('challenge.html', **{
        'challenge': Challenge.formatter(Challenge.package(content),
                                         target=lambda k, v: isinstance(v, datetime),
                                         format=lambda v: str(v)[:10]),
        'rankings': Challenge.get_rankings(cid),
        'desc': './{}?raw=description'.format(cid),
        'train': './{}?raw=train'.format(cid),
        'test': './{}?raw=test'.format(cid),
    })
challenge.route('/<cid>').GET = show

@login_required
def submit(cid):
    try:
        instance = Submission.create({
            'desc': request.form.get('description'),
            'file': request.files.get('file'),
            'cid': Challenge.show(cid).id,
            'uid': User.current().id,
        })
    except Exception as e:
        flash(str(e))
    return redirect(challenge)
challenge.route('/<cid>').POST = submit

def destroy(cid):
    instance = Challenge.delete(cid)
    return redirect(challenge)
challenge.route('/<cid>').DELETE = destroy
