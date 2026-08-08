def detect_scenario(session_data):
    """
    Detect the most likely abandonment scenario.
    """
    if session_data.get("payment_failed"):
        return {
            "scenario": "PAYMENT_FAILURE",
            "confidence": 0.92,
            "description": "User attempted payment but it failed."
        }

    if session_data.get("checkout_started") and not session_data.get("payment_attempt"):
        return {
            "scenario": "CHECKOUT_HESITATION",
            "confidence": 0.85,
            "description": "User started checkout but did not proceed to payment."
        }

    if session_data.get("has_cart") and session_data.get("price_comparison"):
        return {
            "scenario": "PRICE_SENSITIVE",
            "confidence": 0.78,
            "description": "User is comparing prices and may leave for a better deal."
        }

    if session_data.get("shipping_cost_viewed") or session_data.get("delivery_date_changed"):
        return {
            "scenario": "SHIPPING_FRICTION",
            "confidence": 0.80,
            "description": "Shipping cost or delivery date is causing hesitation."
        }

    if session_data.get("form_repeated"):
        return {
            "scenario": "FORM_FRICTION",
            "confidence": 0.75,
            "description": "User is struggling with form fields."
        }

    if session_data.get("has_cart"):
        return {
            "scenario": "CART_ABANDONMENT_RISK",
            "confidence": 0.65,
            "description": "Items in cart but no further progress."
        }

    return {
        "scenario": "BROWSING",
        "confidence": 0.50,
        "description": "Normal browsing behavior."
    }
    