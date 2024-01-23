import os
import pickle
import pandas as pd
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.auth.base_config import current_active_user
from src.models import Prediction, Transaction, User
from typing import Dict, Any

MODELS_PATH = "src/prediction/ml_predictors"


async def predict_on_csv(
    ctx: Dict[str, Any],
    user,
    model_id: int,
    model_name: str,
    model_price: int,
    input_data: pd.DataFrame,
):
    if os.path.exists(MODELS_PATH):
        model = pickle.load(open(f"{MODELS_PATH}/{model_name}.pkl", "rb"))
    result = model.predict(input_data)

    new_prediction = {
        "predicted_labels": (", ").join([str(x) for x in result]),
        "model_id": model_id,
        "user_id": user.id,
    }

    async for session in get_async_session():
        new_prediction = Prediction(
            predicted_labels=(", ").join([str(x) for x in result]),
            model_id=model_id,
            user_id=user.id,
        )
        session.add(new_prediction)
        await session.commit()

        stmt_new_balance = (
            update(User.__table__)
            .where(User.__table__.c.id == user.id)
            .values(balance=user.balance - model_price)
        )
        await session.execute(stmt_new_balance)
        await session.commit()

        new_transaction = Transaction(
            amount=model_price,
            user_id=user.id,
            type="withdraw",
            model_id=model_id,
            prediction_id=new_prediction.id
        )
        session.add(new_transaction)
        await session.commit()

    return result
