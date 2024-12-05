from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_details as model, menu_items as menu_model
from sqlalchemy.exc import SQLAlchemyError


# Create a new order detail
def create(db: Session, request):
    # Retrieve the menu item to get the price
    menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.menu_item_id == request.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")

    # Calculate subtotal
    subtotal = request.quantity * menu_item.price

    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=request.quantity,
        price_per_item=menu_item.price,
        subtotal=subtotal,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


# Read all order details
def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


# Read a single order detail by ID
def read_one(db: Session, detail_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.order_detail_id == detail_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


# Update an order detail
def update(db: Session, detail_id: int, request):
    try:
        item_query = db.query(model.OrderDetail).filter(model.OrderDetail.order_detail_id == detail_id)
        item = item_query.first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail ID not found!")

        # Recalculate subtotal if quantity is updated
        if request.quantity:
            item.subtotal = request.quantity * item.price_per_item

        update_data = request.dict(exclude_unset=True)
        item_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item_query.first()


# Delete an order detail
def delete(db: Session, detail_id: int):
    try:
        item_query = db.query(model.OrderDetail).filter(model.OrderDetail.order_detail_id == detail_id)
        if not item_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail ID not found!")
        item_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
