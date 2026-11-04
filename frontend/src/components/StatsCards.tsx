import React from "react";
import { InternshipStats } from "../types/internship";

interface StatsCardsProps {
  stats: InternshipStats;
  onFilterStatus: (status: string) => void;
  activeStatus: string;
}

export const StatsCards: React.FC<StatsCardsProps> = ({
  stats,
  onFilterStatus,
  activeStatus,
}) => {
  return (
    <div className="stats-grid">
      <div
        className={`stat-card stat-total ${activeStatus === "All" ? "stat-active" : ""}`}
        onClick={() => onFilterStatus("All")}
        role="button"
        tabIndex={0}
      >
        <div className="stat-header">
          <span className="stat-label">Total Opportunities</span>
          <span className="stat-icon">📋</span>
        </div>
        <div className="stat-value">{stats.total}</div>
        <div className="stat-hint">All posted internships</div>
      </div>

      <div
        className={`stat-card stat-open ${activeStatus === "Open" ? "stat-active" : ""}`}
        onClick={() => onFilterStatus("Open")}
        role="button"
        tabIndex={0}
      >
        <div className="stat-header">
          <span className="stat-label">Active / Open</span>
          <span className="stat-icon">🟢</span>
        </div>
        <div className="stat-value text-emerald">{stats.open}</div>
        <div className="stat-hint">Accepting student applications</div>
      </div>

      <div
        className={`stat-card stat-closed ${activeStatus === "Closed" ? "stat-active" : ""}`}
        onClick={() => onFilterStatus("Closed")}
        role="button"
        tabIndex={0}
      >
        <div className="stat-header">
          <span className="stat-label">Closed / Archived</span>
          <span className="stat-icon">⚪</span>
        </div>
        <div className="stat-value text-slate">{stats.closed}</div>
        <div className="stat-hint">Application window closed</div>
      </div>

      <div className="stat-card stat-remote">
        <div className="stat-header">
          <span className="stat-label">Remote Positions</span>
          <span className="stat-icon">🌐</span>
        </div>
        <div className="stat-value text-indigo">{stats.remote}</div>
        <div className="stat-hint">Work from anywhere</div>
      </div>
    </div>
  );
};
