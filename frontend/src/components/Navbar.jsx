import { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ShoppingCart, Search, Heart, Bell, LogOut, User } from "lucide-react";
import { useSession } from "../context/SessionContext";

function Navbar() {
  const { cart, user, logout } = useSession();
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setShowProfileMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    setShowProfileMenu(false);
    navigate("/");
  };

  return (
    <header className="navbar">
      <div className="navbar-container">
        <Link to="/shop" className="logo">
          <ShoppingCart size={24} strokeWidth={2.2} />
          <span>
            CartRescue <strong>AI</strong>
          </span>
        </Link>

        <div className="search-bar">
          <Search size={16} />
          <input placeholder="Search premium products, tech gear, design items..." />
        </div>

        <div className="nav-actions">
          <button className="icon-btn">
            <Bell size={20} />
            <span className="badge">3</span>
          </button>

          <button className="icon-btn">
            <Heart size={20} />
          </button>

          {/* Cart Button → goes to Cart page */}
          <Link to="/cart" className="icon-btn cart-btn">
            <ShoppingCart size={20} />
            {cartCount > 0 && <span className="badge">{cartCount}</span>}
          </Link>

          {user ? (
            <div className="profile-wrapper" ref={menuRef}>
              <button
                className="user-avatar"
                onClick={() => setShowProfileMenu(!showProfileMenu)}
              >
                {user.full_name?.[0]?.toUpperCase() || "U"}
              </button>

              {showProfileMenu && (
                <div className="profile-dropdown">
                  <div className="profile-info">
                    <User size={16} />
                    <div>
                      <strong>{user.full_name}</strong>
                      <p>{user.email}</p>
                    </div>
                  </div>
                  <hr />
                  <button className="logout-btn" onClick={handleLogout}>
                    <LogOut size={16} />
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link to="/login" className="login-btn">
                Login
              </Link>
              <Link to="/register" className="register-btn">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default Navbar;
