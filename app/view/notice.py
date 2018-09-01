from app import app
from app.view import Router
from app.view import request, render, redirect, flash
from app.controller import Post
from app.controller import User

notice = Router('notice')

def index():
    return render('notice.html', notices=Post.index(cate='notice'))
notice.route('/').GET = index

@User.require_login
def create():
    return {}

def show(pid):
    return render('notice.html', notices=Post.index(cate='notice'))
notice.route('/<pid>').GET = show

def destroy(pid):
    instance = Post.delete(pid)
    return redirect('/')
notice.route('/<pid>').DELETE = destroy
