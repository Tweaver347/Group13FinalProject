from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4


# Create a new order
def create(db: Session, request):
    new_order = model.Order(
        customer_id=request.customer_id,
        tracking_number=str(uuid4()),  # Generate a unique tracking number
        order_status="Pending",  # Default status
        total_price=0.0  # Initially zero, calculated from order details later
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order


# Read all orders
def read_all(db: Session):
    try:
        orders = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return orders


# Read a single order by ID
def read_one(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


# Update an order
def update(db: Session, order_id: int, request):
    try:
        order_query = db.query(model.Order).filter(model.Order.order_id == order_id)
        order = order_query.first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")

        update_data = request.dict(exclude_unset=True)
        order_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order_query.first()


# Delete an order
def delete(db: Session, order_id: int):
    try:
        order_query = db.query(model.Order).filter(model.Order.order_id == order_id)
        if not order_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
        order_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
