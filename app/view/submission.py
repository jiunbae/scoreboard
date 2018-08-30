from app import app
from app.view import Router
from app.view import request, render, redirect, flash
from app.controller import Submission

submission = Router('submission')

def show(sid):
    return render('submission.html', submission=Submission.show(sid))
submission.route('/<sid>').GET = show

def destroy(sid):
    instance = Submission.delete(sid)
    return redirect('/')
submission.route('/<sid>').DELETE = destroy
