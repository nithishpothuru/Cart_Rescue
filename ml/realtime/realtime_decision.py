"""
CartGuard AI
Real-Time Decision Engine

Pipeline:

Session Data
    ↓
Feature Generator
    ↓
XGBoost Risk Scorer
    ↓
Scenario Detector
    ↓
Action Engine
    ↓
Final Decision
"""

from pathlib import Path
import sys
import json


# ============================================================
# Path Configuration
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent
ML_DIR = CURRENT_DIR.parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))


# ============================================================
# Import CartGuard Components
# ============================================================

from realtime_features import generate_features
from risk_scorer import score_session
from scenario_detector import detect_scenario
from action_engine import recommend_action


# ============================================================
# Header
# ============================================================

print("=" * 70)
print(" CARTGUARD AI - REAL-TIME DECISION ENGINE ")
print("=" * 70)


# ============================================================
# Example Active Session
# ============================================================
#
# This represents the signals available from a live customer
# session.
#
# Replace these values later with real frontend/backend events.
# ============================================================

session = {

    # --------------------------------------------------------
    # Basic Shopping Activity
    # --------------------------------------------------------

    "session_start": 0,

    "events": [
        {
            "event_type": "view",
            "product_id": "P001",
            "category": "Electronics",
            "brand": "Samsung",
            "price": 50000
        },
        {
            "event_type": "view",
            "product_id": "P002",
            "category": "Electronics",
            "brand": "Apple",
            "price": 45000
        },
        {
            "event_type": "cart",
            "product_id": "P001",
            "category": "Electronics",
            "brand": "Samsung",
            "price": 50000
        }
    ],

    # --------------------------------------------------------
    # Scenario Signals
    # --------------------------------------------------------

    "has_cart": True,

    "payment_attempt": True,
    "payment_failed": True,

    "delivery_viewed": False,
    "delivery_date_changed": False,

    "shipping_cost_viewed": False,

    "price_comparison": False,

    "cod_available": True,
    "cod_requested": False,

    "checkout_started": True,

    "form_repeated": False,

    "cart_changed": False
}


# ============================================================
# STEP 1 - Generate ML Features
# ============================================================

print("\n")
print("=" * 70)
print(" STEP 1 - REAL-TIME FEATURE GENERATION ")
print("=" * 70)

try:

    features = generate_features(session["events"])

except Exception as e:

    print("\nFeature generation failed.")
    print(f"Error : {e}")
    raise


print("\nFeatures Generated : 22")


# ============================================================
# STEP 2 - Calculate Abandonment Risk
# ============================================================

print("\n")
print("=" * 70)
print(" STEP 2 - XGBOOST RISK ASSESSMENT ")
print("=" * 70)

try:

    risk_result = score_session(features)

except Exception as e:

    print("\nRisk scoring failed.")
    print(f"Error : {e}")
    raise


# ------------------------------------------------------------
# Read Risk Result
# ------------------------------------------------------------

purchase_probability = float(
    risk_result["purchase_probability"]
)

abandonment_probability = float(
    risk_result["abandonment_probability"]
)

risk_level = risk_result["risk_level"]

model_prediction = risk_result["prediction"]


print(
    f"\nPurchase Probability     : "
    f"{purchase_probability:.4f}"
)

print(
    f"Abandonment Probability  : "
    f"{abandonment_probability:.4f}"
)

print(
    f"Risk Level               : "
    f"{risk_level}"
)


# ============================================================
# STEP 3 - Detect Shopping Scenario
# ============================================================

print("\n")
print("=" * 70)
print(" STEP 3 - SCENARIO DETECTION ")
print("=" * 70)

try:

    scenario_result = detect_scenario(session)

except Exception as e:

    print("\nScenario detection failed.")
    print(f"Error : {e}")
    raise


# ------------------------------------------------------------
# Read Scenario Result
# ------------------------------------------------------------

scenario = scenario_result["scenario"]

scenario_reason = scenario_result["reason"]

scenario_priority = scenario_result.get(
    "priority",
    None
)


print(
    f"\nScenario                 : "
    f"{scenario}"
)

print(
    f"Reason                   : "
    f"{scenario_reason}"
)

if scenario_priority is not None:

    print(
        f"Priority                 : "
        f"{scenario_priority}"
    )


# ============================================================
# STEP 4 - Select Action
# ============================================================

print("\n")
print("=" * 70)
print(" STEP 4 - ACTION ENGINE ")
print("=" * 70)

try:

    action, action_reason = recommend_action(

        risk_level=risk_level,

        abandonment_probability=
        abandonment_probability,

        scenario=scenario

    )

except Exception as e:

    print("\nAction engine failed.")
    print(f"Error : {e}")
    raise


# ============================================================
# STEP 5 - FINAL CARTGUARD DECISION
# ============================================================

print("\n")
print("=" * 70)
print(" CARTGUARD AI - FINAL DECISION ")
print("=" * 70)

print("\n## SESSION")

print("-" * 40)

print(
    f"Events                   : "
    f"{len(session['events'])}"
)

print(
    f"Cart Active              : "
    f"{session['has_cart']}"
)


print("\n## RISK")

print("-" * 40)

print(
    f"Purchase Probability     : "
    f"{purchase_probability:.4f}"
)

print(
    f"Abandonment Probability  : "
    f"{abandonment_probability:.4f}"
)

print(
    f"Risk Level               : "
    f"{risk_level}"
)

print(
    f"Model Prediction         : "
    f"{model_prediction}"
)


print("\n## SCENARIO")

print("-" * 40)

print(
    f"Detected Scenario        : "
    f"{scenario}"
)

print(
    f"Scenario Reason          : "
    f"{scenario_reason}"
)


print("\n## RECOMMENDED ACTION")

print("-" * 40)

print(
    f"Action                   : "
    f"{action}"
)

print(
    f"Reason                   : "
    f"{action_reason}"
)


# ============================================================
# Final JSON Decision
# ============================================================

final_decision = {

    "risk": {

        "purchase_probability":
            round(purchase_probability, 4),

        "abandonment_probability":
            round(abandonment_probability, 4),

        "risk_level":
            risk_level,

        "model_prediction":
            int(model_prediction)
    },

    "scenario": {

        "name":
            scenario,

        "reason":
            scenario_reason,

        "priority":
            scenario_priority
    },

    "decision": {

        "action":
            action,

        "reason":
            action_reason
    }
}


# ============================================================
# Display JSON
# ============================================================

print("\n")
print("=" * 70)
print(" FINAL DECISION JSON ")
print("=" * 70)

print(
    json.dumps(
        final_decision,
        indent=4
    )
)


print("\n")
print("=" * 70)
print(" REAL-TIME DECISION COMPLETED ")
print("=" * 70)