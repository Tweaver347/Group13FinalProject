from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import promotions as model
from sqlalchemy.exc import SQLAlchemyError


# Create a new promotion
def create(db: Session, request):
    new_promotion = model.Promotion(
        code=request.code,
        description=request.description,
        discount_percentage=request.discount_percentage,
        expiration_date=request.expiration_date,
    )

    try:
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_promotion


# Read all promotions
def read_all(db: Session):
    try:
        promotions = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotions


# Read a single promotion by ID
def read_one(db: Session, promotion_id: int):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.promotion_id == promotion_id).first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion


# Update a promotion
def update(db: Session, promotion_id: int, request):
    try:
        promotion_query = db.query(model.Promotion).filter(model.Promotion.promotion_id == promotion_id)
        promotion = promotion_query.first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion ID not found!")

        update_data = request.dict(exclude_unset=True)
        promotion_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion_query.first()


# Delete a promotion
def delete(db: Session, promotion_id: int):
    try:
        promotion_query = db.query(model.Promotion).filter(model.Promotion.promotion_id == promotion_id)
        if not promotion_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion ID not found!")
        promotion_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
