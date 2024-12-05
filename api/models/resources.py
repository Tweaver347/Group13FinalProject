from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)  # Ensure no duplicate names
    amount = Column(Float, nullable=False)  # Quantity of the resource
    unit = Column(String(50), nullable=False)  # Measurement unit (e.g., kg, liters)
