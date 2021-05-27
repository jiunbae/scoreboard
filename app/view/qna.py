from datetime import datetime

from app import app
from app.view import Router
from app.view import request, render, redirect, flash, Markup
from app.controller import Post
from app.controller import User

qna = Router('qna', template_folder='../templates/post')

@qna.route('/', methods=['GET'])
def index():
    if User.current() == None:
        flash("QnA: Login Required")
        return redirect("/")
    return render('posts.html',
                  uri='qna',
                  post_create=User.current(),
                  posts=Post.index(cate='qna', pack=False))

@User.require_login
@qna.route('/', methods=['POST'])
def create():
    instance = Post.create({
        'title': request.form.get('postTitle'),
        'content': request.form.get('postContent'),
        'cate': 'qna',
        'uid': User.current().id,
    })
    return redirect('/qna/')

@qna.route('/<nid>', methods=['GET'])
def show(nid):
    instance = Post.show(nid)
    return render('post.html',
                  post_edit=instance.user.id == User.current().id,
                  post=Post.formatter(Post.package(instance),
                                      target=lambda k, v: k=='content',
                                      format=lambda v: Markup(Post.render_md(v))))

@qna.route('/<nid>', methods=['DELETE'])
def destroy(nid):
    instance = Post.delete(nid)
    return redirect('/')
