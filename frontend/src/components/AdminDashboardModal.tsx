import React, { useState, useEffect } from "react";
import { User } from "../types/auth";
import { AdminOverviewStats, AuditLogItem } from "../types/admin";
import {
  fetchAdminOverview,
  fetchAllUsers,
  toggleUserBan,
  toggleUserRole,
  fetchAuditLogs,
} from "../services/api";
import { getAccessToken } from "../services/auth";

interface AdminDashboardModalProps {
  currentUser: User;
  isOpen: boolean;
  onClose: () => void;
}

export const AdminDashboardModal: React.FC<AdminDashboardModalProps> = ({
  currentUser,
  isOpen,
  onClose,
}) => {
  const [activeTab, setActiveTab] = useState<"overview" | "users" | "logs" | "export">("overview");
  const [overview, setOverview] = useState<AdminOverviewStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [userSearch, setUserSearch] = useState("");

  useEffect(() => {
    if (isOpen) {
      loadTabData(activeTab);
    } else {
      setError(null);
      setSuccessMsg(null);
    }
  }, [isOpen, activeTab]);

  const loadTabData = async (tab: string) => {
    try {
      setLoading(true);
      setError(null);

      if (tab === "overview") {
        const stats = await fetchAdminOverview();
        setOverview(stats);
      } else if (tab === "users") {
        const userList = await fetchAllUsers();
        setUsers(userList);
      } else if (tab === "logs") {
        const auditLogs = await fetchAuditLogs(100);
        setLogs(auditLogs);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load admin data");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleBan = async (user: User) => {
    if (user.id === currentUser.id) {
      alert("You cannot ban your own administrator account.");
      return;
    }
    if (user.email === "admin@platform.com" || user.is_main_admin) {
      alert("The Main Admin (Admin Manager) is permanently protected and cannot be banned.");
      return;
    }
    const actionName = user.is_banned ? "unban" : "ban";
    if (!confirm(`Are you sure you want to ${actionName} user "${user.email}"?`)) return;

    try {
      setActionLoading(true);
      setError(null);
      const updated = await toggleUserBan(user.id);
      setSuccessMsg(`User ${updated.email} is now ${updated.is_banned ? "BANNED" : "ACTIVE"}.`);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
    } catch (err: any) {
      setError(err.message || "Failed to change user ban status");
    } finally {
      setActionLoading(false);
    }
  };

  const handleToggleRole = async (user: User) => {
    if (user.id === currentUser.id) {
      alert("You cannot demote your own administrator account.");
      return;
    }
    if (user.email === "admin@platform.com" || user.is_main_admin) {
      alert("The Main Admin (Admin Manager) role is permanently protected and cannot be modified.");
      return;
    }
    const targetRole = user.role === "admin" ? "student" : "admin";
    if (!confirm(`Are you sure you want to change "${user.email}" role to ${targetRole.toUpperCase()}?`)) return;

    try {
      setActionLoading(true);
      setError(null);
      const updated = await toggleUserRole(user.id);
      setSuccessMsg(`User ${updated.email} role changed to ${updated.role.toUpperCase()}.`);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
    } catch (err: any) {
      setError(err.message || "Failed to change user role");
    } finally {
      setActionLoading(false);
    }
  };

  const handleDownloadCsv = (dataType: "opportunities" | "users") => {
    const token = getAccessToken();
    const url = `/api/admin/export/csv?data_type=${dataType}&token=${encodeURIComponent(token || "")}`;
    window.open(url, "_blank");
  };

  if (!isOpen) return null;

  const filteredUsers = users.filter(
    (u) =>
      u.name.toLowerCase().includes(userSearch.toLowerCase()) ||
      u.email.toLowerCase().includes(userSearch.toLowerCase()) ||
      u.role.toLowerCase().includes(userSearch.toLowerCase())
  );

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-container modal-lg"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        style={{ maxWidth: "960px" }}
      >
        <div className="modal-header">
          <div>
            <div className="modal-badges">
              <span className="badge badge-indigo">🛡️ Part 5: Admin Command Center</span>
              <span className="badge badge-neutral">Security & Governance</span>
            </div>
            <h2 className="modal-title">Admin Command Center</h2>
            <p className="modal-subtitle">
              Manage platform users, inspect real-time security audit trails, and export data.
            </p>
          </div>
          <button className="modal-close-btn" onClick={onClose} aria-label="Close">
            ✕
          </button>
        </div>

        <div className="modal-body">
          {error && (
            <div className="form-alert-error" style={{ marginBottom: "1rem" }}>
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}
          {successMsg && (
            <div className="form-alert-success" style={{ marginBottom: "1rem" }}>
              <span>✅</span>
              <span>{successMsg}</span>
            </div>
          )}

          {/* Tab Navigation */}
          <div className="status-tabs" style={{ marginBottom: "1.25rem" }}>
            <button
              type="button"
              className={`tab-btn ${activeTab === "overview" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("overview")}
            >
              📊 System Overview
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === "users" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("users")}
            >
              👥 User Management
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === "logs" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("logs")}
            >
              📜 Audit Trail
            </button>
            <button
              type="button"
              className={`tab-btn ${activeTab === "export" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("export")}
            >
              📥 CSV Export
            </button>
          </div>

          {/* TAB 1: OVERVIEW */}
          {activeTab === "overview" && (
            <div>
              {loading || !overview ? (
                <div style={{ textAlign: "center", padding: "2rem", color: "var(--text-muted)" }}>
                  <div className="loading-spinner" style={{ margin: "0 auto 0.75rem auto" }}></div>
                  Loading system statistics...
                </div>
              ) : (
                <>
                  <div className="admin-stats-grid">
                    <div className="admin-stat-card">
                      <span className="admin-stat-label">Total Users</span>
                      <span className="admin-stat-val">{overview.total_users}</span>
                      <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                        {overview.admin_users} Admins | {overview.total_users - overview.admin_users} Students
                      </span>
                    </div>

                    <div className="admin-stat-card">
                      <span className="admin-stat-label">Banned Users</span>
                      <span className="admin-stat-val" style={{ color: "var(--danger)" }}>
                        {overview.banned_users}
                      </span>
                      <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                        Access restricted
                      </span>
                    </div>

                    <div className="admin-stat-card">
                      <span className="admin-stat-label">Total Opportunities</span>
                      <span className="admin-stat-val" style={{ color: "var(--success)" }}>
                        {overview.total_opportunities}
                      </span>
                      <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                        {overview.open_opportunities} currently open
                      </span>
                    </div>

                    <div className="admin-stat-card">
                      <span className="admin-stat-label">Shared Groups</span>
                      <span className="admin-stat-val">{overview.total_groups}</span>
                      <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                        Collaboration pods
                      </span>
                    </div>

                    <div className="admin-stat-card">
                      <span className="admin-stat-label">Audit Events Logged</span>
                      <span className="admin-stat-val">{overview.total_audit_logs}</span>
                      <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                        Real-time security trail
                      </span>
                    </div>
                  </div>

                  <div style={{ background: "var(--bg-page)", padding: "1.25rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-subtle)" }}>
                    <h4 style={{ fontWeight: 700, fontSize: "0.95rem", color: "var(--text-main)", marginBottom: "0.5rem" }}>
                      🛡️ Platform Security & Governance Status
                    </h4>
                    <p style={{ fontSize: "0.85rem", color: "var(--text-muted)", lineHeight: 1.5 }}>
                      JWT Bearer token authentication is actively enforced. Password hashing uses salt-strengthened bcrypt.
                      Role-based access control (RBAC) ensures students can only edit or delete their own opportunities, while admins maintain platform-wide moderation authority.
                    </p>
                  </div>
                </>
              )}
            </div>
          )}

          {/* TAB 2: USER MANAGEMENT */}
          {activeTab === "users" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
                <input
                  type="text"
                  placeholder="🔍 Search users by name, email, or role..."
                  value={userSearch}
                  onChange={(e) => setUserSearch(e.target.value)}
                  className="search-input"
                  style={{ maxWidth: "340px", padding: "0.5rem 0.8rem", fontSize: "0.85rem" }}
                />
                <span style={{ fontSize: "0.82rem", color: "var(--text-muted)" }}>
                  Showing {filteredUsers.length} of {users.length} users
                </span>
              </div>

              <div className="table-responsive">
                <table className="hub-table">
                  <thead>
                    <tr>
                      <th>User</th>
                      <th>Role</th>
                      <th>Status</th>
                      <th>Joined</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredUsers.map((u) => {
                      const isSelf = u.id === currentUser.id;
                      const isTargetMainAdmin = u.email === "admin@platform.com" || Boolean(u.is_main_admin);
                      const isCurrentMainAdmin = currentUser.email === "admin@platform.com" || Boolean(currentUser.is_main_admin);
                      const isTargetSecurityOfficer = u.email === "admin2@platform.com" || u.name.toLowerCase().includes("security") || u.role === "security_officer";

                      return (
                        <tr key={u.id}>
                          <td>
                            <strong>{u.name}</strong> {isSelf && <span style={{ fontSize: "0.72rem", color: "var(--primary)" }}>(You)</span>}
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                              {u.email}
                            </div>
                          </td>
                          <td>
                            {isTargetMainAdmin ? (
                              <span
                                className="badge badge-indigo"
                                style={{ fontWeight: 700, background: "#eef2ff", color: "#4338ca", borderColor: "#c7d2fe" }}
                              >
                                👑 MAIN ADMIN
                              </span>
                            ) : isTargetSecurityOfficer ? (
                              <span
                                className="badge badge-indigo"
                                style={{ fontWeight: 700, background: "#f0f9ff", color: "#0284c7", borderColor: "#bae6fd" }}
                              >
                                🛡️ SECURITY OFFICER
                              </span>
                            ) : (
                              <span className="badge badge-neutral">
                                {u.role === "admin" ? "ADMIN" : "STUDENT"}
                              </span>
                            )}
                          </td>
                          <td>
                            <span className={`badge ${u.is_banned ? "badge-danger" : "badge-success"}`}>
                              <span className="badge-dot"></span>
                              {u.is_banned ? "Banned" : "Active"}
                            </span>
                          </td>
                          <td>{u.created_at?.split(" ")[0] || "Active"}</td>
                          <td>
                            {isSelf ? (
                              <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontStyle: "italic" }}>
                                Active Session
                              </span>
                            ) : isTargetMainAdmin ? (
                              <span
                                className="badge badge-indigo"
                                style={{ fontSize: "0.75rem", padding: "0.25rem 0.6rem", background: "#eef2ff", color: "#4338ca", borderColor: "#c7d2fe" }}
                                title="The Main Admin (Admin Manager) is permanently protected from demotions and bans"
                              >
                                🔒 Protected (Main Admin)
                              </span>
                            ) : isTargetSecurityOfficer && !isCurrentMainAdmin ? (
                              <span className="badge badge-neutral" style={{ fontSize: "0.75rem", padding: "0.25rem 0.6rem" }}>
                                🔒 Protected
                              </span>
                            ) : (
                              <div style={{ display: "flex", gap: "0.35rem" }}>
                                <button
                                  className="btn btn-secondary btn-sm"
                                  style={{ padding: "0.25rem 0.5rem", fontSize: "0.75rem" }}
                                  disabled={actionLoading}
                                  onClick={() => handleToggleRole(u)}
                                  title={`Switch role to ${u.role === "admin" ? "Student" : "Admin"}`}
                                >
                                  {u.role === "admin" ? "Demote" : "Promote"}
                                </button>
                                <button
                                  className={`btn btn-sm ${u.is_banned ? "btn-outline" : "btn-danger-outline"}`}
                                  style={{ padding: "0.25rem 0.5rem", fontSize: "0.75rem" }}
                                  disabled={actionLoading}
                                  onClick={() => handleToggleBan(u)}
                                  title={u.is_banned ? "Unban user" : "Ban user from logging in"}
                                >
                                  {u.is_banned ? "Unban" : "Ban"}
                                </button>
                              </div>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 3: AUDIT TRAIL */}
          {activeTab === "logs" && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                  Showing last {logs.length} security audit events (newest first)
                </span>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => loadTabData("logs")}
                  disabled={loading}
                >
                  🔄 Refresh Logs
                </button>
              </div>

              <div className="table-responsive" style={{ maxHeight: "400px", overflowY: "auto" }}>
                <table className="hub-table">
                  <thead>
                    <tr>
                      <th>Timestamp</th>
                      <th>Action</th>
                      <th>User</th>
                      <th>Details</th>
                      <th>IP</th>
                    </tr>
                  </thead>
                  <tbody>
                    {logs.length > 0 ? (
                      logs.map((log) => (
                        <tr key={log.id}>
                          <td style={{ whiteSpace: "nowrap", fontSize: "0.78rem" }}>
                            {log.timestamp}
                          </td>
                          <td>
                            <span className="badge badge-neutral" style={{ fontWeight: 700, fontSize: "0.72rem" }}>
                              {log.action}
                            </span>
                          </td>
                          <td style={{ fontSize: "0.82rem" }}>
                            {log.user_email || log.user_id || "System"}
                          </td>
                          <td style={{ fontSize: "0.82rem", maxWidth: "260px", wordBreak: "break-word" }}>
                            {log.details}
                          </td>
                          <td style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                            <code>{log.ip_address}</code>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={5} style={{ textAlign: "center", padding: "1.5rem", color: "var(--text-muted)" }}>
                          No audit events recorded yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 4: CSV EXPORT */}
          {activeTab === "export" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
              <div style={{ background: "var(--bg-page)", padding: "1.25rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-subtle)" }}>
                <h4 style={{ fontWeight: 700, fontSize: "1rem", color: "var(--text-main)", marginBottom: "0.25rem" }}>
                  📊 Export Internship Opportunities
                </h4>
                <p style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginBottom: "1rem" }}>
                  Download a full CSV spreadsheet containing all opportunities, company names, locations, salaries, deadlines, and statuses.
                </p>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => handleDownloadCsv("opportunities")}
                >
                  📥 Download Opportunities CSV
                </button>
              </div>

              <div style={{ background: "var(--bg-page)", padding: "1.25rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-subtle)" }}>
                <h4 style={{ fontWeight: 700, fontSize: "1rem", color: "var(--text-main)", marginBottom: "0.25rem" }}>
                  👥 Export User Directory
                </h4>
                <p style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginBottom: "1rem" }}>
                  Download a full CSV of all registered users with their name, email, role, and active status.
                </p>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => handleDownloadCsv("users")}
                >
                  📥 Download Users Directory CSV
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
