import os
import pickle
import numpy as np

MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "saved_models", "xgboost.pkl"
)

def score_session(features):
    """
    Score the session using XGBoost model (or fallback rule-based).
    """
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)

            # Create feature vector in expected order
            feature_order = [
                "num_events", "num_product_views", "num_add_to_cart",
                "num_checkout_started", "num_payment_attempt", "num_payment_failed",
                "has_cart", "has_checkout", "has_payment_fail",
                "avg_price", "max_price", "total_cart_value", "session_duration_sec"
            ]
            X = np.array([[features.get(f, 0) for f in feature_order]])
            prob = float(model.predict_proba(X)[0][1])
        else:
            # Fallback rule-based scoring
            prob = _rule_based_score(features)
    except Exception:
        prob = _rule_based_score(features)

    if prob >= 0.75:
        risk_level = "HIGH"
    elif prob >= 0.45:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "abandonment_probability": round(prob, 4),
        "risk_level": risk_level,
        "risk_score": round(prob * 100, 2),
    }


def _rule_based_score(features):
    score = 0.15
    if features.get("has_cart"):
        score += 0.15
    if features.get("has_checkout"):
        score += 0.20
    if features.get("has_payment_fail"):
        score += 0.35
    if features.get("num_product_views", 0) > 3:
        score += 0.10
    if features.get("num_add_to_cart", 0) > 1:
        score += 0.10
    return min(score, 0.95)
    