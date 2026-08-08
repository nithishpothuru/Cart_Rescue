import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { Sparkles } from "lucide-react";
import "./Auth.css";

const API = "http://127.0.0.1:5000";

function Register() {
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    password: "",
    confirm: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const passwordStrength = () => {
    const p = form.password;
    if (p.length === 0) return { level: 0, text: "" };
    if (p.length < 6) return { level: 1, text: "Weak" };
    if (p.length < 10) return { level: 2, text: "Medium" };
    return { level: 3, text: "Strong" };
  };

  const strength = passwordStrength();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (form.password !== form.confirm) {
      setError("Passwords do not match");
      return;
    }

    if (form.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      const res = await axios.post(`${API}/api/auth/register`, {
        full_name: form.full_name,
        email: form.email,
        phone: form.phone,
        password: form.password,
      });

      if (res.data.success) {
        setSuccess("Account created successfully! Redirecting to login...");
        setTimeout(() => {
          navigate("/login");
        }, 1500);
      }
    } catch (err) {
      console.error("Register error:", err);
      setError(
        err.response?.data?.error || 
        "Registration failed. Please check if backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page register-page">
      <div className="auth-left">
        <div className="auth-brand">
          <Sparkles size={20} />
          <span>CartRescue AI</span>
        </div>

        <h1>Create Your Account</h1>
        <p className="auth-subtitle">
          Join premium shoppers saving time & securing exclusive drops with
          CartRescue AI.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              name="full_name"
              placeholder="Jonathan Doe"
              value={form.full_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Email Address</label>
              <input
                name="email"
                type="email"
                placeholder="john.doe@example.com"
                value={form.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Phone Number</label>
              <input
                name="phone"
                placeholder="+1 (555) 019-2834"
                value={form.phone}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Choose Password</label>
            <input
              name="password"
              type="password"
              placeholder="••••••••••••"
              value={form.password}
              onChange={handleChange}
              required
            />
            {form.password && (
              <div className="strength-bar">
                <div className={`bar level-${strength.level}`}></div>
                <span>Password strength: {strength.text}</span>
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Confirm Password</label>
            <input
              name="confirm"
              type="password"
              placeholder="••••••••••••"
              value={form.confirm}
              onChange={handleChange}
              required
            />
          </div>

          {error && <p className="error-msg">{error}</p>}
          {success && <p className="success-msg">{success}</p>}

          <button type="submit" className="primary-btn full" disabled={loading}>
            {loading ? "Creating Account..." : "Create Account"}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>

      <div className="auth-right">
        <div className="floating-card">
          <img
            src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=120"
            alt="product"
          />
          <div>
            <strong>HoloBuds Pro</strong>
            <p className="saved">Cart rescued! Saved 10%</p>
            <p className="price">$129.00</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
