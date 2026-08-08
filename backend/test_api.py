import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"


def print_response(title, response):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print("Status:", response.status_code)

    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print(response.text)


# ============================================================
# 1. START SESSION
# ============================================================

print("\nStarting test session...")

response = requests.post(
    f"{BASE_URL}/api/session/start",
    json={
        "user_id": "test_user_001"
    }
)

print_response("SESSION START", response)

if response.status_code not in [200, 201]:
    print("\nSession creation failed.")
    exit()

data = response.json()

session_id = data.get("session_id")

if not session_id:
    print("\nNo session_id returned by backend.")
    exit()

print("\nSession ID:", session_id)


# ============================================================
# Helper function
# ============================================================

def send_event(event):
    event["session_id"] = session_id

    response = requests.post(
        f"{BASE_URL}/api/session/event",
        json=event
    )

    print_response(
        f"EVENT: {event['event_type']}",
        response
    )

    time.sleep(1)


# ============================================================
# 2. PRODUCT VIEW
# ============================================================

send_event({
    "event_type": "product_view",
    "product_id": "P1001",
    "category": "Electronics",
    "brand": "Samsung",
    "price": 50000
})


# ============================================================
# 3. SECOND PRODUCT VIEW
# ============================================================

send_event({
    "event_type": "product_view",
    "product_id": "P1002",
    "category": "Electronics",
    "brand": "Apple",
    "price": 45000
})


# ============================================================
# 4. ADD TO CART
# ============================================================

send_event({
    "event_type": "add_to_cart",
    "product_id": "P1001",
    "category": "Electronics",
    "brand": "Samsung",
    "price": 50000
})


# ============================================================
# 5. START CHECKOUT
# ============================================================

send_event({
    "event_type": "checkout_started"
})


# ============================================================
# 6. PAYMENT ATTEMPT
# ============================================================

send_event({
    "event_type": "payment_attempt",
    "payment_method": "UPI"
})


# ============================================================
# 7. PAYMENT FAILURE
# ============================================================

send_event({
    "event_type": "payment_failed",
    "payment_method": "UPI"
})


# ============================================================
# 8. REQUEST REAL-TIME DECISION
# ============================================================

print("\n" + "=" * 60)
print("REQUESTING CARTGUARD DECISION")
print("=" * 60)

response = requests.post(
    f"{BASE_URL}/api/session/decision",
    json={
        "session_id": session_id
    }
)

print_response("CARTGUARD DECISION", response)


print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)