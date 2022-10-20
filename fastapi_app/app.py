from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/", response_model=schemas.Rating)
def create_rating(rating: schemas.Rating, db: Session = Depends(get_db)):
    # ToDo verificar que no haya un rating con ese código
    return crud.create_rating(db=db, rating=rating)


@app.get("/", response_model=List[schemas.Rating])
def read_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = crud.get_ratings(db, skip=skip, limit=limit)
    return ratings


@app.get("/{id_user_scored}/average", response_model=float)
def get_average_score(id_user_scored: str, db: Session = Depends(get_db)):
    ratings_summary = crud.get_ratings_summary(db, id_user_scored)
    if ratings_summary is None:
        raise HTTPException(status_code=404, detail="User not found")

    total_sum, count = ratings_summary
    avg = round(total_sum / count, 2)
    return avg

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
