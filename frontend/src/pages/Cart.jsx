import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useSession } from "../context/SessionContext";
import { Minus, Plus, Trash2, ShoppingBag } from "lucide-react";
import "./Cart.css";

function Cart() {
  const { cart, updateQuantity, removeFromCart, clearCart, trackEvent } =
    useSession();
  const [showPayment, setShowPayment] = useState(false);
  const [selectedPayment, setSelectedPayment] = useState("upi");
  const [processing, setProcessing] = useState(false);
  const navigate = useNavigate();

  const subtotal = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const shipping = subtotal > 100 ? 0 : 9.99;
  const total = subtotal + shipping;

  const handleCheckout = () => {
    if (cart.length === 0) return;
    setShowPayment(true);
    trackEvent({ event_type: "checkout_started" });
  };

  const handlePayment = async () => {
    setProcessing(true);
    await trackEvent({
      event_type: "payment_attempt",
      payment_method: selectedPayment,
    });

    // Simulate payment
    setTimeout(async () => {
      // Randomly succeed or fail for demo (80% success)
      const success = Math.random() > 0.2;

      if (success) {
        await trackEvent({
          event_type: "payment_success",
          payment_method: selectedPayment,
        });
        clearCart();
        setShowPayment(false);
        setProcessing(false);
        alert("Payment successful! Thank you for your order.");
        navigate("/shop");
      } else {
        await trackEvent({
          event_type: "payment_failed",
          payment_method: selectedPayment,
        });
        setProcessing(false);
        alert("Payment failed. Please try again or choose another method.");
      }
    }, 1800);
  };

  if (cart.length === 0) {
    return (
      <div className="cart-page">
        <Navbar />
        <div className="empty-cart">
          <ShoppingBag size={64} strokeWidth={1.2} />
          <h2>Your cart is empty</h2>
          <p>Looks like you haven’t added anything yet.</p>
          <Link to="/shop" className="primary-btn">
            Continue Shopping
          </Link>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="cart-page">
      <Navbar />

      <div className="cart-container">
        <h1>Shopping Cart ({cart.length} items)</h1>

        <div className="cart-layout">
          {/* Left - Items */}
          <div className="cart-items">
            {cart.map((item) => (
              <div className="cart-item" key={item.product_id}>
                <img src={item.image} alt={item.name} />
                <div className="item-details">
                  <h3>{item.name}</h3>
                  <p className="item-category">{item.category}</p>
                  <p className="item-price">${item.price.toFixed(2)}</p>
                </div>

                <div className="quantity-controls">
                  <button
                    onClick={() =>
                      updateQuantity(item.product_id, item.quantity - 1)
                    }
                  >
                    <Minus size={16} />
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    onClick={() =>
                      updateQuantity(item.product_id, item.quantity + 1)
                    }
                  >
                    <Plus size={16} />
                  </button>
                </div>

                <div className="item-total">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>

                <button
                  className="remove-btn"
                  onClick={() => removeFromCart(item.product_id)}
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))}
          </div>

          {/* Right - Summary */}
          <div className="cart-summary">
            <h2>Order Summary</h2>
            <div className="summary-row">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Shipping</span>
              <span>{shipping === 0 ? "FREE" : `$${shipping.toFixed(2)}`}</span>
            </div>
            <hr />
            <div className="summary-row total">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>

            <button className="checkout-btn" onClick={handleCheckout}>
              Proceed to Checkout
            </button>

            <Link to="/shop" className="continue-shopping">
              ← Continue Shopping
            </Link>
          </div>
        </div>
      </div>

      {/* Payment Modal */}
      {showPayment && (
        <div className="payment-modal-overlay">
          <div className="payment-modal">
            <h2>Select Payment Method</h2>
            <p className="payment-amount">
              Amount to pay: <strong>${total.toFixed(2)}</strong>
            </p>

            <div className="payment-options">
              {[
                { id: "upi", label: "UPI / GPay / PhonePe" },
                { id: "card", label: "Credit / Debit Card" },
                { id: "netbanking", label: "Net Banking" },
                { id: "cod", label: "Cash on Delivery" },
              ].map((opt) => (
                <label
                  key={opt.id}
                  className={`payment-option ${
                    selectedPayment === opt.id ? "selected" : ""
                  }`}
                >
                  <input
                    type="radio"
                    name="payment"
                    value={opt.id}
                    checked={selectedPayment === opt.id}
                    onChange={() => setSelectedPayment(opt.id)}
                  />
                  {opt.label}
                </label>
              ))}
            </div>

            <div className="payment-actions">
              <button
                className="cancel-btn"
                onClick={() => setShowPayment(false)}
                disabled={processing}
              >
                Cancel
              </button>
              <button
                className="pay-btn"
                onClick={handlePayment}
                disabled={processing}
              >
                {processing ? "Processing..." : `Pay $${total.toFixed(2)}`}
              </button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
}

export default Cart;
