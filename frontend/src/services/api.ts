import {
  Internship,
  InternshipCreateInput,
  InternshipUpdateInput,
  InternshipStats,
} from "../types/internship";

const API_BASE_URL = "/api";

// Fallback seed data in case backend is offline during frontend-only preview
const FALLBACK_SEED: Internship[] = [
  {
    id: "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f60",
    title: "Frontend Developer Intern",
    company_name: "ABC Technologies",
    location: "Dhaka, Bangladesh",
    description:
      "Join our dynamic frontend engineering squad. Work with React, TypeScript, and modern CSS frameworks to build responsive, accessible web portals.",
    salary: "৳12,000 / month",
    deadline: "2026-11-28",
    status: "Open",
    created_at: "2026-11-04 10:00:00",
  },
  {
    id: "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f61",
    title: "Python & FastAPI Backend Intern",
    company_name: "XYZ Software Solutions",
    location: "Remote",
    description:
      "Assist in building high-performance asynchronous RESTful APIs with FastAPI, SQLModel, and PostgreSQL. Great learning opportunity with senior mentorship.",
    salary: "৳15,000 / month",
    deadline: "2026-11-30",
    status: "Open",
    created_at: "2026-11-04 11:30:00",
  },
  {
    id: "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f62",
    title: "UI/UX Designer Intern",
    company_name: "Creative Studio Lab",
    location: "Dhaka, Bangladesh",
    description:
      "Design wireframes, high-fidelity prototypes in Figma, and conduct usability tests for student productivity apps and job boards.",
    salary: "৳10,000 / month",
    deadline: "2026-11-15",
    status: "Closed",
    created_at: "2026-11-03 09:15:00",
  },
  {
    id: "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f63",
    title: "Data Science & Analytics Intern",
    company_name: "FinTech Matrix",
    location: "Hybrid (Dhaka)",
    description:
      "Clean, process, and analyze financial data using Pandas and SQL. Build exploratory visualization dashboards for executive decision making.",
    salary: "৳14,000 / month",
    deadline: "2026-12-05",
    status: "Open",
    created_at: "2026-11-02 14:20:00",
  },
  {
    id: "f8d1e2a0-4b5c-4d6e-8f9a-1b2c3d4e5f64",
    title: "Full Stack Engineering Intern",
    company_name: "CloudCraft Systems",
    location: "Remote",
    description:
      "Hands-on experience developing end-to-end web features connecting React frontends with Python microservices and Supabase cloud databases.",
    salary: "৳18,000 / month",
    deadline: "2026-12-15",
    status: "Open",
    created_at: "2026-11-01 16:45:00",
  },
];

const LOCAL_STORAGE_KEY = "cse309_internships_data";

function getLocalStorageItems(): Internship[] {
  const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
  if (!raw) {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(FALLBACK_SEED));
    return FALLBACK_SEED;
  }
  try {
    return JSON.parse(raw);
  } catch {
    return FALLBACK_SEED;
  }
}

function saveLocalStorageItems(items: Internship[]): void {
  localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(items));
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      signal: AbortSignal.timeout(2000),
    });
    return res.ok;
  } catch {
    return false;
  }
}

// 1. READ LIST (R in CRUD)
export async function fetchInternships(
  search = "",
  status = "All"
): Promise<{ data: Internship[]; isOffline: boolean }> {
  try {
    const params = new URLSearchParams();
    if (search.trim()) params.append("search", search.trim());
    if (status && status !== "All") params.append("status", status);

    const res = await fetch(`${API_BASE_URL}/internships?${params.toString()}`, {
      method: "GET",
      signal: AbortSignal.timeout(4000),
    });

    if (res.ok) {
      const data: Internship[] = await res.json();
      if (!search.trim() && status === "All") {
        saveLocalStorageItems(data);
      }
      return { data, isOffline: false };
    }
  } catch (err) {
    console.warn("Backend unavailable, using local mock data:", err);
  }

  // Offline fallback
  let items = getLocalStorageItems();
  if (status !== "All") {
    items = items.filter(
      (i) => i.status.toLowerCase() === status.toLowerCase()
    );
  }
  if (search.trim()) {
    const q = search.trim().toLowerCase();
    items = items.filter(
      (i) =>
        i.title.toLowerCase().includes(q) ||
        i.company_name.toLowerCase().includes(q) ||
        i.location.toLowerCase().includes(q) ||
        i.description.toLowerCase().includes(q)
    );
  }
  return { data: items, isOffline: true };
}

