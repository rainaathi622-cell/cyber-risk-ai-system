import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text
from database import engine, Base
from routes import asset_routes, vulnerability_routes, risk_routes, budget_routes, auth_routes
from models import asset, vulnerability, risk_score, user
from scheduler.tasks import start_scheduler

logger = logging.getLogger("api")

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyber Risk AI System")

scheduler = start_scheduler()

# Compress larger responses so they download faster
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.0f}"
    if elapsed_ms > 1500:
        logger.warning("Slow request: %s %s took %.0f ms", request.method, request.url.path, elapsed_ms)
    return response


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