from os.path import join
from datetime import datetime

from flask import make_response, send_file

from app import app
from app.lib.file import File
from app.view import Router
from app.view import request, render, redirect, flash, jsonify
from app.controller import User
from app.controller import Submission
from app.controller import Challenge

challenge = Router('challenge')

@challenge.route('/', methods=['GET'])
def index():
    return render('challenges.html',
                  challenges=Challenge.formatter(Challenge.index(sort_by=Challenge.model.id, reverse=True),
                                                 target=lambda k, v: isinstance(v, datetime),
                                                 format=lambda v: str(v)[:10]),
                  categories=Challenge.model.categories)


@User.require_permission
@challenge.route('/', methods=['POST'])
def create():
    try:
        instance = Challenge.create({
            'title': request.form.get('challengeTitle'),
            'cate': request.form.get('challengeType'),
            'start': request.form.get('date-from'),
            'due': request.form.get('date-to'),
            'desc': request.files.get('desc', ''),
            'label': request.files.get('label', ''),
            'train': request.files.get('train', ''),
            'test': request.files.get('test', ''),
        })
    except Exception as e:
        flash(str(e))
    finally:
        return redirect(challenge)

@challenge.route('/<cid>', methods=['GET'])
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
    content = Challenge.package(content)
    return render('challenge.html', **{
        'challenge': Challenge.formatter(content,
                                         target=lambda k, v: isinstance(v, datetime),
                                         format=lambda v: str(v)[:10]),
        'ranking': Challenge.get_rankings(cid, not User.current().TA),
        'train': content.get('train'),
        'test': content.get('test'),
    })

@User.require_login
@challenge.route('/<cid>', methods=['POST'])
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

@User.require_permission
@challenge.route('/<cid>', methods=['PUT'])
def update(cid):
    response = {'status': 'ok'}
    try:
        Challenge.update(cid, request.get_json())
    except Exception as e:
        response.update({'status': 'failed', 'error': str(e)})
    finally:
        response.update({'board_role': Challenge.show(cid).board_role})
        return jsonify(response)

@challenge.route('/<cid>', methods=['DELETE'])
def destroy(cid):
    instance = Challenge.delete(cid)
    return redirect(challenge)
