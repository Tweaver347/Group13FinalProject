# models/payments.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String)
