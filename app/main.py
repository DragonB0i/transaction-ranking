from fastapi import FastAPI

from app.database import engine
from app.database import Base

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }