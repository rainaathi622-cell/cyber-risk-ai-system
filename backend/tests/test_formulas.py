import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from services.risk_formula import (
    calculate_risk_score,
    classify_risk_level,
    calculate_asset_risk,
)
from services.budget_formula import (
    estimate_fix_cost,
    calculate_risk_reduction_value,
    optimize_budget_allocation,
)


# ---------- Risk score: normal cases ----------

def test_worst_case_asset_scores_high():
    result = calculate_asset_risk([9.8], "Critical", "Public", "Outdated")
    assert result["score"] == pytest.approx(98.0, abs=0.02)
    assert result["level"] == "Critical"


def test_same_cvss_with_safer_context_scores_low():
    result = calculate_asset_risk([9.8], "Low", "Restricted", "Up-to-date")
    assert result["score"] == pytest.approx(2.21, abs=0.02)
    assert result["level"] == "Low"


def test_worst_vulnerability_drives_the_score():
    result = calculate_asset_risk([9.8, 3.2, 5.5], "High", "Internal", "Outdated")
    assert result["score"] == pytest.approx(44.1, abs=0.02)
    assert result["level"] == "Medium"


# ---------- Risk score: invalid and extreme inputs ----------

def test_no_vulnerabilities_means_zero_risk():
    result = calculate_asset_risk([], "Critical", "Public", "Outdated")
    assert result == {"score": 0.0, "level": "Low"}


def test_unknown_labels_use_the_default_weight():
    # 10 x 0.5 x 0.5 x 0.5 x 10 = 12.5
    assert calculate_risk_score(10, "???", "???", "???") == pytest.approx(12.5, abs=0.02)


def test_score_is_capped_at_100():
    assert calculate_risk_score(15, "Critical", "Public", "Outdated") == 100.0


# ---------- Risk level: boundary values ----------

@pytest.mark.parametrize(
    "score, expected",
    [
        (100, "Critical"),
        (70, "Critical"),
        (69.99, "High"),
        (50, "High"),
        (49.99, "Medium"),
        (30, "Medium"),
        (29.99, "Low"),
        (0, "Low"),
    ],
)
def test_risk_level_boundaries(score, expected):
    assert classify_risk_level(score) == expected


# ---------- Budget: cost and risk reduction ----------

def test_fix_cost_for_known_types():
    assert estimate_fix_cost("Server", "Critical") == 20000
    assert estimate_fix_cost("Laptop", "Medium") == 4800


def test_fix_cost_for_unknown_types_uses_defaults():
    assert estimate_fix_cost("Toaster", "Whatever") == 9000


def test_risk_reduction_when_patched():
    # 98 now, 29.4 after patching -> 68.6 reduction
    value = calculate_risk_reduction_value(98.0, 9.8, "Critical", "Public", "Outdated")
    assert value == pytest.approx(68.6, abs=0.02)


def test_risk_reduction_is_never_negative():
    assert calculate_risk_reduction_value(0, 9.8, "Critical", "Public", "Up-to-date") == 0


# ---------- Budget: allocation ----------

FIXES = [
    {"asset_name": "A", "estimated_cost": 5000, "risk_reduction": 40},
    {"asset_name": "B", "estimated_cost": 20000, "risk_reduction": 60},
    {"asset_name": "C", "estimated_cost": 8000, "risk_reduction": 10},
]


def test_zero_budget_selects_nothing():
    result = optimize_budget_allocation(FIXES, 0)
    assert result["selected_fixes"] == []
    assert result["total_cost"] == 0
    assert len(result["skipped_fixes"]) == 3


def test_budget_exactly_equal_to_one_cost():
    result = optimize_budget_allocation(FIXES, 5000)
    assert [f["asset_name"] for f in result["selected_fixes"]] == ["A"]
    assert result["remaining_budget"] == 0


def test_budget_is_never_exceeded():
    result = optimize_budget_allocation(FIXES, 13000)
    assert result["total_cost"] <= 13000
    assert result["remaining_budget"] == pytest.approx(13000 - result["total_cost"])


def test_large_budget_selects_everything():
    result = optimize_budget_allocation(FIXES, 1000000)
    assert len(result["selected_fixes"]) == 3
    assert result["skipped_fixes"] == []