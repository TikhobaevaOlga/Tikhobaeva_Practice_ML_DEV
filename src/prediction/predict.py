from datetime import datetime
import os
import pickle
import pandas as pd
from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.models import Prediction

MODELS_PATH = 'src/prediction/ml_predictors'

async def predict_on_csv(user_id: int, model_id: int, model_name: str, input_data: pd.DataFrame, session: AsyncSession = Depends(get_async_session)):
    if os.path.exists(MODELS_PATH):
        model = pickle.load(open(f"{MODELS_PATH}/{model_name}.pkl", "rb"))
    result = model.predict(input_data)

    new_prediction = {
        'predicted_labels': (', ').join(result),
        'model_id': model_id,
        'user_id': user_id
    }
    stmt = insert(Prediction).values(**new_prediction)
    await session.execute(stmt)
    await session.commit()
    return result