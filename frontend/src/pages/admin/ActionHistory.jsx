import { useEffect, useState } from "react";
import axios from "axios";
import { useSession } from "../../context/SessionContext";
import AdminLayout from "./AdminLayout";

const API = "http://127.0.0.1:5000";

function ActionHistory() {
  const { user } = useSession();
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`${API}/api/admin/actions?user_id=${user.user_id}`)
      .then((res) => {
        if (res.data.success) {
          setActions(res.data.actions || []);
        }
      })
      .catch((err) => {
        console.error("Failed to load actions", err);
      })
      .finally(() => setLoading(false));
  }, [user]);

  return (
    <AdminLayout title="Action History">
      <div className="admin-card">
        {loading ? (
          <p className="empty-text">Loading...</p>
        ) : actions.length === 0 ? (
          <p className="empty-text">No actions taken yet</p>
        ) : (
          <table className="admin-table">
            <thead>
              <tr>
                <th>Decision ID</th>
                <th>Session</th>
                <th>Suggested Action</th>
                <th>Choice</th>
                <th>Twilio</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {actions.map((a) => (
                <tr key={a.decision_id}>
                  <td>{a.decision_id?.slice(0, 8)}...</td>
                  <td>{a.session_id?.slice(0, 10)}...</td>
                  <td>{a.suggested_action || "—"}</td>
                  <td>
                    <span className={`badge-${a.choice}`}>
                      {a.choice}
                    </span>
                  </td>
                  <td>
                    {a.twilio_result?.success
                      ? `✅ ${a.twilio_result.type}`
                      : a.twilio_result
                      ? "❌ Failed"
                      : "—"}
                  </td>
                  <td>
                    {a.created_at
                      ? new Date(a.created_at).toLocaleString()
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AdminLayout>
  );
}

export default ActionHistory;