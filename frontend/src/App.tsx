import { useEffect, useState, useMemo, useCallback } from "react";
import { User } from "./types/auth";
import * as authService from "./services/auth";
import { LoginPage } from "./components/LoginPage";
import {
  Internship,
  InternshipCreateInput,
  InternshipUpdateInput,
  InternshipStats,
} from "./types/internship";
import {
  fetchInternships,
  createInternship,
  updateInternship,
  deleteInternship,
  fetchStats,
  checkBackendHealth,
} from "./services/api";
import { Navbar } from "./components/Navbar";
import { StatsCards } from "./components/StatsCards";
import { FilterBar } from "./components/FilterBar";
import { InternshipCard } from "./components/InternshipCard";
import { InternshipDetailModal } from "./components/InternshipDetailModal";
import { InternshipFormModal } from "./components/InternshipFormModal";
import { DeleteConfirmModal } from "./components/DeleteConfirmModal";
import { Toast, ToastMessage } from "./components/Toast";
import { GroupManagementModal } from "./components/GroupManagementModal";
import { AdminDashboardModal } from "./components/AdminDashboardModal";

export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(() => authService.getStoredUser());
  const [internships, setInternships] = useState<Internship[]>([]);
  const [stats, setStats] = useState<InternshipStats>({
    total: 0,
    open: 0,
    closed: 0,
    remote: 0,
  });
  const [loading, setLoading] = useState(true);
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  // Filters & Sorting
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortBy, setSortBy] = useState("newest");
  const [myOnly, setMyOnly] = useState(false);
  const [activeGroupId, setActiveGroupId] = useState<string | undefined>(undefined);
  const [activeGroupName, setActiveGroupName] = useState<string | undefined>(undefined);

  // Modals state
  const [selectedDetail, setSelectedDetail] = useState<Internship | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingInternship, setEditingInternship] = useState<Internship | null>(
    null
  );
  const [deleteTarget, setDeleteTarget] = useState<Internship | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isGroupModalOpen, setIsGroupModalOpen] = useState(false);
  const [isAdminModalOpen, setIsAdminModalOpen] = useState(false);

  // Notifications
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = (
    type: "success" | "error" | "info",
    message: string,
    method?: "POST" | "PUT" | "DELETE" | "GET"
  ) => {
    const newToast: ToastMessage = {
      id: crypto.randomUUID(),
      type,
      message,
      method,
    };
    setToasts((prev) => [...prev, newToast]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  // Load data function
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const isOnline = await checkBackendHealth();
      setIsBackendConnected(isOnline);

      const [internshipsRes, statsRes] = await Promise.all([
        fetchInternships(search, statusFilter, myOnly, activeGroupId),
        fetchStats(),
      ]);

      const items = internshipsRes.data;
      setInternships(items);

      // Keep dashboard stats counter cards 100% in sync with the opportunities data
      if (!search.trim() && statusFilter === "All" && !myOnly && !activeGroupId) {
        setStats({
          total: items.length,
          open: items.filter((i) => i.status.toLowerCase() === "open").length,
          closed: items.filter((i) => i.status.toLowerCase() === "closed").length,
          remote: items.filter((i) => i.location.toLowerCase().includes("remote")).length,
        });
      } else {
        setStats(statsRes);
      }
    } catch (err) {
      console.error("Error loading data:", err);
      addToast("error", "Failed to load internship opportunities.");
    } finally {
      setLoading(false);
    }
  }, [search, statusFilter, myOnly, activeGroupId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // CREATE (C in CRUD)
  async function handleCreate(payload: InternshipCreateInput) {
    try {
      const res = await createInternship(payload);
      addToast(
        "success",
        `Internship "${res.data.title}" posted successfully.`,
        "POST"
      );
      await loadData();
    } catch (err) {
      addToast(
        "error",
        err instanceof Error ? err.message : "Failed to create internship"
      );
      throw err;
    }
  }

  // UPDATE (U in CRUD)
  async function handleUpdate(id: string, payload: InternshipUpdateInput) {
    try {
      const res = await updateInternship(id, payload);
      addToast(
        "success",
        `Internship "${res.data.title}" updated successfully.`,
        "PUT"
      );
      await loadData();
      if (selectedDetail && selectedDetail.id === id) {
        setSelectedDetail(res.data);
      }
    } catch (err) {
      addToast(
        "error",
        err instanceof Error ? err.message : "Failed to update internship"
      );
      throw err;
    }
  }

  // DELETE (D in CRUD)
  async function handleConfirmDelete(id: string) {
    try {
      setIsDeleting(true);
      await deleteInternship(id);
      addToast(
        "success",
        "Internship opportunity deleted successfully.",
        "DELETE"
      );
      setDeleteTarget(null);
      if (selectedDetail && selectedDetail.id === id) {
        setSelectedDetail(null);
      }
      await loadData();
    } catch (err) {
      addToast(
        "error",
        err instanceof Error ? err.message : "Failed to delete internship"
      );
    } finally {
      setIsDeleting(false);
    }
  }

  // Sorted list
  const sortedInternships = useMemo(() => {
    const list = [...internships];
    if (sortBy === "title") {
      return list.sort((a, b) => a.title.localeCompare(b.title));
    }
    if (sortBy === "company") {
      return list.sort((a, b) => a.company_name.localeCompare(b.company_name));
    }
    if (sortBy === "deadline") {
      return list.sort((a, b) => a.deadline.localeCompare(b.deadline));
    }
    // default newest
    return list.sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
  }, [internships, sortBy]);

  // Require login before viewing the dashboard
  if (!currentUser) {
    return <LoginPage onLoginSuccess={(user) => setCurrentUser(user)} />;
  }

  return (
    <div className="app-shell">
      <Navbar
        onOpenCreate={() => {
          setEditingInternship(null);
          setIsFormOpen(true);
        }}
        isBackendConnected={isBackendConnected}
        onRefresh={loadData}
        currentUser={currentUser}
        onLogout={() => {
          authService.logout();
          setCurrentUser(null);
        }}
        onOpenGroups={() => setIsGroupModalOpen(true)}
        onOpenAdmin={() => setIsAdminModalOpen(true)}
      />

      <main className="main-content">
        <div className="page-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <h2 className="page-title">Internship Opportunity Manager</h2>
            <p className="page-subtitle">
              Manage student job listings, internships, requirements, and deadlines.
            </p>
          </div>

          <div style={{ display: "flex", gap: "0.5rem", alignItems: "center", flexWrap: "wrap" }}>
            <div className="status-tabs">
              <button
                type="button"
                className={`tab-btn ${!myOnly && !activeGroupId ? "tab-active" : ""}`}
                onClick={() => {
                  setMyOnly(false);
                  setActiveGroupId(undefined);
                  setActiveGroupName(undefined);
                }}
              >
                🌐 All Opportunities
              </button>
              <button
                type="button"
                className={`tab-btn ${myOnly ? "tab-active" : ""}`}
                onClick={() => {
                  setMyOnly(true);
                  setActiveGroupId(undefined);
                  setActiveGroupName(undefined);
                }}
              >
                👤 My Postings
              </button>
            </div>

            {activeGroupId && (
              <span className="badge badge-indigo" style={{ padding: "0.35rem 0.65rem", fontSize: "0.8rem", display: "inline-flex", alignItems: "center", gap: "0.4rem" }}>
                <span>👥 Group: {activeGroupName || "Selected"}</span>
                <button
                  type="button"
                  style={{ background: "none", border: "none", cursor: "pointer", color: "inherit", fontWeight: 700, padding: 0 }}
                  onClick={() => {
                    setActiveGroupId(undefined);
                    setActiveGroupName(undefined);
                  }}
                  title="Clear group filter"
                >
                  ✕
                </button>
              </span>
            )}
          </div>
        </div>

        {/* Aggregate Stats (Read Aggregation) */}
        <StatsCards
          stats={stats}
          onFilterStatus={(status) => setStatusFilter(status)}
          activeStatus={statusFilter}
        />

        {/* Search, Filter & Sort Bar */}
        <FilterBar
          search={search}
          onSearchChange={setSearch}
          statusFilter={statusFilter}
          onStatusChange={setStatusFilter}
          sortBy={sortBy}
          onSortChange={setSortBy}
          totalResults={sortedInternships.length}
        />

        {/* Content Listing (Read List) */}
        {loading ? (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading internship opportunities...</p>
          </div>
        ) : sortedInternships.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📂</div>
            <h3>No Internship Opportunities Found</h3>
            <p>
              {search
                ? `No results matching "${search}". Try adjusting your keywords.`
                : "No internships match the selected filter."}
            </p>
            <div className="empty-actions">
              {search && (
                <button
                  className="btn btn-secondary"
                  onClick={() => setSearch("")}
                >
                  Clear Search
                </button>
              )}
              <button
                className="btn btn-primary"
                onClick={() => {
                  setEditingInternship(null);
                  setIsFormOpen(true);
                }}
              >
                + Post New Internship
              </button>
            </div>
          </div>
        ) : (
          <div className="cards-grid">
            {sortedInternships.map((internship) => (
              <InternshipCard
                key={internship.id}
                internship={internship}
                currentUser={currentUser}
                onViewDetails={(item) => setSelectedDetail(item)}
                onEdit={(item) => {
                  setEditingInternship(item);
                  setIsFormOpen(true);
                }}
                onDelete={(item) => setDeleteTarget(item)}
              />
            ))}
          </div>
        )}

      </main>

      {/* MODALS */}
      <InternshipDetailModal
        internship={selectedDetail}
        currentUser={currentUser}
        onClose={() => setSelectedDetail(null)}
        onEdit={(item) => {
          setEditingInternship(item);
          setIsFormOpen(true);
        }}
        onDelete={(item) => setDeleteTarget(item)}
      />

      <InternshipFormModal
        isOpen={isFormOpen}
        onClose={() => {
          setIsFormOpen(false);
          setEditingInternship(null);
        }}
        onSubmitCreate={handleCreate}
        onSubmitUpdate={handleUpdate}
        editingInternship={editingInternship}
      />

      <DeleteConfirmModal
        internship={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleConfirmDelete}
        isDeleting={isDeleting}
      />

      {/* Part 4: Study Groups Modal */}
      <GroupManagementModal
        currentUser={currentUser}
        isOpen={isGroupModalOpen}
        onClose={() => setIsGroupModalOpen(false)}
        activeGroupId={activeGroupId}
        onSelectGroupFilter={(groupId, groupName) => {
          setActiveGroupId(groupId);
          setActiveGroupName(groupName);
          setMyOnly(false);
        }}
      />

      {/* Part 5: Admin Command Center Modal (Admin Manager & Security Officer) */}
      {(currentUser.role === "admin" || currentUser.role === "security_officer" || currentUser.is_main_admin || currentUser.email === "admin2@platform.com") && (
        <AdminDashboardModal
          currentUser={currentUser}
          isOpen={isAdminModalOpen}
          onClose={() => setIsAdminModalOpen(false)}
        />
      )}

      {/* TOAST ALERTS */}
      <Toast toasts={toasts} onDismiss={removeToast} />
    </div>
  );
}
