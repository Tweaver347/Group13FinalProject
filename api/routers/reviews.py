from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import reviews as controller  
from ..schemas import schema 
from ..routers import router

@router.post("/", response_model=schema.Review)
def leave_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, review=request)
