from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, database

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.post("/", response_model=schemas.Mission)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(database.get_db)):
    return crud.create_mission(db=db, mission_data=mission)

@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_mission(db=db, mission_id=mission_id)

@router.patch("/{mission_id}/assign-cat")
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(database.get_db)):
    return crud.assign_cat_to_mission(db=db, mission_id=mission_id, cat_id=cat_id)

@router.patch("/{mission_id}/complete")
def complete_mission(mission_id: int, db: Session = Depends(database.get_db)):
    return crud.complete_mission(db=db, mission_id=mission_id)

@router.patch("/targets/{target_id}")
def update_target(target_id: int, target: schemas.TargetBase, db: Session = Depends(database.get_db)):
    return crud.update_target(db=db, target_id=target_id, target_data=target)

@router.patch("/targets/{target_id}/complete")
def complete_target(target_id: int, db: Session = Depends(database.get_db)):
    return crud.complete_target(db=db, target_id=target_id)

@router.get("/", response_model=List[schemas.Mission])
def list_missions(db: Session = Depends(database.get_db)):
    return crud.get_missions(db=db)

@router.get("/{mission_id}", response_model=schemas.Mission)
def get_mission(mission_id: int, db: Session = Depends(database.get_db)):
    return crud.get_mission(db=db, mission_id=mission_id)
