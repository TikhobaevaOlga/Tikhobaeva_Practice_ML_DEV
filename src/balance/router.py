from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_active_user
from src.database import get_async_session
from src.models import Transaction, User

router = APIRouter(
    prefix="/balance",
    tags=["Balance"]
)

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