import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const API = "http://127.0.0.1:5000";
const SessionContext = createContext();

export function SessionProvider({ children }) {
  const [sessionId, setSessionId] = useState(
    localStorage.getItem("session_id") || null
  );
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("user") || "null")
  );
  const [cart, setCart] = useState(
    JSON.parse(localStorage.getItem("cart") || "[]")
  );
  const [toast, setToast] = useState(null); // for success messages

  // Persist cart
  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  // Start session
  useEffect(() => {
    if (!sessionId) {
      startSession();
    }
  }, []);

  const startSession = async () => {
    try {
      const res = await axios.post(`${API}/api/session/start`, {
        user_id: user?.user_id || null,
      });
      if (res.data.success) {
        setSessionId(res.data.session_id);
        localStorage.setItem("session_id", res.data.session_id);
      }
    } catch (err) {
      console.error("Failed to start session", err);
    }
  };

  const trackEvent = async (eventData) => {
    if (!sessionId) return;
    try {
      await axios.post(`${API}/api/session/event`, {
        session_id: sessionId,
        ...eventData,
      });
    } catch (err) {
      console.error("Failed to track event", err);
    }
  };

  // Show toast message
  const showToast = (message, type = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 2500);
  };

  // Add to cart with quantity
  const addToCart = async (product, quantity = 1) => {
    setCart((prev) => {
      const exists = prev.find((p) => p.product_id === product.product_id);
      if (exists) {
        return prev.map((p) =>
          p.product_id === product.product_id
            ? { ...p, quantity: p.quantity + quantity }
            : p
        );
      }
      return [...prev, { ...product, quantity }];
    });

    await trackEvent({
      event_type: "add_to_cart",
      product_id: product.product_id,
      category: product.category,
      brand: product.brand || "CartRescue",
      price: product.price,
    });

    showToast("Added successfully to cart!");
  };

  // Update quantity in cart
  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) {
      removeFromCart(productId);
      return;
    }
    setCart((prev) =>
      prev.map((item) =>
        item.product_id === productId
          ? { ...item, quantity: newQuantity }
          : item
      )
    );
  };

  // Remove item
  const removeFromCart = (productId) => {
    setCart((prev) => prev.filter((item) => item.product_id !== productId));
    showToast("Item removed from cart", "info");
  };

  // Clear cart after successful checkout
  const clearCart = () => {
    setCart([]);
    localStorage.removeItem("cart");
  };

const login = (userData) => {
  setUser(userData);   // userData now contains role
  localStorage.setItem("user", JSON.stringify(userData));
};

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
    showToast("Logged out successfully", "info");
  };

  return (
    <SessionContext.Provider
      value={{
        sessionId,
        user,
        cart,
        toast,
        trackEvent,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        login,
        logout,
        startSession,
        showToast,
      }}
    >
      {children}
      {/* Global Toast */}
      {toast && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}
    </SessionContext.Provider>
  );
}

export const useSession = () => useContext(SessionContext);
