from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.db import engine, Base
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute("SELECT 1")
    return {"db": list(result)}