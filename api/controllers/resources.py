from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import resources as model
from sqlalchemy.exc import SQLAlchemyError


# Create a new resource
def create(db: Session, request):
    new_resource = model.Resource(
        name=request.name,
        amount=request.amount,
        unit=request.unit,
    )

    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_resource


# Read all resources
def read_all(db: Session):
    try:
        resources = db.query(model.Resource).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resources


# Read a single resource by ID
def read_one(db: Session, resource_id: int):
    try:
        resource = db.query(model.Resource).filter(model.Resource.resource_id == resource_id).first()
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource


# Update a resource
def update(db: Session, resource_id: int, request):
    try:
        resource_query = db.query(model.Resource).filter(model.Resource.resource_id == resource_id)
        resource = resource_query.first()
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource ID not found!")

        update_data = request.dict(exclude_unset=True)
        resource_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource_query.first()


# Delete a resource
def delete(db: Session, resource_id: int):
    try:
        resource_query = db.query(model.Resource).filter(model.Resource.resource_id == resource_id)
        if not resource_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource ID not found!")
        resource_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
