import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useSession } from "../../context/SessionContext";
import AdminLayout from "./AdminLayout";

const API = "http://127.0.0.1:5000";

function LiveSessions() {
  const { user } = useSession();
  const [sessions, setSessions] = useState([]);
  const [filter, setFilter] = useState("all"); // all | active | inactive

  const loadSessions = () => {
    axios
      .get(`${API}/api/admin/sessions/live?user_id=${user.user_id}`)
      .then((res) => {
        if (res.data.success) setSessions(res.data.sessions);
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    loadSessions();
    const interval = setInterval(loadSessions, 10000); // auto refresh every 10s
    return () => clearInterval(interval);
  }, [user]);

  const filteredSessions = sessions.filter((s) => {
    if (filter === "active") return s.status === "active";
    if (filter === "inactive") return s.status === "inactive";
    return true;
  });

  const activeCount = sessions.filter((s) => s.status === "active").length;
  const inactiveCount = sessions.filter((s) => s.status === "inactive").length;

  return (
    <AdminLayout title="Customer Sessions">
      {/* Filter Tabs */}
      <div className="filter-tabs">
        <button
          className={filter === "all" ? "active" : ""}
          onClick={() => setFilter("all")}
        >
          All ({sessions.length})
        </button>
        <button
          className={filter === "active" ? "active" : ""}
          onClick={() => setFilter("active")}
        >
          🟢 Active ({activeCount})
        </button>
        <button
          className={filter === "inactive" ? "active" : ""}
          onClick={() => setFilter("inactive")}
        >
          ⚪ Inactive ({inactiveCount})
        </button>
      </div>

      <div className="admin-card">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Session ID</th>
              <th>User</th>
              <th>Status</th>
              <th>Cart Value</th>
              <th>Risk Level</th>
              <th>Last Activity</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredSessions.map((s) => (
              <tr key={s.session_id}>
                <td>{s.session_id?.slice(0, 12)}...</td>
                <td>{s.user_id ? s.user_id.slice(0, 8) + "..." : "Guest"}</td>
                <td>
                  <span className={`status-badge status-${s.status}`}>
                    {s.status === "active" ? "🟢 Active" : "⚪ Inactive"}
                  </span>
                </td>
                <td>${Number(s.cart_value || 0).toFixed(2)}</td>
                <td>
                  <span className={`risk-${s.risk_level || "LOW"}`}>
                    {s.risk_level || "—"}
                  </span>
                </td>
                <td>
                  {s.last_activity
                    ? new Date(s.last_activity).toLocaleString()
                    : "—"}
                </td>
                <td>
                  <Link
                    to={`/admin/session/${s.session_id}`}
                    className="view-btn"
                  >
                    Open
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredSessions.length === 0 && (
          <p className="empty-text">No sessions found</p>
        )}
      </div>
    </AdminLayout>
  );
}

export default LiveSessions;
