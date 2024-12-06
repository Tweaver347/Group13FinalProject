from ..models import model  
from ..schemas import schema  
from sqlalchemy.orm import Session

def create(db: Session, payment: schema.PaymentCreate):
    db_payment = model.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