// 2. READ SINGLE (R in CRUD)
export async function fetchInternshipById(
  id: string
): Promise<{ data: Internship; isOffline: boolean }> {
  try {
    const res = await fetch(`${API_BASE_URL}/internships/${id}`, {
      method: "GET",
      signal: AbortSignal.timeout(4000),
    });

    if (res.ok) {
      const data: Internship = await res.json();
      return { data, isOffline: false };
    }
  } catch (err) {
    console.warn("Backend unavailable, reading from local fallback:", err);
  }

  const items = getLocalStorageItems();
  const found = items.find((i) => i.id === id);
  if (!found) {
    throw new Error("Internship not found");
  }
  return { data: found, isOffline: true };
}

// 3. CREATE (C in CRUD)
export async function createInternship(
  payload: InternshipCreateInput
): Promise<{ data: Internship; isOffline: boolean }> {
  try {
    const res = await fetch(`${API_BASE_URL}/internships`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(4000),
    });

    if (res.ok) {
      const data: Internship = await res.json();
      const current = getLocalStorageItems().filter((i) => i.id !== data.id);
      current.unshift(data);
      saveLocalStorageItems(current);
      return { data, isOffline: false };
    }
  } catch (err) {
    console.warn("Backend unavailable, creating in local fallback:", err);
  }

  const items = getLocalStorageItems();
  const newItem: Internship = {
    ...payload,
    id: crypto.randomUUID(),
    created_at: new Date().toISOString().replace("T", " ").substring(0, 19),
  };
  items.unshift(newItem);
  saveLocalStorageItems(items);
  return { data: newItem, isOffline: true };
}

// 4. UPDATE (U in CRUD)
export async function updateInternship(
  id: string,
  payload: InternshipUpdateInput
): Promise<{ data: Internship; isOffline: boolean }> {
  try {
    const res = await fetch(`${API_BASE_URL}/internships/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(4000),
    });

    if (res.ok) {
      const data: Internship = await res.json();
      const current = getLocalStorageItems().map((i) => (i.id === data.id ? data : i));
      saveLocalStorageItems(current);
      return { data, isOffline: false };
    }
  } catch (err) {
    console.warn("Backend unavailable, updating in local fallback:", err);
  }

  const items = getLocalStorageItems();
  const idx = items.findIndex((i) => i.id === id);
  if (idx === -1) {
    throw new Error("Internship not found");
  }
  const updatedItem: Internship = {
    ...items[idx],
    ...payload,
  };
  items[idx] = updatedItem;
  saveLocalStorageItems(items);
  return { data: updatedItem, isOffline: true };
}

// 5. DELETE (D in CRUD)
export async function deleteInternship(
  id: string
): Promise<{ success: boolean; isOffline: boolean }> {
  try {
    const res = await fetch(`${API_BASE_URL}/internships/${id}`, {
      method: "DELETE",
      signal: AbortSignal.timeout(4000),
    });

    if (res.ok) {
      const current = getLocalStorageItems().filter((i) => i.id !== id);
      saveLocalStorageItems(current);
      return { success: true, isOffline: false };
    }
  } catch (err) {
    console.warn("Backend unavailable, deleting from local fallback:", err);
  }

  const items = getLocalStorageItems().filter((i) => i.id !== id);
  saveLocalStorageItems(items);
  return { success: true, isOffline: true };
}

// STATS
export async function fetchStats(): Promise<InternshipStats> {
  try {
    const res = await fetch(`${API_BASE_URL}/internships/stats/summary`, {
      method: "GET",
      signal: AbortSignal.timeout(4000),
    });
    if (res.ok) {
      return await res.json();
    }
  } catch {
    // ignore
  }

  const items = getLocalStorageItems();
  return {
    total: items.length,
    open: items.filter((i) => i.status.toLowerCase() === "open").length,
    closed: items.filter((i) => i.status.toLowerCase() === "closed").length,
    remote: items.filter((i) => i.location.toLowerCase().includes("remote")).length,
  };
}

// SEED RESET
export async function resetDatabaseSeed(): Promise<void> {
  try {
    const res = await fetch(`${API_BASE_URL}/internships/seed/reset`, {
      method: "POST",
      signal: AbortSignal.timeout(4000),
    });
    if (res.ok) return;
  } catch {
    // ignore
  }
  localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(FALLBACK_SEED));
}
