def generate_features(events):
    """
    Convert list of events into feature dictionary for the model.
    """
    if not events:
        return {}

    event_types = [e.get("event_type") for e in events]
    prices = [float(e.get("price", 0)) for e in events if e.get("price")]

    features = {
        "num_events": len(events),
        "num_product_views": event_types.count("product_view"),
        "num_add_to_cart": event_types.count("add_to_cart"),
        "num_checkout_started": event_types.count("checkout_started"),
        "num_payment_attempt": event_types.count("payment_attempt"),
        "num_payment_failed": event_types.count("payment_failed"),
        "has_cart": 1 if "add_to_cart" in event_types else 0,
        "has_checkout": 1 if "checkout_started" in event_types else 0,
        "has_payment_fail": 1 if "payment_failed" in event_types else 0,
        "avg_price": sum(prices) / len(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "total_cart_value": sum(prices),
        "session_duration_sec": 0,  # can be calculated from timestamps later
    }
    return features
