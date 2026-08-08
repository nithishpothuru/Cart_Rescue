import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useSession } from "../../context/SessionContext";
import AdminLayout from "./AdminLayout";

const API = "http://127.0.0.1:5000";

function HighRiskSessions() {
  const { user } = useSession();
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    axios
      .get(`${API}/api/admin/sessions/high-risk?user_id=${user.user_id}`)
      .then((res) => {
        if (res.data.success) setSessions(res.data.sessions);
      });
  }, [user]);

  return (
    <AdminLayout title="High Risk Sessions">
      <div className="admin-card">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Session ID</th>
              <th>Status</th>
              <th>Risk Score</th>
              <th>Scenario</th>
              <th>Recommended Action</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((s) => (
              <tr key={s.session_id}>
                <td>{s.session_id?.slice(0, 12)}...</td>
                <td>
                  <span className={`status-badge status-${s.status}`}>
                    {s.status === "active" ? "🟢 Active" : "⚪ Inactive"}
                  </span>
                </td>
                <td>{s.risk_score ?? "—"}</td>
                <td>{s.scenario || "—"}</td>
                <td>{s.recommended_action || "—"}</td>
                <td>
                  <Link
                    to={`/admin/session/${s.session_id}`}
                    className="view-btn"
                  >
                    Review
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {sessions.length === 0 && (
          <p className="empty-text">No high-risk sessions</p>
        )}
      </div>
    </AdminLayout>
  );
}

export default HighRiskSessions;
