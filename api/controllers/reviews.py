from ..models import model  
from ..schemas import schema  
from sqlalchemy.orm import Session

def create(db: Session, review: schema.ReviewCreate):
    db_review = model.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
