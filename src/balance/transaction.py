from sqlalchemy import update, insert
from src.auth.base_config import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi import Depends

from src.models import Transaction, User

async def withdraw_credits(
        price: int, model_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
    ):
    stmt_new_balance = update(User.__table__).where(User.__table__.c.id == user.id).values(balance=user.balance - price)
    await session.execute(stmt_new_balance)
    await session.commit()

    new_transaction = {
        'amount': price,
        'model_id': model_id,
        'user_id': user.id,
        'type': 'withdraw'
    }
    stmt_add_trans = insert(Transaction).values(**new_transaction)
    await session.execute(stmt_add_trans)
    await session.commit()