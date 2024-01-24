from fastapi import APIRouter, Depends, UploadFile, status
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.Asyncrq import asyncrq

from src.auth.base_config import current_active_user
from src.database import get_async_session
from src.models import Model, User
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

    job = await asyncrq.pool.enqueue_job(
        function="predict_on_csv",
        user=user,
        model_id=model_id,
        model_name=model_name,
        model_price=model_price,
        input_data=data,
    )

    return {
        "status": "task_queued",
        "task_id": job.job_id,
        "message": "Your task has been successfully queued. You can use the task_id to check the status and retrieve the result later.",
    }


@router.get("/{job_id}")
async def get_prediction_result(
    job_id: str,
    user: User = Depends(current_active_user),
):
    job = Job(job_id, asyncrq.pool)
    if await job.status() != "complete":
        status = await job.status()
        return {"status": str(status)}
    else:
        result = await job.result(timeout=20)
        return {"result": str(result)}
