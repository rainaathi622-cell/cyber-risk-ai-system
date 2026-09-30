import logging
import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from services.risk_score_service import calculate_risk_for_all_assets

# Add scripts folder to path so we can reuse the CVE fetch logic
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")


def scheduled_risk_recalculation():
    """
    Recalculate risk scores for all assets based on current data.
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


def scheduled_cve_refresh():
    """
    Fetch fresh CVE data from NVD and link any new ones to assets,
    then recalculate risk scores to reflect the new data.
    This simulates continuous vulnerability monitoring.
    """
    logger.info("Running scheduled CVE data refresh...")
    db: Session = SessionLocal()
    try:
        from fetch_cve_data import fetch_critical_cves, link_cves_to_assets
        from models.asset import Asset

        assets = db.query(Asset).all()
        cve_list = fetch_critical_cves(results_limit=10)

        if cve_list:
            link_cves_to_assets(db, cve_list, assets)
            logger.info("CVE refresh complete. New vulnerabilities linked (duplicates skipped).")
        else:
            logger.warning("CVE refresh returned no data - possible rate limit or network issue.")

        # Recalculate risk scores after refreshing CVE data
        calculate_risk_for_all_assets(db)
        logger.info("Risk scores updated after CVE refresh.")

    except Exception as e:
        logger.error(f"Scheduled CVE refresh failed: {e}")
    finally:
        db.close()


def start_scheduler():
    """
    Start the background scheduler with all recurring jobs.
    """
    scheduler = BackgroundScheduler()

    # Recalculate risk scores every 30 minutes
    scheduler.add_job(
        scheduled_risk_recalculation,
        trigger="interval",
        minutes=30,
        id="risk_recalculation_job",
        replace_existing=True
    )

    # Fetch fresh CVE data every 6 hours (NVD rate limits mean we shouldn't do this too often)
    scheduler.add_job(
        scheduled_cve_refresh,
        trigger="interval",
        hours=6,
        id="cve_refresh_job",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Background scheduler started: risk recalculation every 30 min, CVE refresh every 6 hours.")
    return scheduler