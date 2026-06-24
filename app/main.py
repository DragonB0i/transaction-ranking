from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.database import engine, Base, get_db
from app.models import User, Transaction
from app.schemas import TransactionRequest, TransactionResponse

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()
STREAK_REQUIREMENTS = {
    0: 100,
    1: 250,
    2: 400,
    3: 550,
    4: 700,
    5: 850,
    6: 1000
}


@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/transaction", response_model=TransactionResponse)
def create_transaction(
    request: TransactionRequest,
    db: Session = Depends(get_db)
):
    existing_transaction = db.query(Transaction).filter(
        Transaction.transaction_id == request.transactionId
    ).first()

    if existing_transaction:
        raise HTTPException(
            status_code=400,
            detail="Duplicate transaction detected"
        )

    user = db.query(User).filter(
        User.id == request.userId
    ).first()

    if not user:
        user = User(id=request.userId)

        db.add(user)
        db.commit()
        db.refresh(user)

    base_points = request.amount * 0.2

    today = request.transactionDate or date.today()

    transaction = Transaction(
        transaction_id=request.transactionId,
        user_id=request.userId,
        amount=request.amount,
        transaction_date=today
    )

    db.add(transaction)
    db.flush()

    qualifying_transactions = db.query(Transaction).filter(
        Transaction.user_id == request.userId,
        Transaction.amount >= 100,
        Transaction.transaction_date == today
    ).all()

    if (
            len(qualifying_transactions) >= 5
            and user.daily_bonus_awarded_date != today
    ):
        user.bonus_points += 10
        user.daily_bonus_awarded_date = today

    required_amount = STREAK_REQUIREMENTS.get(
        user.current_streak,
        1000
    )

    # First streak day
    if user.last_transaction_date is None:

        if request.amount > required_amount:
            user.current_streak = 1
            user.last_transaction_date = today

    # Existing streak
    else:

        expected_date = (
                user.last_transaction_date +
                timedelta(days=1)
        )

        # Consecutive day
        if today == expected_date:

            if request.amount > required_amount:

                user.current_streak += 1
                user.last_transaction_date = today

                if (
                        user.current_streak == 7
                        and user.streak_completed == 0
                ):
                    user.bonus_points += 50
                    user.streak_completed = 1

        # Missed a day
        elif today > expected_date:

            # Restart streak
            if request.amount > STREAK_REQUIREMENTS[0]:
                user.current_streak = 1
                user.last_transaction_date = today
            else:
                user.current_streak = 0

        # Same day transaction
        else:
            pass

    user.total_amount += request.amount
    user.total_points += base_points
    user.transaction_count += 1

    user.ranking_score = (
            user.total_points
            + user.bonus_points
            + (user.current_streak * 15)
    )

    db.commit()

    return TransactionResponse(
        message="Transaction processed successfully",
        pointsEarned=base_points
    )
@app.get("/summary/{user_id}")
def get_user_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "userId": user.id,
        "totalAmount": user.total_amount,
        "totalPoints": user.total_points,
        "bonusPoints": user.bonus_points,
        "transactionCount": user.transaction_count,
        "currentStreak": user.current_streak,
        "rankingScore": user.ranking_score
    }
@app.get("/ranking")
def get_ranking(
    db: Session = Depends(get_db)
):
    users = db.query(User).order_by(
        User.ranking_score.desc(),
        User.current_streak.desc(),
        User.total_amount.desc(),
        User.transaction_count.desc()
    ).all()

    rankings = []

    previous_score = None
    current_rank = 0

    for index, user in enumerate(users):

        if user.ranking_score != previous_score:
            current_rank = index + 1

        rankings.append({
            "rank": current_rank,
            "userId": user.id,
            "score": user.ranking_score,
            "points": user.total_points,
            "streak": user.current_streak
        })

        previous_score = user.ranking_score
    return rankings