from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import payments as controller
from ..schemas import schema
from ..schemas.payments import Payment

router = APIRouter(tags=["Payments"], prefix="/payments")

@router.post("/", response_model=Payment)
def make_payment(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, payment=request)
