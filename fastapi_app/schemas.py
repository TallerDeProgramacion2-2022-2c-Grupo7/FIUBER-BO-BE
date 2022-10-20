from pydantic import BaseModel

class Rating(BaseModel):
    id_trip: str
    id_user_scorer: str
    id_user_scored: str
    value: int

    class Config:
        orm_mode = True
