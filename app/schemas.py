from pydantic import BaseModel, Field
from datetime import date

class TransactionRequest(BaseModel):
    transactionId: str = Field(min_length=3)

    userId: int = Field(gt=0)

    amount: float = Field(gt=0)

    transactionDate: date | None = None

class TransactionResponse(BaseModel):
    message: str
    pointsEarned: float


class UserSummaryResponse(BaseModel):
    userId: int
    totalAmount: float
    totalPoints: float
    transactionCount: int
    currentStreak: int
    rankingScore: float