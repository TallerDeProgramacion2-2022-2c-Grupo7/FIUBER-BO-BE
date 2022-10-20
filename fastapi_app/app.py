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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
