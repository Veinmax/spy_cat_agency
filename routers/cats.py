import crud, schemas, database
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/cats", tags=["Spy Cats"])

@router.post("/", response_model=schemas.SpyCat)
def create_cat(cat: schemas.SpyCatCreate, db: Session = Depends(database.get_db)):
    return crud.create_cat(db=db, cat=cat)

@router.get("/", response_model=List[schemas.SpyCat])
def list_cats(db: Session = Depends(database.get_db)):
    return crud.get_cats(db=db)

@router.get("/{cat_id}", response_model=schemas.SpyCat)
def get_cat(cat_id: int, db: Session = Depends(database.get_db)):
    return crud.get_cat(db=db, cat_id=cat_id)

@router.patch("/{cat_id}", response_model=schemas.SpyCat)
def update_cat(cat_id: int, salary: float, db: Session = Depends(database.get_db)):
    return crud.update_cat(db=db, cat_id=cat_id, salary=salary)

@router.delete("/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_cat(db=db, cat_id=cat_id)
