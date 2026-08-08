import { useEffect, useState } from "react";
import axios from "axios";
import { useSession } from "../../context/SessionContext";
import AdminLayout from "./AdminLayout";
import { Activity, AlertTriangle, Users, Zap } from "lucide-react";

const API = "http://127.0.0.1:5000";

function AdminDashboard() {
  const { user } = useSession();
  const [stats, setStats] = useState(null);
  const [recent, setRecent] = useState([]);

  useEffect(() => {
    axios
      .get(`${API}/api/admin/dashboard?user_id=${user.user_id}`)
      .then((res) => {
        if (res.data.success) {
          setStats(res.data.stats);
          setRecent(res.data.recent_actions || []);
        }
      });
  }, [user]);

  return (
    <AdminLayout title="Dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <Activity size={22} />
          <div>
            <h3>{stats?.active_sessions ?? "—"}</h3>
            <p>Live Sessions</p>
          </div>
        </div>
        <div className="stat-card danger">
          <AlertTriangle size={22} />
          <div>
            <h3>{stats?.high_risk_sessions ?? "—"}</h3>
            <p>High Risk</p>
          </div>
        </div>
        <div className="stat-card">
          <Zap size={22} />
          <div>
            <h3>{stats?.total_sessions ?? "—"}</h3>
            <p>Total Sessions</p>
          </div>
        </div>
        <div className="stat-card">
          <Users size={22} />
          <div>
            <h3>{stats?.total_customers ?? "—"}</h3>
            <p>Customers</p>
          </div>
        </div>
      </div>

      <div className="admin-card">
        <h2>Recent Actions</h2>
        {recent.length === 0 ? (
          <p className="empty-text">No actions yet</p>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>Session</th>
                <th>Action</th>
                <th>Choice</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {recent.map((a) => (
                <tr key={a.decision_id}>
                  <td>{a.session_id?.slice(0, 8)}...</td>
                  <td>{a.suggested_action}</td>
                  <td>
                    <span className={`badge-${a.choice}`}>
                      {a.choice}
                    </span>
                  </td>
                  <td>{new Date(a.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AdminLayout>
  );
}

export default AdminDashboard;