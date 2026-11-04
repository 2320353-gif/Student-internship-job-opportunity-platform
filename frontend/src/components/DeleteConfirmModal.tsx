import React from "react";
import { Internship } from "../types/internship";

interface DeleteConfirmModalProps {
  internship: Internship | null;
  onClose: () => void;
  onConfirm: (id: string) => Promise<void>;
  isDeleting: boolean;
}

export const DeleteConfirmModal: React.FC<DeleteConfirmModalProps> = ({
  internship,
  onClose,
  onConfirm,
  isDeleting,
}) => {
  if (!internship) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-container modal-sm"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal-header">
          <div>
            <h2 className="modal-title">Confirm Deletion</h2>
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
          <div className="delete-icon-wrap">⚠️</div>
          <p className="delete-confirm-text">
            Are you sure you want to remove{" "}
            <strong>&quot;{internship.title}&quot;</strong> at{" "}
            <strong>{internship.company_name}</strong>?
          </p>
          <p className="delete-warning-note">
            This operation will call{" "}
            <code>DELETE /api/internships/{internship.id}</code> and permanently
            remove the record.
          </p>
        </div>

        <div className="modal-footer">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onClose}
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button
            type="button"
            className="btn btn-danger"
            onClick={() => onConfirm(internship.id)}
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Yes, Delete Record"}
          </button>
        </div>
      </div>
    </div>
  );
};
