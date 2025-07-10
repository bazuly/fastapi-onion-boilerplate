# This code snippet is setting up user authentication and authorization using FastAPI and FastAPI
# Users library. Here's a breakdown of what each part is doing:
import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport

from app.users.auth.core.security import get_jwt_strategy
from app.users.auth.models import User
from .user_dependency import get_user_manager

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
