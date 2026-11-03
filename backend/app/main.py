import os
import time
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text
from database import engine, Base
from routes import asset_routes, vulnerability_routes, risk_routes, budget_routes, auth_routes
from models import asset, vulnerability, risk_score, user
from scheduler.tasks import start_scheduler
from services.auth_dependency import get_current_user

load_dotenv()
logger = logging.getLogger("api")

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyber Risk AI System")

scheduler = start_scheduler()

# Websites allowed to call this API. For deployment, set FRONTEND_ORIGINS in the
# environment to the website address(es), separated by commas.
origins = [
    o.strip()
    for o in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_common_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000

    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.0f}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"

    if elapsed_ms > 1500:
        logger.warning("Slow request: %s %s took %.0f ms", request.method, request.url.path, elapsed_ms)
    return response


# These routes now require a valid login token
protected = [Depends(get_current_user)]

app.include_router(asset_routes.router, dependencies=protected)
app.include_router(vulnerability_routes.router, dependencies=protected)
app.include_router(risk_routes.router, dependencies=protected)
app.include_router(budget_routes.router, dependencies=protected)

# Login and signup must stay open
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
    except Exception:
        # Details stay in the backend terminal, not in the public response
        logger.exception("Database connection test failed")
        return {"database": "Connection failed"}