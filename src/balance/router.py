from fastapi import APIRouter, Depends, UploadFile
import pandas as pd
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_active_user
from src.database import get_async_session
from src.models import Transaction, User

router = APIRouter(
    prefix="/balance",
    tags=["Balance"]
)

@router.get("/")
async def check_balance(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User.balance).where(User.id == user.id)
    query_result = await session.execute(query)
    current_user_balance = query_result.mappings().all()[0]['balance']
    return {'message': f'Your current balance is {current_user_balance}'}

@router.post("/")
async def replenish_balance(
    amount: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):  
    stmt_replenish_balance = update(User.__table__).where(User.__table__.c.id == user.id).values(balance=user.balance + amount)
    await session.execute(stmt_replenish_balance)
    await session.commit()

    new_transaction = {
        'amount': amount,
        'user_id': user.id,
        'type': 'replenish'
    }
    stmt_add_trans = insert(Transaction).values(**new_transaction)
    await session.execute(stmt_add_trans)
    await session.commit()

    return {'message': f'Your balance were replenished on {amount}'}

@router.get("/transaction_history")
async def transaction_history(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(Transaction.__table__).where(Transaction.__table__.c.user_id == user.id)
    query_result = await session.execute(query)
    user_transaction_history = query_result.mappings().all()
    return user_transaction_history