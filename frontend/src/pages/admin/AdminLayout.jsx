import { Link, useLocation, useNavigate } from "react-router-dom";
import { useSession } from "../../context/SessionContext";
import {
  LayoutDashboard,
  Activity,
  AlertTriangle,
  History,
  BarChart3,
  LogOut,
  ShoppingCart,
  Store,
} from "lucide-react";
import "./Admin.css";

function AdminLayout({ children, title }) {
  const { user, logout } = useSession();
  const location = useLocation();
  const navigate = useNavigate();

  const menu = [
    { path: "/admin", label: "Dashboard", icon: LayoutDashboard },
    { path: "/admin/live", label: "Live Sessions", icon: Activity },
    { path: "/admin/high-risk", label: "High Risk", icon: AlertTriangle },
    { path: "/admin/actions", label: "Action History", icon: History },
    { path: "/admin/analytics", label: "Analytics", icon: BarChart3 },
  ];

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-logo">
          <ShoppingCart size={22} />
          <span>
            CartRescue <strong>Admin</strong>
          </span>
        </div>

        <nav>
          {menu.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`admin-nav-item ${active ? "active" : ""}`}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* ✅ Button to go to Shopping page */}
        <Link to="/shop" className="go-shop-btn">
          <Store size={18} />
          Go to Shop
        </Link>

        <div className="admin-user">
          <div className="admin-avatar">
            {user?.full_name?.[0]?.toUpperCase() || "A"}
          </div>
          <div>
            <strong>{user?.full_name || "Admin"}</strong>
            <p>Super Admin</p>
          </div>
          <button onClick={handleLogout} title="Logout">
            <LogOut size={18} />
          </button>
        </div>
      </aside>

      <main className="admin-main">
        <header className="admin-header">
          <h1>{title}</h1>
        </header>
        <div className="admin-content">{children}</div>
      </main>
    </div>
  );
}

export default AdminLayout;
