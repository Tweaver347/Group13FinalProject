# models/reviews.py
from sqlalchemy import Column, Integer, String, ForeignKey
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    review_text = Column(String)
    rating = Column(Integer)
