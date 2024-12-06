from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import sandwiches as controller
from ..schemas.sandwiches import Sandwich

router = APIRouter(tags=["Sandwiches"], prefix="/menu")

@router.get("/", response_model=list[Sandwich])
def browse_menu(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/filter", response_model=list[Sandwich])
def filter_menu(price: float, db: Session = Depends(get_db)):
    return controller.read_filtered(db, price=price)
