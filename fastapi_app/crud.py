from sqlalchemy.orm import Session

import schemas
from models import Rating, RatingsSummary

def create_rating(db: Session, rating: schemas.Rating):
    db_rating = Rating(id_trip=rating.id_trip, 
                            id_user_scorer = rating.id_user_scorer,
                            id_user_scored = rating.id_user_scored,
                            value = rating.value)

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)


    q = db.query(RatingsSummary).filter_by(id_user_scored = rating.id_user_scored)
    # If the rating was present in the summary 
    if (q.scalar()):
        q.update({ RatingsSummary.total_sum: RatingsSummary.total_sum + rating.value,
                 RatingsSummary.count: RatingsSummary.count + 1})
                   
    else:
        db_ratings_summary = RatingsSummary(id_user_scored = rating.id_user_scored,
                                            total_sum = rating.value,
                                            count = 1)
        db.add(db_ratings_summary)
        
    db.commit()

    return db_rating


def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rating).offset(skip).limit(limit).all()

def get_ratings_summary(db: Session, id_user_scored: str):
    return db.query(RatingsSummary.total_sum, RatingsSummary.count).filter_by(id_user_scored = id_user_scored).first()

    

