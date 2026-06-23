from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    transactionId: str
    userId: int
    amount: float = Field(gt=0)


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