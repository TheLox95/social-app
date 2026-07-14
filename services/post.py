from sqlalchemy import Result, ScalarResult, delete, insert, select, update
from sqlalchemy.orm import InstrumentedAttribute, Session, joinedload, noload

from models.post import Post
from models.post_comment import PostComment
from models.post_like import PostLike


class FindPostParams:
    def __init__(
        self,
        user_id: int | None = None,
        id: str | None = None,
        include_likes: bool = False,
        include_comments: bool = False,
        fields: list[InstrumentedAttribute] | None = None,
    ):
        self.id = id
        self.user_id = user_id
        self.fields = fields
        self.include_likes = include_likes
        self.include_comments = include_comments


def find_post(params: FindPostParams, session: Session) -> ScalarResult[Post] | Result:
    if params.fields is not None and len(params.fields) > 0:
        query = select().options(noload("*"))
        query = query.add_columns(*params.fields)
    else:
        query = select(Post).options(noload("*"))

    if params.include_likes:
        query = query.options(joinedload(Post.likes))

    if params.include_comments:
        query = query.options(joinedload(Post.comments))

    if params.user_id is not None:
        query = query.where(Post.user_id == params.user_id)

    if params.id is not None:
        query = query.where(Post.id == params.id)

    if params.fields is not None and len(params.fields) > 0:
        return session.execute(query)
    else:
        return session.scalars(query).unique()


class CreatePostParams:
    def __init__(self, content: str, user_id: int):
        self.content = content
        self.user_id = user_id


def create_post(params: CreatePostParams, session: Session) -> Result:
    query = insert(Post).values(content=params.content, user_id=params.user_id)
    return session.execute(query)


class UpdatePostParams:
    def __init__(self, content: str, user_id: int, post_id: str):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id


def update_post(params: UpdatePostParams, session: Session) -> Result:
    query = (
        update(Post)
        .where(Post.user_id == params.user_id)
        .where(Post.id == params.post_id)
        .values(content=params.content)
    )
    return session.execute(query)


class DeletePostParams:
    def __init__(self, post_id: str, user_id: int):
        self.id = post_id
        self.user_id = user_id


def delete_post(params: DeletePostParams, session: Session):
    query = (
        delete(Post).where(Post.id == params.id).where(Post.user_id == params.user_id)
    )

    return session.execute(query)


class LikePostParams:
    def __init__(self, post_id: str, author_id: int):
        self.post_id = post_id
        self.author_id = author_id


def like_post(params: LikePostParams, session: Session):
    query = insert(PostLike).values(post_id=params.post_id, author_id=params.author_id)

    return session.execute(query)


class DeleteLikePostParams:
    def __init__(self, post_id: str, author_id: int, like_id: int):
        self.post_id = post_id
        self.like_id = like_id
        self.author_id = author_id


def delete_like_post(params: DeleteLikePostParams, session: Session):
    query = (
        delete(PostLike)
        .where(PostLike.post_id == params.post_id)
        .where(PostLike.author_id == params.author_id)
        .where(PostLike.id == params.like_id)
    )

    return session.execute(query)


class CommentPostParams:
    def __init__(
        self,
        post_id: str,
        author_id: int,
        content: str,
        parent_comment_id: int | None = None,
    ):
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self.parent_comment_id = parent_comment_id


def comment_post(params: CommentPostParams, session: Session):
    query = insert(PostComment).values(
        post_id=params.post_id,
        author_id=params.author_id,
        content=params.content,
        parent_comment_id=params.parent_comment_id,
    )

    return session.execute(query)
