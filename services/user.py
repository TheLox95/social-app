
from sqlalchemy import ScalarResult, select
from sqlalchemy.orm import Session

from models.user import User

class FindUsersParams:
    def __init__(self, username: str | None = None, email: str | None = None):
        self.username = username
        self.email = email

async def find_users(params: FindUsersParams, session: Session) -> ScalarResult:
    query = select(User)

    if params.username is not None:
        query = query.where(User.username == params.username)

    if params.email is not None:
        query = query.where(User.email == params.email)

    return session.scalars(query)
