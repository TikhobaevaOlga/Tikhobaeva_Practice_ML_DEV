from fastapi import APIRouter, Depends, UploadFile
import pandas as pd
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.Asyncrq import asyncrq

from src.auth.base_config import current_active_user
from src.database import get_async_session
from src.models import Model, Transaction, User
from src.prediction.predict import predict_on_csv

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)

@router.post("/")
async def predict(
    model_name: str,
    file: UploadFile,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):  
    query = select(Model.id, Model.price).where(Model.name == model_name)
    query_result = await session.execute(query)
    query_result = query_result.mappings().all()[0]
    model_id = query_result['id']
    model_price = query_result['price']

    data = pd.read_csv(file.file)
    file.file.close()

    #await asyncrq.pool.enqueue_job(
        #'predict_on_csv',
        #user_id=user.id,
        #model_id=model_id,
        #model_name=model_name,
        #input_data=data)
    
    stmt_new_balance = update(User.__table__).where(User.__table__.c.id == user.id).values(balance=user.balance - model_price)
    await session.execute(stmt_new_balance)
    await session.commit()

    new_transaction = {
        'amount': model_price,
        'model_id': model_id,
        'user_id': user.id,
        'type': 'withdraw'
    }
    stmt_add_trans = insert(Transaction).values(**new_transaction)
    await session.execute(stmt_add_trans)
    await session.commit()

    return {'message': 'We are working on your prediction'}