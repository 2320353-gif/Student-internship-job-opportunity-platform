import React from "react";
import { Internship } from "../types/internship";

interface InternshipDetailModalProps {
  internship: Internship | null;
  onClose: () => void;
  onEdit: (item: Internship) => void;
  onDelete: (item: Internship) => void;
}

export const InternshipDetailModal: React.FC<InternshipDetailModalProps> = ({
  internship,
  onClose,
  onEdit,
  onDelete,
}) => {
  if (!internship) return null;

  const isOpen = internship.status.toLowerCase() === "open";
  const isRemote = internship.location.toLowerCase().includes("remote");

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-container modal-lg"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal-header">
          <div>
            <div className="modal-badges">
              <span
                className={`badge ${isOpen ? "badge-success" : "badge-neutral"}`}
              >
                <span className="badge-dot"></span>
                {internship.status}
              </span>
              {isRemote && <span className="badge badge-indigo">🌐 Remote Opportunity</span>}
            </div>
            <h2 className="modal-title">{internship.title}</h2>
            <p className="modal-subtitle">🏢 {internship.company_name}</p>
          </div>
          <button
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        <div className="modal-body">
          <div className="detail-meta-grid">
            <div className="detail-meta-card">
              <span className="detail-meta-label">Location</span>
              <span className="detail-meta-val">📍 {internship.location}</span>
            </div>
            <div className="detail-meta-card">
              <span className="detail-meta-label">Compensation / Salary</span>
              <span className="detail-meta-val text-emerald">
                💰 {internship.salary}
              </span>
            </div>
            <div className="detail-meta-card">
              <span className="detail-meta-label">Application Deadline</span>
              <span className="detail-meta-val">⏰ {internship.deadline}</span>
            </div>
            <div className="detail-meta-card">
              <span className="detail-meta-label">Posted Date</span>
              <span className="detail-meta-val">
                📅 {internship.created_at || "Recent"}
              </span>
            </div>
          </div>

          <div className="detail-section">
            <h4 className="detail-section-title">About the Role & Requirements</h4>
            <div className="detail-description-text">
              {internship.description.split("\n").map((para, i) => (
                <p key={i}>{para}</p>
              ))}
            </div>
          </div>

          <div className="detail-tech-box">
            <span className="tech-box-label">Database Record ID (UUID):</span>
            <code className="tech-box-code">{internship.id}</code>
            <p className="tech-box-hint">
              Fetched via <code>GET /api/internships/{internship.id}</code>
            </p>
          </div>
        </div>

        <div className="modal-footer">
          <button
            className="btn btn-danger-outline"
            onClick={() => {
              onClose();
              onDelete(internship);
            }}
          >
            🗑 Delete
          </button>
          <div className="modal-footer-right">
            <button
              className="btn btn-secondary"
              onClick={() => {
                onClose();
                onEdit(internship);
              }}
            >
              ✏️ Edit Opportunity
            </button>
            <button className="btn btn-primary" onClick={onClose}>
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
