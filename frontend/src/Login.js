import React, { useState } from "react";
import "./Login.css";

// In dev, package.json "proxy" sends requests to backend (e.g. http://localhost:8000)
const authUrl = (path) => path;

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const submitHandler = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const endpoint = isRegister ? "/register" : "/login";
      const body = { email, password };
      const res = await fetch(authUrl(endpoint), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        // Backend may return detail as string or array (validation errors)
        let msg = data.detail || data.message;
        if (Array.isArray(msg)) msg = msg.map((e) => e.msg || e.message).join(". ");
        if (!msg) msg = `Request failed (${res.status}). Is the backend running on port 8000?`;
        setError(msg);
        setLoading(false);
        return;
      }
      if (isRegister) {
        setSuccess("Account created. You can log in now.");
        setError("");
        setIsRegister(false);
        setPassword("");
        setLoading(false);
        return;
      }
      // Login success: store token and user, then notify parent
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify({ email }));
      onLogin({ email, token: data.access_token });
    } catch (err) {
      setError(err.message || "Network error");
    }
    setLoading(false);
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>{isRegister ? "Create Account" : "Welcome Back"}</h2>
        <p className="subtitle">
          {isRegister
            ? "Register to get job alerts"
            : "Login to your dashboard"}
        </p>

        {error && <p className="auth-error">{error}</p>}
        {success && <p className="auth-success">{success}</p>}
        <form onSubmit={submitHandler}>
          <input
            type="email"
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Please wait…" : isRegister ? "Register" : "Login"}
          </button>
        </form>

        <p className="switch">
          {isRegister ? "Already have an account?" : "New user?"}
          <span onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? " Login" : " Register"}
          </span>
        </p>
      </div>
    </div>
  );
}

export default Login;
