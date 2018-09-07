from app import app
from app.view import Router
from app.view import request, render, redirect, flash
from app.controller import Submission

submission = Router('submission')

@submission.route('/<sid>', methods=['GET'])
def show(sid):
    return render('submission.html', submission=Submission.show(sid))


@submission.route('/<sid>', methods=['DELETE'])
def destroy(sid):
    instance = Submission.delete(sid)
    return redirect('/')

