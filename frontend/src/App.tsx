import { useEffect, useState, useMemo, useCallback } from "react";
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

export default function App() {
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

  // Modals state
  const [selectedDetail, setSelectedDetail] = useState<Internship | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingInternship, setEditingInternship] = useState<Internship | null>(
    null
  );
  const [deleteTarget, setDeleteTarget] = useState<Internship | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

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
        fetchInternships(search, statusFilter),
        fetchStats(),
      ]);

      const items = internshipsRes.data;
      setInternships(items);

      // Keep dashboard stats counter cards 100% in sync with the opportunities data
      if (!search.trim() && statusFilter === "All") {
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
  }, [search, statusFilter]);

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

  return (
    <div className="app-shell">
      <Navbar
        onOpenCreate={() => {
          setEditingInternship(null);
          setIsFormOpen(true);
        }}
        isBackendConnected={isBackendConnected}
        onRefresh={loadData}
      />

      <main className="main-content">
        <div className="page-header">
          <div>
            <h2 className="page-title">Internship Opportunity Manager</h2>
            <p className="page-subtitle">
              Manage student job listings, internships, requirements, and deadlines.
            </p>
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

      {/* TOAST ALERTS */}
      <Toast toasts={toasts} onDismiss={removeToast} />
    </div>
  );
}
