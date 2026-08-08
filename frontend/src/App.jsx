import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Shop from "./pages/Shop";
import Cart from "./pages/Cart";
import AdminDashboard from "./pages/admin/AdminDashboard";
import LiveSessions from "./pages/admin/LiveSessions";
import HighRiskSessions from "./pages/admin/HighRiskSessions";
import SessionDetail from "./pages/admin/SessionDetail";
import ActionHistory from "./pages/admin/ActionHistory";
import Analytics from "./pages/admin/Analytics";
import { SessionProvider, useSession } from "./context/SessionContext";

// Protect Admin routes
function AdminRoute({ children }) {
  const { user } = useSession();
  if (!user || user.role !== "super_admin") {
    return <Navigate to="/login" replace />;
  }
  return children;
}

// Protect Customer routes (optional – mostly open)
function CustomerRoute({ children }) {
  return children;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Customer */}
      <Route path="/shop" element={<Shop />} />
      <Route path="/cart" element={<Cart />} />

      {/* Super Admin */}
      <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
      <Route path="/admin/live" element={<AdminRoute><LiveSessions /></AdminRoute>} />
      <Route path="/admin/high-risk" element={<AdminRoute><HighRiskSessions /></AdminRoute>} />
      <Route path="/admin/session/:sessionId" element={<AdminRoute><SessionDetail /></AdminRoute>} />
      <Route path="/admin/actions" element={<AdminRoute><ActionHistory /></AdminRoute>} />
      <Route path="/admin/analytics" element={<AdminRoute><Analytics /></AdminRoute>} />
    </Routes>
  );
}

function App() {
  return (
    <SessionProvider>
      <AppRoutes />
    </SessionProvider>
  );
}

export default App;