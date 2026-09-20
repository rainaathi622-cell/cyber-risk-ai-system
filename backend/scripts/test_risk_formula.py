import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from services.risk_formula import calculate_asset_risk

# Test Case 1: Critical, Public, Outdated asset with a severe vulnerability
test1 = calculate_asset_risk(
    vulnerabilities=[9.8],
    criticality="Critical",
    exposure="Public",
    patch_status="Outdated"
)
print("Test 1 (Critical/Public/Outdated, CVSS 9.8):", test1)

# Test Case 2: Low criticality, Restricted, Up-to-date asset with same vulnerability
test2 = calculate_asset_risk(
    vulnerabilities=[9.8],
    criticality="Low",
    exposure="Restricted",
    patch_status="Up-to-date"
)
print("Test 2 (Low/Restricted/Up-to-date, CVSS 9.8):", test2)

# Test Case 3: Multiple vulnerabilities, mixed severity
test3 = calculate_asset_risk(
    vulnerabilities=[9.8, 3.2, 5.5],
    criticality="High",
    exposure="Internal",
    patch_status="Outdated"
)
print("Test 3 (High/Internal/Outdated, multiple CVEs):", test3)

# Test Case 4: No vulnerabilities at all
test4 = calculate_asset_risk(
    vulnerabilities=[],
    criticality="Critical",
    exposure="Public",
    patch_status="Outdated"
)
print("Test 4 (No vulnerabilities):", test4)