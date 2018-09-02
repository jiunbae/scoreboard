from datetime import datetime

from app import app
from app.view import Router
from app.view import request, render, redirect, flash, Markup
from app.controller import Post
from app.controller import User

notice = Router('notice')

def index():
    return render('posts.html', uri=str(notice), posts=Post.index(cate='notice', pack=False))
notice.route('/').GET = index

@User.require_permission
def create():
    instance = Post.create({
        'title': request.form.get('postTitle'),
        'content': request.form.get('postContent'),
        'cate': 'notice',
        'uid': User.current().id,
    })
    return redirect(notice)
notice.route('/').POST = create

def show(nid):
    return render('post.html', post=Post.formatter(Post.show(nid, pack=True),
                                                   target=lambda k, v: k=='content',
                                                   format=lambda v: Markup(Post.render_md(v))))

notice.route('/<nid>').GET = show

def destroy(nid):
    instance = Post.delete(nid)
    return redirect('/')
notice.route('/<nid>').DELETE = destroy
