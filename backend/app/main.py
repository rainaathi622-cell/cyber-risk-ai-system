from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Backend running fine"}

@app.get("/test-db")
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "Connected successfully"}
    except Exception as e:
        return {"database": "Connection failed", "error": str(e)}