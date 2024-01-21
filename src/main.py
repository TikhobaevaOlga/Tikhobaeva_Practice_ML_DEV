from fastapi import Depends, FastAPI
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware

from src.Asyncrq import asyncrq
from src.models import User

from src.database import create_db_and_tables
from src.auth.base_config import auth_backend, current_active_user, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.prediction.router import router as prediction_router
from src.balance.router import router as balance_router

app = FastAPI(title="Malware Classification App")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(prediction_router)
app.include_router(balance_router)


@app.get("/current_user")
async def show_current_user(user: User = Depends(current_active_user)):
    return {"username": user.username, "email": user.email, "balance": user.balance}


origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "https://localhost:8501",
    "https://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.from_url(url="redis://127.0.0.1:6379")
    await asyncrq.create_pool()
    await create_db_and_tables()
