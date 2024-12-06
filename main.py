from fastapi import FastAPI
from routers import cats, missions
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cats.router)
app.include_router(missions.router)
