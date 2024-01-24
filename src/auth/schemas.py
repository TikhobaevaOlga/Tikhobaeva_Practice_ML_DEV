from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    balance: int
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str
