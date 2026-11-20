import React from "react";
import { User } from "../types/auth";

interface NavbarProps {
  onOpenCreate: () => void;
  isBackendConnected: boolean;
  onRefresh: () => void;
  currentUser?: User | null;
  onLogout?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenCreate,
  isBackendConnected,
  onRefresh,
  currentUser,
  onLogout,
}) => {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="brand-icon">🎓</div>
          <div>
            <div className="brand-title-wrap">
              <h1 className="brand-title">OpportunityHub</h1>
              {currentUser?.role === "admin" && (
                <span className="brand-badge" style={{ background: "#eef2ff", color: "#4f46e5", borderColor: "#c7d2fe" }}>
                  Admin Portal
                </span>
              )}
            </div>
            <p className="brand-subtitle">
              Student Internship & Job Opportunity Platform
            </p>
          </div>
        </div>

        <div className="navbar-actions">
          {currentUser && (
            <div className="user-badge" title={`Signed in as ${currentUser.email}`}>
              <span>👤</span>
              <span>{currentUser.name}</span>
              <span
                className={`badge ${currentUser.role === "admin" ? "badge-indigo" : "badge-success"}`}
                style={{ padding: "0.15rem 0.5rem", fontSize: "0.7rem", marginLeft: "0.25rem" }}
              >
                {currentUser.role.toUpperCase()}
              </span>
            </div>
          )}

          <button
            className="btn btn-secondary btn-icon"
            onClick={onRefresh}
            title="Reload data from server"
          >
            🔄 Refresh
          </button>

          <button className="btn btn-primary" onClick={onOpenCreate}>
            <span className="btn-icon-plus">+</span> Post Internship
          </button>

          {onLogout && (
            <button
              className="btn btn-outline btn-sm"
              onClick={onLogout}
              title="Sign out of your account"
              style={{ color: "var(--danger)", borderColor: "var(--danger-border)" }}
            >
              🚪 Sign Out
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
