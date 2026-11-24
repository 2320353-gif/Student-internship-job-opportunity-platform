import React from "react";
import { Internship } from "../types/internship";
import { User } from "../types/auth";

interface InternshipCardProps {
  internship: Internship;
  currentUser?: User | null;
  onViewDetails: (item: Internship) => void;
  onEdit: (item: Internship) => void;
  onDelete: (item: Internship) => void;
}

export const InternshipCard: React.FC<InternshipCardProps> = ({
  internship,
  currentUser,
  onViewDetails,
  onEdit,
  onDelete,
}) => {
  const isOpen = internship.status.toLowerCase() === "open";
  const isRemote = internship.location.toLowerCase().includes("remote");

  // RBAC ownership logic:
  // 1. Admin Manager (Main Admin) can modify all postings
  // 2. Owner can always modify their own postings
  // 3. Security Officer can modify student postings, but CANNOT modify Admin Manager's postings
  // 4. Students can only modify their own postings
  const isOwner = Boolean(currentUser && internship.user_id && currentUser.id === internship.user_id);
  const isMainAdmin = Boolean(currentUser && (currentUser.email === "admin@platform.com" || currentUser.is_main_admin));
  const isSecurityOfficer = Boolean(currentUser && (currentUser.email === "admin2@platform.com" || currentUser.role === "security_officer" || currentUser.name.toLowerCase().includes("security")));
  const isPostByMainAdmin = Boolean(internship.user_id && internship.user_id === "a1000000-0000-0000-0000-000000000001");

  const canModify = Boolean(
    isOwner ||
    isMainAdmin ||
    (isSecurityOfficer && !isPostByMainAdmin) ||
    (!internship.user_id && (isMainAdmin || isSecurityOfficer || currentUser?.role === "admin"))
  );

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
            {isOwner && (
              <span className="badge badge-indigo" title="You posted this opportunity">
                👤 My Post
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
          style={!canModify ? { width: "100%", justifyContent: "center" } : undefined}
        >
          👁 View Details {!canModify && "(Read-Only)"}
        </button>
        {canModify && (
          <>
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
          </>
        )}
      </div>
    </article>
  );
};
