from pydantic import BaseModel, Field

class Rating(BaseModel):
    id_trip: str
    id_user_scorer: str
    id_user_scored: str
    value: int = Field(ge=1, le=5)


    class Config:
        orm_mode = True


class RatingsSummary(BaseModel):
    id_user_scored: str
    total_sum: int
    count: int

    class Config:
        orm_mode = True
