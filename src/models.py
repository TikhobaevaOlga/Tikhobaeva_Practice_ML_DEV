from datetime import datetime
from typing import Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, default=0.0)
    username: Mapped[str] = mapped_column(String, nullable=False)

class Model(Base):
    __tablename__ = 'model'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

class Prediction(Base):
    __tablename__ = 'prediction'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    predicted_labels: Mapped[str] = Column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('model.id'), nullable=False)
    created_at = mapped_column(TIMESTAMP, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = 'transaction'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commited_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    type: Mapped[str] = mapped_column(String)
    model_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('model.id'), nullable=True)
    prediction_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('prediction.id'), nullable=True)
