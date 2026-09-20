from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine, Base
from routes import asset_routes, vulnerability_routes, risk_routes, budget_routes, auth_routes
from models import asset, vulnerability, risk_score, user

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyber Risk AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(asset_routes.router)
app.include_router(vulnerability_routes.router)
app.include_router(risk_routes.router)
app.include_router(budget_routes.router)
app.include_router(auth_routes.router)

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