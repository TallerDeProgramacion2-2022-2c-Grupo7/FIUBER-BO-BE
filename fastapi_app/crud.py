from sqlalchemy.orm import Session

import models, schemas


def create_rating(db: Session, rating: schemas.Rating):
    db_rating = models.Rating(id_trip=rating.id_trip, 
                            id_user_scorer = rating.id_user_scorer,
                            id_user_scored = rating.id_user_scored,
                            value = rating.value)

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rating).offset(skip).limit(limit).all()

