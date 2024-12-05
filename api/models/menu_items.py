from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    menu_item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    ingredients = Column(String(255))  # Could be a JSON string for complex cases
    price = Column(Float, nullable=False)
    calories = Column(Integer)
    food_category = Column(String(50))  # Example: spicy, vegetarian, etc.

    # Relationships
    order_details = relationship("OrderDetail", back_populates="menu_item")