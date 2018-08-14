from flask import request, render_template, redirect, url_for

from app import app
from app.view import Router
from app.controller import Submission as controller

submission = Router('submission')

def create():
    instance = controller.create(request.get_json())
    return redirect('/')
submission.route('/').POST = create

def destroy(sid):
    instance = controller.delete(sid)
    return redirect('/')
submission.route('/<sid>').DELETE = destroy
