import React, { useState, useEffect } from "react";
import { User } from "../types/auth";
import { GroupRead, GroupMemberRead } from "../types/group";
import {
  fetchGroups,
  createGroup,
  fetchGroupDetails,
  addGroupMember,
  removeGroupMember,
  deleteGroup,
} from "../services/api";

interface GroupManagementModalProps {
  currentUser: User;
  isOpen: boolean;
  onClose: () => void;
  onSelectGroupFilter?: (groupId: string | undefined, groupName?: string) => void;
  activeGroupId?: string;
}

export const GroupManagementModal: React.FC<GroupManagementModalProps> = ({
  currentUser,
  isOpen,
  onClose,
  onSelectGroupFilter,
  activeGroupId,
}) => {
  const [groups, setGroups] = useState<GroupRead[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<GroupRead | null>(null);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Create group form
  const [isCreating, setIsCreating] = useState(false);
  const [newGroupName, setNewGroupName] = useState("");
  const [newGroupDesc, setNewGroupDesc] = useState("");

  // Add member form
  const [newMemberEmail, setNewMemberEmail] = useState("");
  const [canCreate, setCanCreate] = useState(true);
  const [canEdit, setCanEdit] = useState(false);
  const [canAssign, setCanAssign] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadGroups();
    } else {
      setSelectedGroup(null);
      setIsCreating(false);
      setError(null);
      setSuccessMsg(null);
    }
  }, [isOpen]);

  const loadGroups = async () => {
    try {
      setLoading(true);
      setError(null);
      const list = await fetchGroups();
      setGroups(list);
      if (selectedGroup) {
        const updated = list.find((g) => g.id === selectedGroup.id);
        if (updated) setSelectedGroup(updated);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load groups");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectGroup = async (group: GroupRead) => {
    try {
      setActionLoading(true);
      setError(null);
      const details = await fetchGroupDetails(group.id);
      setSelectedGroup(details);
    } catch (err: any) {
      setError(err.message || "Failed to load group details");
    } finally {
      setActionLoading(false);
    }
  };

  const handleCreateGroup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newGroupName.trim()) return;

    try {
      setActionLoading(true);
      setError(null);
      const created = await createGroup({
        name: newGroupName.trim(),
        description: newGroupDesc.trim(),
      });
      setSuccessMsg(`Group "${created.name}" created successfully!`);
      setNewGroupName("");
      setNewGroupDesc("");
      setIsCreating(false);
      await loadGroups();
      setSelectedGroup(created);
    } catch (err: any) {
      setError(err.message || "Failed to create group");
    } finally {
      setActionLoading(false);
    }
  };

  const handleAddMember = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedGroup || !newMemberEmail.trim()) return;

    try {
      setActionLoading(true);
      setError(null);
      await addGroupMember(selectedGroup.id, {
        email: newMemberEmail.trim(),
        can_create: canCreate,
        can_edit: canEdit,
        can_assign: canAssign,
      });
      setSuccessMsg(`User ${newMemberEmail} added to group!`);
      setNewMemberEmail("");
      // Refresh selected group
      const refreshed = await fetchGroupDetails(selectedGroup.id);
      setSelectedGroup(refreshed);
      await loadGroups();
    } catch (err: any) {
      setError(err.message || "Failed to add member to group");
    } finally {
      setActionLoading(false);
    }
  };

  const handleRemoveMember = async (memberId: string, memberName: string) => {
    if (!selectedGroup) return;
    if (!confirm(`Are you sure you want to remove ${memberName} from this group?`)) return;

    try {
      setActionLoading(true);
      setError(null);
      await removeGroupMember(selectedGroup.id, memberId);
      setSuccessMsg(`Removed ${memberName} from group.`);
      const refreshed = await fetchGroupDetails(selectedGroup.id);
      setSelectedGroup(refreshed);
      await loadGroups();
    } catch (err: any) {
      setError(err.message || "Failed to remove member");
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteGroup = async (groupId: string, groupName: string) => {
    if (!confirm(`Are you sure you want to permanently delete the group "${groupName}"?`)) return;

    try {
      setActionLoading(true);
      setError(null);
      await deleteGroup(groupId);
      setSuccessMsg(`Group "${groupName}" deleted.`);
      setSelectedGroup(null);
      if (activeGroupId === groupId && onSelectGroupFilter) {
        onSelectGroupFilter(undefined);
      }
      await loadGroups();
    } catch (err: any) {
      setError(err.message || "Failed to delete group");
    } finally {
      setActionLoading(false);
    }
  };

  if (!isOpen) return null;

  const isOwner = selectedGroup?.owner_id === currentUser.id || currentUser.role === "admin";

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-container modal-lg"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        style={{ maxWidth: "880px" }}
      >
        <div className="modal-header">
          <div>
            <div className="modal-badges">
              <span className="badge badge-indigo">👥 Part 4: Shared Groups</span>
              {selectedGroup && (
                <span className="badge badge-neutral">{selectedGroup.name}</span>
              )}
            </div>
            <h2 className="modal-title">Study Groups & Collaboration Hub</h2>
            <p className="modal-subtitle">
              Collaborate with classmates, share opportunities, and manage group permissions.
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

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
            <div className="status-tabs">
              <button
                type="button"
                className={`tab-btn ${!selectedGroup && !isCreating ? "tab-active" : ""}`}
                onClick={() => {
                  setSelectedGroup(null);
                  setIsCreating(false);
                }}
              >
                All Groups ({groups.length})
              </button>
              {selectedGroup && (
                <button
                  type="button"
                  className="tab-btn tab-active"
                  onClick={() => setIsCreating(false)}
                >
                  📍 {selectedGroup.name}
                </button>
              )}
            </div>

            <button
              className="btn btn-primary btn-sm"
              onClick={() => {
                setIsCreating(!isCreating);
                setSelectedGroup(null);
              }}
            >
              {isCreating ? "✕ Cancel" : "+ Create New Group"}
            </button>
          </div>

          {/* VIEW 1: CREATE GROUP FORM */}
          {isCreating && (
            <form onSubmit={handleCreateGroup} style={{ background: "var(--bg-page)", padding: "1.25rem", borderRadius: "var(--radius-md)", border: "1px solid var(--border-subtle)" }}>
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "0.75rem", color: "var(--text-main)" }}>
                Create a Study or Career Group
              </h3>
              <div className="form-group">
                <label className="form-label">Group Name *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. AI & Data Science Seekers"
                  value={newGroupName}
                  onChange={(e) => setNewGroupName(e.target.value)}
                  className="search-input"
                  style={{ padding: "0.6rem 0.8rem" }}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  rows={3}
                  placeholder="Describe your group's focus, goals, or meeting frequency..."
                  value={newGroupDesc}
                  onChange={(e) => setNewGroupDesc(e.target.value)}
                  className="search-input"
                  style={{ padding: "0.6rem 0.8rem", width: "100%", resize: "vertical" }}
                />
              </div>
              <div style={{ display: "flex", gap: "0.5rem", justifyContent: "flex-end" }}>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() => setIsCreating(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={actionLoading}
                  className="btn btn-primary btn-sm"
                >
                  {actionLoading ? "Creating..." : "Save & Create Group"}
                </button>
              </div>
            </form>
          )}

          {/* VIEW 2: GROUP DETAILS & MEMBERS */}
          {selectedGroup && !isCreating && (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1rem", paddingBottom: "1rem", borderBottom: "1px solid var(--border-subtle)" }}>
                <div>
                  <h3 style={{ fontSize: "1.2rem", fontWeight: 700, color: "var(--text-main)" }}>
                    {selectedGroup.name}
                  </h3>
                  <p style={{ color: "var(--text-muted)", fontSize: "0.88rem", marginTop: "0.2rem" }}>
                    {selectedGroup.description || "No description provided."}
                  </p>
                  <div style={{ display: "flex", gap: "0.75rem", marginTop: "0.5rem", fontSize: "0.8rem", color: "var(--text-muted)" }}>
                    <span>👤 Owner: <strong>{selectedGroup.owner_name || "Club Creator"}</strong></span>
                    <span>📅 Created: {selectedGroup.created_at || "Recently"}</span>
                  </div>
                </div>

                <div style={{ display: "flex", gap: "0.5rem" }}>
                  {onSelectGroupFilter && (
                    <button
                      className={`btn btn-sm ${activeGroupId === selectedGroup.id ? "btn-primary" : "btn-outline"}`}
                      onClick={() => {
                        if (activeGroupId === selectedGroup.id) {
                          onSelectGroupFilter(undefined);
                        } else {
                          onSelectGroupFilter(selectedGroup.id, selectedGroup.name);
                        }
                        onClose();
                      }}
                      title="Filter main feed opportunities by this group"
                    >
                      {activeGroupId === selectedGroup.id ? "✓ Filtering Feed" : "🔍 Filter Feed by Group"}
                    </button>
                  )}
                  {isOwner && (
                    <button
                      className="btn btn-danger-outline btn-sm"
                      onClick={() => handleDeleteGroup(selectedGroup.id, selectedGroup.name)}
                      title="Owner can delete group"
                    >
                      🗑 Delete Group
                    </button>
                  )}
                </div>
              </div>

              {/* Members List */}
              <h4 style={{ fontSize: "0.95rem", fontWeight: 700, marginBottom: "0.75rem", color: "var(--text-main)" }}>
                Group Members & Role-Based Permissions ({selectedGroup.members?.length || 0})
              </h4>
              <div className="table-responsive" style={{ marginBottom: "1.5rem" }}>
                <table className="hub-table">
                  <thead>
                    <tr>
                      <th>Member</th>
                      <th>Group Role</th>
                      <th>Can Create</th>
                      <th>Can Edit</th>
                      <th>Can Assign</th>
                      <th>Joined</th>
                      {isOwner && <th>Action</th>}
                    </tr>
                  </thead>
                  <tbody>
                    {selectedGroup.members && selectedGroup.members.length > 0 ? (
                      selectedGroup.members.map((m: GroupMemberRead) => (
                        <tr key={m.id}>
                          <td>
                            <strong>{m.name || "Member"}</strong>
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                              {m.email}
                            </div>
                          </td>
                          <td>
                            <span className={`badge ${m.is_owner ? "badge-indigo" : "badge-neutral"}`}>
                              {m.is_owner ? "OWNER" : "MEMBER"}
                            </span>
                          </td>
                          <td>{m.can_create ? "✅ Yes" : "❌ No"}</td>
                          <td>{m.can_edit ? "✅ Yes" : "❌ No"}</td>
                          <td>{m.can_assign ? "✅ Yes" : "❌ No"}</td>
                          <td>{m.joined_at?.split(" ")[0] || "Active"}</td>
                          {isOwner && (
                            <td>
                              {!m.is_owner && (
                                <button
                                  className="btn btn-danger-outline btn-sm"
                                  style={{ padding: "0.2rem 0.5rem", fontSize: "0.75rem" }}
                                  onClick={() => handleRemoveMember(m.user_id, m.name || m.email || "Member")}
                                >
                                  Remove
                                </button>
                              )}
                            </td>
                          )}
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={7} style={{ textAlign: "center", color: "var(--text-muted)", padding: "1.5rem" }}>
                          No members in this group yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Add Member Form (Owner / Admin only) */}
              {isOwner && (
                <form
                  onSubmit={handleAddMember}
                  style={{
                    background: "var(--bg-page)",
                    padding: "1rem",
                    borderRadius: "var(--radius-md)",
                    border: "1px dashed var(--border-card)",
                  }}
                >
                  <h5 style={{ fontSize: "0.85rem", fontWeight: 700, marginBottom: "0.5rem", color: "var(--text-main)" }}>
                    ➕ Add Member & Configure Group Permissions
                  </h5>
                  <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "0.75rem", alignItems: "flex-end" }}>
                    <div>
                      <label className="form-label" style={{ fontSize: "0.78rem" }}>Student Email</label>
                      <input
                        type="email"
                        required
                        placeholder="e.g. student2@university.edu"
                        value={newMemberEmail}
                        onChange={(e) => setNewMemberEmail(e.target.value)}
                        className="search-input"
                        style={{ padding: "0.45rem 0.7rem", fontSize: "0.85rem" }}
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={actionLoading}
                      className="btn btn-primary btn-sm"
                      style={{ height: "36px" }}
                    >
                      {actionLoading ? "Adding..." : "Add to Group"}
                    </button>
                  </div>

                  <div style={{ display: "flex", gap: "1.25rem", marginTop: "0.75rem", fontSize: "0.82rem" }}>
                    <label style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem", cursor: "pointer" }}>
                      <input
                        type="checkbox"
                        checked={canCreate}
                        onChange={(e) => setCanCreate(e.target.checked)}
                      />
                      <span>can_create (Post in group)</span>
                    </label>
                    <label style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem", cursor: "pointer" }}>
                      <input
                        type="checkbox"
                        checked={canEdit}
                        onChange={(e) => setCanEdit(e.target.checked)}
                      />
                      <span>can_edit (Edit group posts)</span>
                    </label>
                    <label style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem", cursor: "pointer" }}>
                      <input
                        type="checkbox"
                        checked={canAssign}
                        onChange={(e) => setCanAssign(e.target.checked)}
                      />
                      <span>can_assign (Assign candidates)</span>
                    </label>
                  </div>
                </form>
              )}
            </div>
          )}

          {/* VIEW 3: GROUPS LIST GRID */}
          {!selectedGroup && !isCreating && (
            <div>
              {loading ? (
                <div style={{ textAlign: "center", padding: "2rem", color: "var(--text-muted)" }}>
                  <div className="loading-spinner" style={{ margin: "0 auto 0.75rem auto" }}></div>
                  Loading groups...
                </div>
              ) : groups.length === 0 ? (
                <div style={{ textAlign: "center", padding: "2.5rem", background: "var(--bg-page)", borderRadius: "var(--radius-md)" }}>
                  <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>👥</div>
                  <h4 style={{ fontWeight: 700, color: "var(--text-main)", marginBottom: "0.25rem" }}>No Groups Found</h4>
                  <p style={{ color: "var(--text-muted)", fontSize: "0.88rem", marginBottom: "1rem" }}>
                    Create a group to share internship postings and collaborate with peers.
                  </p>
                  <button className="btn btn-primary btn-sm" onClick={() => setIsCreating(true)}>
                    + Create First Group
                  </button>
                </div>
              ) : (
                <div className="group-list-grid">
                  {groups.map((g) => {
                    const isUserOwner = g.owner_id === currentUser.id;
                    const isFiltering = activeGroupId === g.id;

                    return (
                      <div
                        key={g.id}
                        className={`group-item-card ${isFiltering ? "selected" : ""}`}
                        style={{ cursor: "pointer" }}
                        onClick={() => handleSelectGroup(g)}
                      >
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                          <span className={`badge ${isUserOwner ? "badge-indigo" : "badge-neutral"}`}>
                            {isUserOwner ? "👑 Owner" : "👥 Member"}
                          </span>
                          {isFiltering && (
                            <span className="badge badge-success">✓ Active Filter</span>
                          )}
                        </div>

                        <h4 style={{ fontSize: "1.05rem", fontWeight: 700, color: "var(--text-main)" }}>
                          {g.name}
                        </h4>
                        <p style={{ fontSize: "0.82rem", color: "var(--text-muted)", flex: 1, minHeight: "2.5rem" }}>
                          {g.description || "Collaborative student study group."}
                        </p>

                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "0.78rem", color: "var(--text-muted)", paddingTop: "0.5rem", borderTop: "1px solid var(--border-subtle)" }}>
                          <span>{g.members?.length || 1} members</span>
                          <span style={{ color: "var(--primary)", fontWeight: 600 }}>Manage & View →</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
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
