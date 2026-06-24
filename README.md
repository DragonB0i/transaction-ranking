# Transaction Ranking System

## Overview

The Transaction Ranking System is a backend-focused application built using FastAPI, SQLAlchemy, and SQLite. It processes user transactions, calculates reward points, maintains user rankings, tracks streaks, awards bonuses, and exposes REST APIs for transaction management and leaderboard generation.

The project also includes a lightweight frontend built using HTML, CSS, and JavaScript, deployed separately and connected to the backend through REST APIs.

---

## Live Deployment

### Frontend

GitHub Pages Deployment

### Backend

Render Deployment

### API Documentation

`/docs` endpoint powered by Swagger UI

---

# Features

## Transaction Processing

Users can submit transactions through the API.

Each transaction contains:

* Transaction ID
* User ID
* Transaction Amount
* Transaction Date (optional)

Example:

```json
{
  "transactionId": "TXN101",
  "userId": 1,
  "amount": 500
}
```

---

## Duplicate Transaction Detection

Every transaction ID must be unique.

Before processing a transaction, the system checks:

```python
Transaction.transaction_id == request.transactionId
```

If a duplicate transaction ID is detected:

```json
{
  "detail": "Duplicate transaction detected"
}
```

Response Code:

```http
400 Bad Request
```

This prevents accidental double processing and duplicate rewards.

---

## Automatic User Creation

If a transaction is received for a user that does not exist:

* A new user record is automatically created.
* No separate user registration endpoint is required.

---

# Reward Points System

Every transaction earns base points.

Formula:

```text
Points Earned = Transaction Amount × 0.2
```

Examples:

| Amount | Points Earned |
| ------ | ------------- |
| 100    | 20            |
| 500    | 100           |
| 1000   | 200           |

---

# Daily Bonus System

The system rewards highly active users.

Rule:

* Complete 5 or more qualifying transactions
* Each transaction must be at least ₹100
* Bonus awarded only once per day

Bonus:

```text
+10 Bonus Points
```

Validation:

```python
Transaction.amount >= 100
```

and

```python
user.daily_bonus_awarded_date != today
```

This prevents users from claiming the same daily bonus multiple times.

---

# Streak System

The streak system rewards consistent daily transaction activity.

A streak increases only if:

1. Transaction is made on the next consecutive day.
2. Minimum transaction requirement is met.

---

## Streak Thresholds

| Streak Day | Required Amount |
| ---------- | --------------- |
| Day 1      | > 100           |
| Day 2      | > 250           |
| Day 3      | > 400           |
| Day 4      | > 550           |
| Day 5      | > 700           |
| Day 6      | > 850           |
| Day 7      | > 1000          |

Implemented using:

```python
STREAK_REQUIREMENTS = {
    0: 100,
    1: 250,
    2: 400,
    3: 550,
    4: 700,
    5: 850,
    6: 1000
}
```

---

## Consecutive Day Validation

The system checks:

```python
expected_date =
    last_transaction_date +
    timedelta(days=1)
```

Only transactions performed on the exact next day continue the streak.

---

## Missed Day Handling

If a user misses a day:

```python
today > expected_date
```

The streak is reset.

If the new transaction satisfies the first threshold:

```text
Current Streak = 1
```

Otherwise:

```text
Current Streak = 0
```

---

## Same Day Protection

Multiple transactions on the same day do not increase streak count.

This prevents abuse.

---

## Streak Completion Reward

Upon reaching a 7-day streak:

```text
+50 Bonus Points
```

Awarded only once.

Validation:

```python
user.streak_completed == 0
```

After reward:

```python
user.streak_completed = 1
```

This prevents repeated streak reward farming.

---

# Ranking System

Every user receives a ranking score.

Formula:

```text
Ranking Score =
    Total Points
    + Bonus Points
    + (Current Streak × 15)
```

Example:

```text
Total Points = 620
Bonus Points = 10
Current Streak = 3

Ranking Score =
620 + 10 + (3 × 15)

= 675
```

---

# Leaderboard Ranking Factors

Users are sorted using multiple ranking factors.

Priority Order:

### 1. Ranking Score

Higher score ranks first.

```python
User.ranking_score.desc()
```

---

### 2. Current Streak

If scores are equal:

```python
User.current_streak.desc()
```

Longer streak wins.

---

### 3. Total Transaction Amount

If streaks are equal:

```python
User.total_amount.desc()
```

Higher spending wins.

---

### 4. Transaction Count

Final tie-breaker:

```python
User.transaction_count.desc()
```

More transactions wins.

---

# API Endpoints

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

Used by frontend to verify backend availability.

---

## Create Transaction

```http
POST /transaction
```

Processes transaction and updates:

* Points
* Bonus
* Streak
* Ranking

---

## User Summary

```http
GET /summary/{user_id}
```

Returns:

```json
{
  "userId": 1,
  "totalAmount": 3100,
  "totalPoints": 620,
  "bonusPoints": 10,
  "transactionCount": 4,
  "currentStreak": 3,
  "rankingScore": 675
}
```

---

## Leaderboard

```http
GET /ranking
```

Returns ranked users.

Example:

```json
[
  {
    "rank": 1,
    "userId": 2,
    "score": 3455,
    "points": 3400,
    "streak": 3
  }
]
```

---

# Error Handling

## Duplicate Transaction

```http
400 Bad Request
```

```json
{
  "detail": "Duplicate transaction detected"
}
```

---

## User Not Found

```http
404 Not Found
```

```json
{
  "detail": "User not found"
}
```

---

## Validation Errors

FastAPI automatically validates request data.

Example:

```http
422 Unprocessable Entity
```

Invalid requests:

* Missing fields
* Invalid types
* Malformed JSON

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn

## Frontend

* HTML
* CSS
* JavaScript

## Deployment

* Render (Backend)
* GitHub Pages (Frontend)

---

# Project Architecture

```text
Frontend (GitHub Pages)
        |
        |
        v
FastAPI Backend (Render)
        |
        |
        v
SQLite Database
```

---

# Future Improvements

* JWT Authentication
* User Registration/Login
* PostgreSQL Database
* Docker Containerization
* Redis Caching
* Automated Streak Scheduler
* Admin Dashboard
* Analytics Dashboard
* Unit & Integration Testing

---

# Author

Built as a backend engineering assessment project demonstrating:

* REST API Design
* Database Modeling
* Business Logic Implementation
* Ranking Algorithms
* Validation & Error Handling
* Deployment & Frontend Integration
