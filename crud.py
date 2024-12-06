import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException
from services.breeds import validate_breed

# CRUD operations for Spy Cats
def create_cat(db: Session, cat: schemas.SpyCatCreate):
    if not validate_breed(cat.breed):
        raise HTTPException(status_code=400, detail="Invalid breed")
    db_cat = models.SpyCat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_cats(db: Session):
    return db.query(models.SpyCat).all()

def get_cat(db: Session, cat_id: int):
    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat

def update_cat(db: Session, cat_id: int, salary: float):
    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db_cat.salary = salary
    db.commit()
    db.refresh(db_cat)
    return db_cat

def delete_cat(db: Session, cat_id: int):
    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(db_cat)
    db.commit()
    return {"message": "Cat deleted successfully"}

# CRUD operations for Missions
def create_mission(db: Session, mission_data: schemas.MissionCreate) -> models.Mission:
    """Create a new Mission and its Targets."""
    mission = models.Mission(complete=False)
    db.add(mission)
    db.commit()
    db.refresh(mission)

    for target_data in mission_data.targets:
        existing_target = db.query(models.Target).filter(
            models.Target.notes == target_data.notes,
            models.Target.mission_id == mission.id,
        ).first()

        if existing_target:
            raise HTTPException(
                status_code=400, detail=f"Target with notes {target_data.notes} already exists in the mission"
            )

        target = models.Target(**target_data.dict(exclude={"mission_id"}), mission_id=mission.id)
        db.add(target)

    db.commit()
    db.refresh(mission)
    return mission


# Delete a Mission
def delete_mission(db: Session, mission_id: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if db_mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete a mission assigned to a cat")

    db.delete(db_mission)
    db.commit()
    return {"message": "Mission deleted successfully"}


# Assign a Cat to a Mission
def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if db_mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned to a cat")

    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    # Ensure the cat has no active mission
    active_mission = db.query(models.Mission).filter(
        models.Mission.cat_id == cat_id, models.Mission.complete == False
    ).first()
    if active_mission:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    db_mission.cat_id = cat_id
    db.commit()
    db.refresh(db_mission)
    return db_mission


# Update Targets
def update_target(db: Session, target_id: int, target_data: schemas.TargetBase):
    db_target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not db_target:
        raise HTTPException(status_code=404, detail="Target not found")

    if db_target.complete:
        raise HTTPException(status_code=400, detail="Cannot update a completed target")

    db_mission = db_target.mission
    if db_mission.complete:
        raise HTTPException(status_code=400, detail="Cannot update a target in a completed mission")

    for key, value in target_data.dict().items():
        setattr(db_target, key, value)

    db.commit()
    db.refresh(db_target)
    return db_target


# Mark Target as Completed
def complete_target(db: Session, target_id: int):
    db_target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not db_target:
        raise HTTPException(status_code=404, detail="Target not found")

    db_target.complete = True
    db.commit()
    return {"message": "Target marked as complete"}


# Mark Mission as Completed
def complete_mission(db: Session, mission_id: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    for target in db_mission.targets:
        if not target.complete:
            raise HTTPException(status_code=400, detail="All targets must be completed first")

    db_mission.complete = True
    db.commit()
    return {"message": "Mission marked as complete"}


# Get a Mission
def get_mission(db: Session, mission_id: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission


# List Missions
def get_missions(db: Session):
    return db.query(models.Mission).all()
