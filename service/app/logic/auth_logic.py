import jwt
import bcrypt
from datetime import datetime, timedelta
from ..db.repository.auth import AuthRepository

SECRET_KEY = "your_jwt_secret_key"
ALGORITHM = "HS256"

class AuthLogic:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    def authenticate_user(self, login: str, password: str):
        user = self.auth_repo.get_user_by_login(login)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        return None

    def create_access_token(self, user_id: int, expires_delta: timedelta = None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)  # Пример времени жизни токена
        to_encode = {"exp": expire, "sub": str(user_id)}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)