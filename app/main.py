from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.db import engine, Base
from app.collectors.vk import fetch_vk
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute("SELECT 1")
    return {"db": list(result)}


@app.post("/collect/vk")
def collect_vk():
    fetch_vk()
    return {"status": "vk collected"}