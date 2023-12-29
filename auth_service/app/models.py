import ormar
from app.core.db import BaseMeta
from passlib.hash import bcrypt


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "auth"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    login: str = ormar.String(max_length=100, nullable=False, unique=True)
    password: str = ormar.String(max_length=128)
    is_admin: bool = ormar.Boolean(default=False)

    @classmethod
    async def get_user(cls, login):
        return cls.get(login=login)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
