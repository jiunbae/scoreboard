from datetime import datetime

from app import app
from app.view import Router
from app.view import request, render, redirect, flash, Markup
from app.controller import Post
from app.controller import User

notice = Router('notice', template_folder='../templates/post')

@notice.route('/', methods=['GET'])
def index():
    if User.current() == None:
        flash("Notice: Login Required")
        return redirect("/")
    return render('posts.html',
                  uri=str(notice),
                  post_create=User.current().TA,
                  posts=Post.index(cate='notice', pack=False))

@User.require_permission
@notice.route('/', methods=['POST'])
def create():
    instance = Post.create({
        'title': request.form.get('postTitle'),
        'content': request.form.get('postContent'),
        'cate': 'notice',
        'uid': User.current().id,
    })
    return redirect("/notice/")

@notice.route('/<nid>', methods=['GET'])
def show(nid):
    return render('post.html',
                  post_edit=User.current().TA,
                  post=Post.formatter(Post.show(nid, pack=True),
                                      target=lambda k, v: k=='content',
                                      format=lambda v: Markup(Post.render_md(v))))

@notice.route('/<nid>', methods=['DELETE'])
def destroy(nid):
    instance = Post.delete(nid)
    return redirect('/')
