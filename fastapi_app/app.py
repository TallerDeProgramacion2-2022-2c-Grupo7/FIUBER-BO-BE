from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import firebase_admin
from firebase_admin import credentials
from os import environ
from datadog_event import DatadogEventMiddleware
from datadog import initialize

from firebase_credentials import admin_credentials
from id_token import IdTokenMiddleware
import crud, models, schemas

if __name__ == "__main__":
    from database import SessionLocal, engine

initialize(statsd_host="dd-agent", statsd_port=8125)
firebase_credentials = credentials.Certificate(admin_credentials)
firebase_admin.initialize_app(firebase_credentials)


app = FastAPI()

# Only create models and add middleware if this is not for running tests
if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(IdTokenMiddleware)

    app.add_middleware(DatadogEventMiddleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=schemas.Rating)
def create_rating(rating: schemas.Rating, db: Session = Depends(get_db)):
    if rating.id_user_scorer == rating.id_user_scored:
        raise HTTPException(status_code=400, detail="A user can't rate himself")

    # db_rating = crud.get_rating_by_id_trip(db, id_trip=rating.id_trip)
    # if db_rating:
    # raise HTTPException(status_code=400, detail="Rating already registered")

    return crud.create_rating(db=db, rating=rating)


@app.get("/{id_user_scorer}", response_model=List[schemas.RatingBase])
def read_ratings(
    id_user_scorer: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    ratings = crud.get_ratings_by_id_user_scorer(
        db, id_user_scorer, skip=skip, limit=limit
    )
    return ratings


@app.get("/{id_user_scored}/average", response_model=float)
def get_average_score(id_user_scored: str, db: Session = Depends(get_db)):
    ratings_summary = crud.get_ratings_summary(db, id_user_scored)
    if ratings_summary is None:
        return -1

    total_sum, count = ratings_summary
    avg = round(total_sum / count, 2)
    return avg


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
