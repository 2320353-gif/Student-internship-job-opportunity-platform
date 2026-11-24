import React, { useState } from "react";
import { User, LoginPayload, RegisterPayload } from "../types/auth";
import * as authService from "../services/auth";

interface LoginPageProps {
  onLoginSuccess: (user: User) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const [isSignup, setIsSignup] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (isSignup) {
      if (!name.trim()) {
        setError("Please enter your full name.");
        return;
      }
      if (password.length < 6) {
        setError("Password must be at least 6 characters long.");
        return;
      }
      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }

      setLoading(true);
      try {
        const res = await authService.register({
          name: name.trim(),
          email: email.trim(),
          password,
        });
        onLoginSuccess(res.user);
      } catch (err: any) {
        setError(err.message || "Failed to create account.");
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(true);
      try {
        const res = await authService.login({
          email: email.trim(),
          password,
        });
        onLoginSuccess(res.user);
      } catch (err: any) {
        setError(err.message || "Invalid email or password.");
      } finally {
        setLoading(false);
      }
    }
  };

  const handleQuickDemo = async (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError(null);
    setLoading(true);
    try {
      const res = await authService.login({ email: demoEmail, password: demoPass });
      onLoginSuccess(res.user);
    } catch (err: any) {
      setError(err.message || "Failed to log in with demo account.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      {/* Top Navbar Brand */}
      <header className="navbar">
        <div className="navbar-container">
          <div className="navbar-brand">
            <div className="brand-icon">🎓</div>
            <div>
              <div className="brand-title-wrap">
                <h1 className="brand-title">OpportunityHub</h1>
                <span className="brand-badge">Authentication Required</span>
              </div>
              <p className="brand-subtitle">Student Internship & Job Opportunity Platform</p>
            </div>
          </div>
        </div>
      </header>

      {/* Centered Login Card */}
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <div className="auth-icon-wrap">
              {isSignup ? "📝" : "🔐"}
            </div>
            <h2 className="auth-title">
              {isSignup ? "Create an Account" : "Welcome Back"}
            </h2>
            <p className="auth-subtitle">
              {isSignup
                ? "Sign up to post and manage student internships"
                : "Sign in with your email and password to enter the dashboard"}
            </p>
          </div>

          {error && (
            <div className="form-alert-error" style={{ margin: "0 0 1rem 0" }}>
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            {isSignup && (
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Afrin Sultana"
                  className="search-input"
                  style={{ padding: "0.65rem 0.85rem" }}
                />
              </div>
            )}

            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="e.g. student@university.edu"
                className="search-input"
                style={{ padding: "0.65rem 0.85rem" }}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="search-input"
                style={{ padding: "0.65rem 0.85rem" }}
              />
            </div>

            {isSignup && (
              <div className="form-group">
                <label className="form-label">Confirm Password</label>
                <input
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Re-enter password"
                  className="search-input"
                  style={{ padding: "0.65rem 0.85rem" }}
                />
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ width: "100%", padding: "0.75rem", marginTop: "0.5rem" }}
            >
              {loading
                ? isSignup
                  ? "Creating Account..."
                  : "Signing In..."
                : isSignup
                ? "Sign Up & Open Dashboard"
                : "Sign In to Dashboard"}
            </button>
          </form>

          {/* Quick Demo Logins for Teachers / Evaluators */}
          {!isSignup && (
            <div className="demo-credentials-box">
              <div className="demo-credentials-title">⚡ Quick Demo One-Click Access</div>
              <div className="demo-btns-grid" style={{ gridTemplateColumns: "1fr 1fr 1fr", gap: "0.4rem" }}>
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => handleQuickDemo("admin@platform.com", "password123")}
                  className="btn btn-secondary btn-sm"
                  title="Log in as Main Admin (Admin Manager)"
                  style={{ fontSize: "0.74rem", padding: "0.35rem 0.4rem", whiteSpace: "nowrap" }}
                >
                  👑 Admin Manager
                </button>
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => handleQuickDemo("admin2@platform.com", "password123")}
                  className="btn btn-secondary btn-sm"
                  title="Log in as Security Officer"
                  style={{ fontSize: "0.74rem", padding: "0.35rem 0.4rem", whiteSpace: "nowrap" }}
                >
                  🛡️ Security Officer
                </button>
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => handleQuickDemo("student@university.edu", "password123")}
                  className="btn btn-secondary btn-sm"
                  title="Log in as Student"
                  style={{ fontSize: "0.74rem", padding: "0.35rem 0.4rem", whiteSpace: "nowrap" }}
                >
                  🎓 Student Demo
                </button>
              </div>
            </div>
          )}

          <div className="auth-footer">
            {isSignup ? (
              <span>
                Already have an account?{" "}
                <button
                  type="button"
                  className="auth-link"
                  onClick={() => {
                    setIsSignup(false);
                    setError(null);
                  }}
                >
                  Sign In
                </button>
              </span>
            ) : (
              <span>
                Don't have an account yet?{" "}
                <button
                  type="button"
                  className="auth-link"
                  onClick={() => {
                    setIsSignup(true);
                    setError(null);
                  }}
                >
                  Create Account
                </button>
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
