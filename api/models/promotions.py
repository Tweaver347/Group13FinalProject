from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    promotion_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)  # Promotion code
    description = Column(String(100))  # Brief description of the promotion
    discount_percentage = Column(Float, nullable=False)  # Discount as a percentage (e.g., 10.0 for 10%)
    expiration_date = Column(Date, nullable=False)  # Expiry date for the promotion