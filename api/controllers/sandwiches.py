from sqlalchemy.orm import Session
from ..models import sandwiches as model
from ..schemas import sandwiches as schema

def read_all(db: Session):
    return db.query(model.Sandwich).all()

def read_filtered(db: Session, price: float = None):
    query = db.query(model.Sandwich)
    if price:
        query = query.filter(model.Sandwich.price <= price)
    return query.all()
