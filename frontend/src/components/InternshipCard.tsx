import React from "react";
import { Internship } from "../types/internship";

interface InternshipCardProps {
  internship: Internship;
  onViewDetails: (item: Internship) => void;
  onEdit: (item: Internship) => void;
  onDelete: (item: Internship) => void;
}

export const InternshipCard: React.FC<InternshipCardProps> = ({
  internship,
  onViewDetails,
  onEdit,
  onDelete,
}) => {
  const isOpen = internship.status.toLowerCase() === "open";
  const isRemote = internship.location.toLowerCase().includes("remote");

  return (
    <article className="internship-card">
      <div className="card-top">
        <div className="card-header-info">
          <div className="card-badges">
            <span
              className={`badge ${isOpen ? "badge-success" : "badge-neutral"}`}
            >
              <span className="badge-dot"></span>
              {internship.status}
            </span>
            {isRemote && (
              <span className="badge badge-indigo">
                🌐 Remote
              </span>
            )}
          </div>
          <h3 className="card-title" onClick={() => onViewDetails(internship)}>
            {internship.title}
          </h3>
          <p className="card-company">
            🏢 {internship.company_name}
          </p>
        </div>
      </div>

      <p className="card-description">{internship.description}</p>

      <div className="card-meta">
        <div className="meta-item">
          <span className="meta-icon">📍</span>
          <span className="meta-text">{internship.location}</span>
        </div>
        <div className="meta-item">
          <span className="meta-icon">💰</span>
          <span className="meta-text meta-salary">{internship.salary}</span>
        </div>
        <div className="meta-item">
          <span className="meta-icon">⏰</span>
          <span className="meta-text">Deadline: {internship.deadline}</span>
        </div>
      </div>

      <div className="card-actions">
        <button
          className="btn btn-outline btn-sm"
          onClick={() => onViewDetails(internship)}
          title="Read Single Record (GET /api/internships/:id)"
        >
          👁 View Details
        </button>
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => onEdit(internship)}
          title="Update Record (PUT /api/internships/:id)"
        >
          ✏️ Edit
        </button>
        <button
          className="btn btn-danger-outline btn-sm"
          onClick={() => onDelete(internship)}
          title="Delete Record (DELETE /api/internships/:id)"
        >
          🗑 Delete
        </button>
      </div>
    </article>
  );
};
