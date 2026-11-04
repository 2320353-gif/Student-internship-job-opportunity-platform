import React from "react";

interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  statusFilter: string;
  onStatusChange: (status: string) => void;
  sortBy: string;
  onSortChange: (sort: string) => void;
  onResetSeed: () => void;
  totalResults: number;
}

export const FilterBar: React.FC<FilterBarProps> = ({
  search,
  onSearchChange,
  statusFilter,
  onStatusChange,
  sortBy,
  onSortChange,
  onResetSeed,
  totalResults,
}) => {
  return (
    <div className="filter-bar">
      <div className="filter-search-wrap">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          className="search-input"
          placeholder="Search by job title, company, location, or skills..."
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
        />
        {search && (
          <button
            className="search-clear-btn"
            onClick={() => onSearchChange("")}
            title="Clear search"
          >
            ✕
          </button>
        )}
      </div>

      <div className="filter-controls">
        <div className="status-tabs">
          {["All", "Open", "Closed"].map((tab) => (
            <button
              key={tab}
              className={`tab-btn ${statusFilter === tab ? "tab-active" : ""}`}
              onClick={() => onStatusChange(tab)}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="sort-wrap">
          <label htmlFor="sort-select" className="sort-label">
            Sort by:
          </label>
          <select
            id="sort-select"
            className="sort-select"
            value={sortBy}
            onChange={(e) => onSortChange(e.target.value)}
          >
            <option value="newest">Newest First</option>
            <option value="title">Job Title (A-Z)</option>
            <option value="company">Company Name (A-Z)</option>
            <option value="deadline">Application Deadline</option>
          </select>
        </div>

        <button
          className="btn btn-outline btn-reset"
          onClick={onResetSeed}
          title="Reset sample data for viva demonstration"
        >
          ⚡ Reset Demo Data
        </button>
      </div>

      <div className="results-count-bar">
        <span>
          Showing <strong>{totalResults}</strong> internship opportunit{totalResults === 1 ? "y" : "ies"}
        </span>
        {search && (
          <span className="search-tag">
            Filter: &quot;{search}&quot;
          </span>
        )}
      </div>
    </div>
  );
};
