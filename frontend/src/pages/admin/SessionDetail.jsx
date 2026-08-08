import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { useSession } from "../../context/SessionContext";
import AdminLayout from "./AdminLayout";

const API = "http://127.0.0.1:5000";

function SessionDetail() {
  const { sessionId } = useParams();
  const { user } = useSession();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios
      .get(
        `${API}/api/admin/sessions/${sessionId}?user_id=${user.user_id}`
      )
      .then((res) => {
        if (res.data.success) setData(res.data);
      })
      .finally(() => setLoading(false));
  }, [sessionId, user]);

  const handleAction = async (choice) => {
    setActionLoading(true);
    setMessage("");
    try {
      const res = await axios.post(
        `${API}/api/admin/sessions/${sessionId}/action`,
        {
          user_id: user.user_id,
          choice,
          suggested_action: data?.decision?.decision?.action,
          customer_phone: data?.session?.phone || null, // you can store phone later
        }
      );
      if (res.data.success) {
        setMessage(
          choice === "accept"
            ? "✅ Action accepted. Twilio notification sent (if configured)."
            : "Action ignored."
        );
        setTimeout(() => navigate("/admin/high-risk"), 1500);
      }
    } catch (err) {
      setMessage("Failed to process action");
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <AdminLayout title="Session Detail">
        <p>Loading...</p>
      </AdminLayout>
    );
  }

  const decision = data?.decision;

  return (
    <AdminLayout title="Session Detail">
      <div className="session-detail-grid">
        <div className="admin-card">
          <h2>Session Info</h2>
          <p><strong>ID:</strong> {data?.session?.session_id}</p>
          <p><strong>Status:</strong> {data?.session?.status}</p>
          <p><strong>Started:</strong> {new Date(data?.session?.started_at).toLocaleString()}</p>
          <p><strong>Events:</strong> {data?.events?.length || 0}</p>
        </div>

        <div className="admin-card decision-card">
          <h2>AI Recommendation</h2>
          {decision ? (
            <>
              <div className="risk-badge-large">
                Risk: <span className={`risk-${decision.risk.risk_level}`}>
                  {decision.risk.risk_level}
                </span>
                ({decision.risk.abandonment_probability * 100}%)
              </div>
              <p><strong>Scenario:</strong> {decision.scenario.scenario}</p>
              <p><strong>Description:</strong> {decision.scenario.description}</p>
              <p><strong>Suggested Action:</strong></p>
              <div className="suggested-action">
                {decision.decision.action}
              </div>
              <p className="reason">{decision.decision.reason}</p>

              <div className="action-buttons">
                <button
                  className="accept-btn"
                  onClick={() => handleAction("accept")}
                  disabled={actionLoading}
                >
                  {actionLoading ? "Processing..." : "✅ Accept & Send"}
                </button>
                <button
                  className="ignore-btn"
                  onClick={() => handleAction("ignore")}
                  disabled={actionLoading}
                >
                  Ignore
                </button>
              </div>
              {message && <p className="action-message">{message}</p>}
            </>
          ) : (
            <p>No decision available (not enough events)</p>
          )}
        </div>
      </div>

      <div className="admin-card">
        <h2>Event Timeline</h2>
        <div className="event-timeline">
          {data?.events?.map((e, i) => (
            <div key={i} className="event-item">
              <span className="event-type">{e.event_type}</span>
              <span className="event-time">
                {new Date(e.timestamp).toLocaleTimeString()}
              </span>
              {e.product_id && <span>Product: {e.product_id}</span>}
              {e.price > 0 && <span>${e.price}</span>}
            </div>
          ))}
        </div>
      </div>
    </AdminLayout>
  );
}

export default SessionDetail;