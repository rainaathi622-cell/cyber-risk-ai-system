import logging
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from services.risk_score_service import calculate_risk_for_all_assets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")


def scheduled_risk_recalculation():
    """
    Recalculate risk scores for all assets.
    This runs automatically on a schedule to simulate continuous monitoring.
    """
    logger.info("Running scheduled risk score recalculation...")
    db: Session = SessionLocal()
    try:
        results = calculate_risk_for_all_assets(db)
        logger.info(f"Scheduled recalculation complete. Updated {len(results)} asset risk scores.")
    except Exception as e:
        logger.error(f"Scheduled recalculation failed: {e}")
    finally:
        db.close()


def start_scheduler():
    """
    Start the background scheduler with all recurring jobs.
    """
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        scheduled_risk_recalculation,
        trigger="interval",
        minutes=30,
        id="risk_recalculation_job",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Background scheduler started. Risk scores will recalculate every 30 minutes.")
    return scheduler