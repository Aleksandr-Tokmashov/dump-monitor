from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import get_db
from .db import engine, Base
from .collectors.vk import fetch_vk
from .models import PostRaw, Incident
from .models_stations import RailwayStation
from .services.detector import process_posts
from app.bot import bot

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_event_handler("startup", bot.startup)
app.add_event_handler("shutdown", bot.shutdown)

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute("SELECT 1")
    return {"db": list(result)}


@app.post("/collect/vk")
def collect_vk():
    fetch_vk()
    return {"status": "vk collected"}


@app.post("/process")
async def process(db: Session = Depends(get_db)):

    await process_posts(db)

    return {"status": "processed"}