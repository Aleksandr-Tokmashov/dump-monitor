from fastapi import FastAPI
from app.db import engine

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    conn = engine.connect()
    result = conn.execute("SELECT 1")
    return {"db": list(result)}