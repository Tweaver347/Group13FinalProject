from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    order_detail_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.menu_item_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))

    # Relationships
    order = relationship("Order", back_populates="order_details")
    menu_item = relationship("MenuItem", back_populates="order_details")
    sandwich = relationship("Sandwich", back_populates="order_details")
