from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Rating(Base):
    __tablename__ = "ratings"

    id_trip = Column(String, primary_key=True)
    # The id of the user who gives the rating
    id_user_scorer = Column(String, index=True)
    # The id of the user who receives the rating
    id_user_scored = Column(String, index=True)
    value = Column(Integer)


class RatingsSummary(Base):
    __tablename__ = "ratings_summary"

    id_user_scored = Column(String, primary_key=True, index=True)
    total_sum = Column(Integer)
    count = Column(Integer)
