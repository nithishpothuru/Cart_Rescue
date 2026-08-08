import { useEffect, useState } from "react";
import axios from "axios";
import { useSession } from "../../context/SessionContext";
import AdminLayout from "./AdminLayout";

const API = "http://127.0.0.1:5000";

function Analytics() {
  const { user } = useSession();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`${API}/api/admin/analytics?user_id=${user.user_id}`)
      .then((res) => {
        if (res.data.success) {
          setData(res.data.analytics);
        }
      })
      .catch((err) => {
        console.error("Failed to load analytics", err);
      })
      .finally(() => setLoading(false));
  }, [user]);

  if (loading) {
    return (
      <AdminLayout title="Analytics">
        <p className="empty-text">Loading analytics...</p>
      </AdminLayout>
    );
  }

  const risk = data?.risk_breakdown || {};
  const actions = data?.actions || {};
  const scenarios = data?.scenarios || [];

  return (
    <AdminLayout title="Analytics">
      {/* Summary Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div>
            <h3>{data?.total_sessions ?? 0}</h3>
            <p>Total Sessions</p>
          </div>
        </div>
        <div className="stat-card danger">
          <div>
            <h3>{risk.HIGH ?? 0}</h3>
            <p>High Risk</p>
          </div>
        </div>
        <div className="stat-card">
          <div>
            <h3>{risk.MEDIUM ?? 0}</h3>
            <p>Medium Risk</p>
          </div>
        </div>
        <div className="stat-card">
          <div>
            <h3>{risk.LOW ?? 0}</h3>
            <p>Low Risk</p>
          </div>
        </div>
      </div>

      <div className="session-detail-grid">
        {/* Actions Taken */}
        <div className="admin-card">
          <h2>Admin Actions</h2>
          <div className="analytics-row">
            <span>Accepted</span>
            <strong style={{ color: "#16a34a" }}>{actions.accepted ?? 0}</strong>
          </div>
          <div className="analytics-row">
            <span>Ignored</span>
            <strong style={{ color: "#64748b" }}>{actions.ignored ?? 0}</strong>
          </div>
        </div>

        {/* Risk Breakdown */}
        <div className="admin-card">
          <h2>Risk Breakdown</h2>
          <div className="analytics-row">
            <span className="risk-HIGH">HIGH</span>
            <strong>{risk.HIGH ?? 0}</strong>
          </div>
          <div className="analytics-row">
            <span className="risk-MEDIUM">MEDIUM</span>
            <strong>{risk.MEDIUM ?? 0}</strong>
          </div>
          <div className="analytics-row">
            <span className="risk-LOW">LOW</span>
            <strong>{risk.LOW ?? 0}</strong>
          </div>
        </div>
      </div>

      {/* Scenarios */}
      <div className="admin-card">
        <h2>Top Scenarios</h2>
        {scenarios.length === 0 ? (
          <p className="empty-text">No scenario data yet</p>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>Scenario</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {scenarios.map((s, i) => (
                <tr key={i}>
                  <td>{s._id || "Unknown"}</td>
                  <td>{s.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AdminLayout>
  );
}

export default Analytics;