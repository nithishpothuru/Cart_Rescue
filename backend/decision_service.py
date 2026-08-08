"""
CartGuard AI
Backend Decision Service

Connects Flask backend with ML real-time decision pipeline.

Pipeline:

MongoDB Events
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

import sys
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent

PROJECT_DIR = CURRENT_DIR.parent

ML_DIR = PROJECT_DIR / "ml"
REALTIME_DIR = ML_DIR / "realtime"


if str(REALTIME_DIR) not in sys.path:
    sys.path.insert(0, str(REALTIME_DIR))


# ============================================================
# IMPORT ML COMPONENTS
# ============================================================

from realtime_features import generate_features
from risk_scorer import score_session
from scenario_detector import detect_scenario
from action_engine import recommend_action


# ============================================================
# GENERATE CARTGUARD DECISION
# ============================================================

def generate_decision(session_events):

    """
    Generate a complete CartGuard decision.

    Input:
        session_events -> list of event dictionaries

    Output:
        {
            risk: {...},
            scenario: {...},
            decision: {...}
        }
    """

    # --------------------------------------------------------
    # Validate Input
    # --------------------------------------------------------

    if not isinstance(session_events, list):

        raise ValueError(
            "session_events must be a list."
        )

    if len(session_events) == 0:

        raise ValueError(
            "No events found for this session."
        )


    # ========================================================
    # STEP 1
    # FEATURE GENERATION
    # ========================================================

    features = generate_features(
        session_events
    )


    # ========================================================
    # STEP 2
    # XGBOOST RISK SCORING
    # ========================================================

    risk = score_session(
        features
    )


    # ========================================================
    # STEP 3
    # SCENARIO DETECTION
    # ========================================================

    # scenario_detector currently expects
    # a session dictionary, not just a list.

    session_data = {

        "events": session_events,

        "has_cart": any(
            event.get("event_type") == "cart"
            for event in session_events
        ),

        "payment_attempt": any(
            event.get("event_type") == "payment_attempt"
            for event in session_events
        ),

        "payment_failed": any(
            event.get("event_type") == "payment_failed"
            for event in session_events
        ),

        "delivery_viewed": any(
            event.get("event_type") == "delivery_viewed"
            for event in session_events
        ),

        "delivery_date_changed": any(
            event.get("event_type") == "delivery_date_changed"
            for event in session_events
        ),

        "shipping_cost_viewed": any(
            event.get("event_type") == "shipping_cost_viewed"
            for event in session_events
        ),

        "price_comparison": any(
            event.get("event_type") == "price_comparison"
            for event in session_events
        ),

        "cod_available": True,

        "cod_requested": any(
            event.get("event_type") == "cod_requested"
            for event in session_events
        ),

        "checkout_started": any(
            event.get("event_type") == "checkout_started"
            for event in session_events
        ),

        "form_repeated": any(
            event.get("event_type") == "form_repeated"
            for event in session_events
        ),

        "cart_changed": any(
            event.get("event_type") == "cart_changed"
            for event in session_events
        )
    }


    scenario = detect_scenario(
        session_data
    )


    # ========================================================
    # STEP 4
    # ACTION ENGINE
    # ========================================================

    action, action_reason = recommend_action(

        risk_level=risk["risk_level"],

        abandonment_probability=
            risk["abandonment_probability"],

        scenario=scenario["scenario"]
    )


    # ========================================================
    # FINAL DECISION
    # ========================================================

    return {

        "risk": risk,

        "scenario": scenario,

        "decision": {

            "action": action,

            "reason": action_reason
        }
    }