from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.orm import InstrumentedAttribute, Session

from models.post import Post


class FindPostParams:
    def __init__(
        self,
        user_id: int | None = None,
        fields: list[InstrumentedAttribute] | None = None,
    ):
        self.user_id = user_id
        self.fields = fields


def find_post(params: FindPostParams, session: Session) -> Result:
    query = select()
    if params.fields is not None and len(params.fields) > 0:
        query = query.add_columns(*params.fields)
    else:
        for c in Post.__table__.columns:
            query = query.add_columns(getattr(Post, c.key))

    if params.user_id is not None:
        query = query.where(Post.user_id == params.user_id)

    return session.execute(query)


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

class DeletePostParams():
    def __init__(self, post_id: str, user_id: int):
        self.id = post_id
        self.user_id = user_id

def delete_post(params: DeletePostParams, session: Session):
    query = delete(Post).where(Post.id == params.id).where(Post.user_id == params.user_id)

    return session.execute(query)

