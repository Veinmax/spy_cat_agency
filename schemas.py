from pydantic import BaseModel
from typing import List, Optional

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    complete: bool = False

class TargetCreate(TargetBase):
    pass

class Target(TargetBase):
    id: int
    mission_id: int

    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    complete: bool = False

class MissionCreate(MissionBase):
    targets: List[TargetCreate]

class Mission(MissionBase):
    id: int
    cat_id: Optional[int] = None
    targets: List[Target]

    class Config:
        orm_mode = True

class SpyCatBase(BaseModel):
    name: str
    experience: int
    breed: str
    salary: float

class SpyCatCreate(SpyCatBase):
    pass

class SpyCat(SpyCatBase):
    id: int
    missions: List[Mission] = []

    class Config:
        orm_mode = True
