from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import get_db

router = APIRouter(tags=['Menu'], prefix="/menu")

@router.get("/", response_model=list[schema.Sandwich])
def get_menu_items(db: Session = Depends(get_db)):
    return controller.get_all(db)
