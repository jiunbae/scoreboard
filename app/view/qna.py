from datetime import datetime

from app import app
from app.view import Router
from app.view import request, render, redirect, flash, Markup
from app.controller import Post
from app.controller import User

qna = Router('qna')

def index():
    return render('posts.html', uri='qna', posts=Post.index(cate='qna', pack=False))
qna.route('/').GET = index

@User.require_login
def create():
    instance = Post.create({
        'title': request.form.get('postTitle'),
        'content': request.form.get('postContent'),
        'cate': 'qna',
        'uid': User.current().id,
    })
    return redirect(qna)
qna.route('/').POST = create

def show(nid):
    return render('post.html', post=Post.formatter(Post.show(nid, pack=True),
                                                   target=lambda k, v: k=='content',
                                                   format=lambda v: Markup(Post.render_md(v))))

qna.route('/<nid>').GET = show

def destroy(nid):
    instance = Post.delete(nid)
    return redirect('/')
qna.route('/<nid>').DELETE = destroy
