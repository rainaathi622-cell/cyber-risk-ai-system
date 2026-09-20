# Weight mappings - convert categorical values into numeric multipliers

CRITICALITY_WEIGHTS = {
    "Critical": 1.0,
    "High": 0.75,
    "Medium": 0.5,
    "Low": 0.25
}

EXPOSURE_WEIGHTS = {
    "Public": 1.0,
    "Internal": 0.6,
    "Restricted": 0.3
}

PATCH_STATUS_WEIGHTS = {
    "Outdated": 1.0,
    "Unknown": 0.7,
    "Up-to-date": 0.3
}


def calculate_risk_score(cvss_score: float, criticality: str, exposure: str, patch_status: str) -> float:
    """
    Calculate a single risk score for one vulnerability on one asset.

    cvss_score: 0-10 severity score from NVD
    criticality: Critical / High / Medium / Low
    exposure: Public / Internal / Restricted
    patch_status: Outdated / Up-to-date / Unknown

    Returns a score from 0 to 100
    """
    criticality_weight = CRITICALITY_WEIGHTS.get(criticality, 0.5)
    exposure_weight = EXPOSURE_WEIGHTS.get(exposure, 0.5)
    patch_weight = PATCH_STATUS_WEIGHTS.get(patch_status, 0.5)

    # Base score out of 10, multiplied by weights, then scaled to 100
    raw_score = cvss_score * criticality_weight * exposure_weight * patch_weight
    scaled_score = (raw_score / 10) * 100

    # Cap at 100
    return round(min(scaled_score, 100), 2)


def classify_risk_level(score: float) -> str:
    """
    Convert a numeric score (0-100) into a risk level label.
    """
    if score >= 70:
        return "Critical"
    elif score >= 50:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"


def calculate_asset_risk(vulnerabilities: list, criticality: str, exposure: str, patch_status: str) -> dict:
    """
    Calculate the AGGREGATE risk score for an asset that may have multiple vulnerabilities.

    vulnerabilities: list of cvss_score floats (e.g. [9.8, 7.5, 4.2])
    Returns a dict with the final score and risk level
    """
    if not vulnerabilities:
        return {"score": 0.0, "level": "Low"}

    # Use the HIGHEST cvss score among all vulnerabilities as the driving factor
    # (An asset is as risky as its worst vulnerability, not the average)
    highest_cvss = max(vulnerabilities)

    score = calculate_risk_score(highest_cvss, criticality, exposure, patch_status)
    level = classify_risk_level(score)

    return {"score": score, "level": level}