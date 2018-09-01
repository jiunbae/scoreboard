from typing import List, Optional

from app import Session
from app import models
from app.controller import Controller

class Post(Controller):
    model = models.Post

    @classmethod
    def index(cls, cate: str, *args: list, **kwargs: dict) -> List[models.Post]:
        if cate not in models.Post.categories:
            raise Exception('Wrong type')
        return super(Post, cls).index(filter_by={'cate': models.Post.categories.index(cate)}, *args, **kwargs)
