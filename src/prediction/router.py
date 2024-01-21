from fastapi import APIRouter, Depends, UploadFile, status
import pandas as pd
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.Asyncrq import Asyncrq, asyncrq

from src.auth.base_config import current_active_user
from src.database import get_async_session
from src.models import Model, Transaction, User
from arq.jobs import Job

router = APIRouter(prefix="/prediction", tags=["Prediction"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def predict(
    model_name: str,
    file: UploadFile,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Model.id, Model.price).where(Model.name == model_name)
    query_result = await session.execute(query)
    query_result = query_result.mappings().all()[0]
    model_id = query_result["id"]
    model_price = query_result["price"]

    data = pd.read_csv(file.file)
    file.file.close()

    # Отправляем задачу в Redis для того, чтобы worker мог ее исполнить. Возвращаем task_id, он уникальный, по нему можно попросить результат
    # Нужно будет реализовать endpoint /{task_id}
    # В этом endpoint примерно следующий код:
    # j = Job('1234567890 уникальный id', Asyncrq.pool) Создаем экземпляр класса Job с указанием ID и базы
    # await j.status() Можно получить статус (в работе, выполнена, ошибка и тд)
    # await j.result(timeout=3600) Вот тут мы будем дожидаться выполнения максимум 3600 сек, потом кинем ошибку
    # Можно проверять статус и, если задача готова, возвращать результат

    job = await asyncrq.pool.enqueue_job(
        function="predict_on_csv",
        user_id=user.id,
        model_id=model_id,
        model_name=model_name,
        input_data=data,
    )

    stmt_new_balance = (
        update(User.__table__)
        .where(User.__table__.c.id == user.id)
        .values(balance=user.balance - model_price)
    )
    await session.execute(stmt_new_balance)
    await session.commit()

    new_transaction = {
        "amount": model_price,
        "model_id": model_id,
        "user_id": user.id,
        "type": "withdraw",
    }
    stmt_add_trans = insert(Transaction).values(**new_transaction)
    await session.execute(stmt_add_trans)
    await session.commit()

    return {
        "status": "task_queued",
        "task_id": job.job_id,
        "message": "Your task has been successfully queued. You can use the task_id to check the status and retrieve the result later.",
    }
