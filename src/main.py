from fastapi import Depends, FastAPI
import aioredis

from src.Asyncrq import asyncrq
from src.models import User

from src.database import create_db_and_tables
from src.auth.base_config import auth_backend, current_active_user, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.prediction.router import router as prediction_router

app = FastAPI(
    title="Malware Classification App"
)

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

app.include_router(prediction_router)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.username}!"}

@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.from_url(url="redis://localhost")
    await asyncrq.create_pool()
    await create_db_and_tables()