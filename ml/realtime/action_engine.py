def recommend_action(risk_level, abandonment_probability, scenario):
    """
    Recommend the best intervention action.
    """
    if risk_level == "HIGH":
        if scenario == "PAYMENT_FAILURE":
            return "OFFER_COD_OR_ALTERNATE_PAYMENT", "Payment failed – offer COD or different method + small discount"
        if scenario == "PRICE_SENSITIVE":
            return "SHOW_LIMITED_TIME_DISCOUNT", "High price sensitivity – show 10-15% flash discount"
        if scenario == "SHIPPING_FRICTION":
            return "OFFER_FREE_SHIPPING", "Shipping friction detected – offer free shipping"
        return "SHOW_EXIT_INTENT_POPUP", "High risk of abandonment – show exit-intent offer"

    if risk_level == "MEDIUM":
        if scenario == "CHECKOUT_HESITATION":
            return "SHOW_TRUST_BADGES_AND_REVIEWS", "Hesitation at checkout – reinforce trust"
        if scenario == "CART_ABANDONMENT_RISK":
            return "SEND_CART_REMINDER", "Items sitting in cart – schedule reminder"
        return "SHOW_PERSONALIZED_RECOMMENDATION", "Medium risk – show related products"

    # LOW risk
    return "NO_ACTION", "Low abandonment risk – continue normal experience"
    