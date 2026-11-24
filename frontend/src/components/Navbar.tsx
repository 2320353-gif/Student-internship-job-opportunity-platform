import React from "react";
import { User } from "../types/auth";

interface NavbarProps {
  onOpenCreate: () => void;
  isBackendConnected: boolean;
  onRefresh: () => void;
  currentUser?: User | null;
  onLogout?: () => void;
  onOpenGroups?: () => void;
  onOpenAdmin?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenCreate,
  isBackendConnected,
  onRefresh,
  currentUser,
  onLogout,
  onOpenGroups,
  onOpenAdmin,
}) => {
  const isMainAdmin = Boolean(currentUser && (currentUser.email === "admin@platform.com" || currentUser.is_main_admin));
  const isSecurityOfficer = Boolean(currentUser && (currentUser.email === "admin2@platform.com" || currentUser.role === "security_officer" || currentUser.name.toLowerCase().includes("security")));
  const hasAdminAccess = Boolean(isMainAdmin || isSecurityOfficer || currentUser?.role === "admin");

  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="brand-icon">🎓</div>
          <div>
            <div className="brand-title-wrap">
              <h1 className="brand-title">OpportunityHub</h1>
              {hasAdminAccess && (
                <span className="brand-badge" style={{ background: "#eef2ff", color: "#4f46e5", borderColor: "#c7d2fe" }}>
                  {isMainAdmin ? "👑 Admin Manager Portal" : "🛡️ Security Operations"}
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
              {isMainAdmin ? (
                <span
                  className="badge badge-indigo"
                  style={{ padding: "0.15rem 0.5rem", fontSize: "0.7rem", marginLeft: "0.25rem", background: "#eef2ff", color: "#4338ca", borderColor: "#c7d2fe" }}
                >
                  👑 MAIN ADMIN
                </span>
              ) : isSecurityOfficer ? (
                <span
                  className="badge badge-indigo"
                  style={{ padding: "0.15rem 0.5rem", fontSize: "0.7rem", marginLeft: "0.25rem", background: "#f0f9ff", color: "#0284c7", borderColor: "#bae6fd" }}
                >
                  🛡️ SECURITY OFFICER
                </span>
              ) : (
                <span
                  className="badge badge-success"
                  style={{ padding: "0.15rem 0.5rem", fontSize: "0.7rem", marginLeft: "0.25rem" }}
                >
                  STUDENT
                </span>
              )}
            </div>
          )}

          {currentUser && onOpenGroups && (
            <button
              className="btn btn-secondary btn-sm"
              onClick={onOpenGroups}
              title="Collaborative Study Groups"
            >
              👥 Groups
            </button>
          )}

          {hasAdminAccess && onOpenAdmin && (
            <button
              className="btn btn-secondary btn-sm"
              onClick={onOpenAdmin}
              title="Open Admin Command Center"
              style={{ background: "#eef2ff", color: "#4f46e5", borderColor: "#c7d2fe" }}
            >
              🛡️ Admin Panel
            </button>
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
