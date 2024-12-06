from pydantic import BaseModel
from datetime import date
from typing import Optional

class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_percentage: float
    expiration_date: date


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    description: Optional[str]
    discount_percentage: Optional[float]
    expiration_date: Optional[date]


class Promotion(PromotionBase):
    promotion_id: int

    class Config:
        orm_mode = True
