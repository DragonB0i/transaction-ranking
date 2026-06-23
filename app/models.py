from sqlalchemy import Column, Integer, Float, String, Date, DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    total_amount = Column(Float, default=0)

    total_points = Column(Float, default=0)

    transaction_count = Column(Integer, default=0)

    current_streak = Column(Integer, default=0)

    last_transaction_date = Column(Date, nullable=True)

    ranking_score = Column(Float, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    transaction_id = Column(String, unique=True, nullable=False)

    user_id = Column(Integer, nullable=False)

    amount = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())