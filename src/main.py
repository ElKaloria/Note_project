from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.auth.schemas import UserRead, UserCreate
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.database import User
from src.note_app.routers import router as note_app_router

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.include_router(note_app_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)