import React, { useState, useEffect } from "react";
import {
  Internship,
  InternshipCreateInput,
  InternshipUpdateInput,
} from "../types/internship";

interface InternshipFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmitCreate: (data: InternshipCreateInput) => Promise<void>;
  onSubmitUpdate: (id: string, data: InternshipUpdateInput) => Promise<void>;
  editingInternship: Internship | null;
}

export const InternshipFormModal: React.FC<InternshipFormModalProps> = ({
  isOpen,
  onClose,
  onSubmitCreate,
  onSubmitUpdate,
  editingInternship,
}) => {
  const isEditing = Boolean(editingInternship);

  const [title, setTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [location, setLocation] = useState("");
  const [salary, setSalary] = useState("");
  const [deadline, setDeadline] = useState("");
  const [status, setStatus] = useState("Open");
  const [description, setDescription] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState("");

  useEffect(() => {
    if (editingInternship) {
      setTitle(editingInternship.title);
      setCompanyName(editingInternship.company_name);
      setLocation(editingInternship.location);
      setSalary(editingInternship.salary);
      setDeadline(editingInternship.deadline);
      setStatus(editingInternship.status);
      setDescription(editingInternship.description);
    } else {
      // Default initial values for new entry
      setTitle("");
      setCompanyName("");
      setLocation("Dhaka, Bangladesh");
      setSalary("৳12,000 / month");
      // Default deadline to 3 weeks ahead
      const futureDate = new Date();
      futureDate.setDate(futureDate.getDate() + 21);
      setDeadline(futureDate.toISOString().split("T")[0]);
      setStatus("Open");
      setDescription("");
    }
    setFormError("");
  }, [editingInternship, isOpen]);

  if (!isOpen) return null;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFormError("");

    if (!title.trim()) {
      setFormError("Job/Internship Title is required.");
      return;
    }
    if (!companyName.trim()) {
      setFormError("Company Name is required.");
      return;
    }
    if (!location.trim()) {
      setFormError("Location is required.");
      return;
    }
    if (!description.trim()) {
      setFormError("Job Description is required.");
      return;
    }

    try {
      setIsSubmitting(true);
      if (isEditing && editingInternship) {
        await onSubmitUpdate(editingInternship.id, {
          title: title.trim(),
          company_name: companyName.trim(),
          location: location.trim(),
          salary: salary.trim() || "Unpaid",
          deadline: deadline || new Date().toISOString().split("T")[0],
          status,
          description: description.trim(),
        });
      } else {
        await onSubmitCreate({
          title: title.trim(),
          company_name: companyName.trim(),
          location: location.trim(),
          salary: salary.trim() || "Unpaid",
          deadline: deadline || new Date().toISOString().split("T")[0],
          status,
          description: description.trim(),
        });
      }
      onClose();
    } catch (err) {
      setFormError(
        err instanceof Error ? err.message : "Failed to save internship"
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-container modal-md"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal-header">
          <div>
            <h2 className="modal-title">
              {isEditing ? "Edit Internship Opportunity" : "Post New Internship"}
            </h2>
            <p className="modal-subtitle">
              {isEditing
                ? "Update requirements, deadline, or compensation"
                : "Fill in the details to publish a new student opportunity"}
            </p>
          </div>
          <button
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          {formError && (
            <div className="form-alert-error">
              <span>⚠️</span> {formError}
            </div>
          )}

          <div className="form-grid">
            <div className="form-group form-col-full">
              <label className="form-label" htmlFor="internship-title">
                Internship Title <span className="text-danger">*</span>
              </label>
              <input
                id="internship-title"
                type="text"
                className="form-input"
                placeholder="e.g. Junior Frontend Developer Intern"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="company-name">
                Company Name <span className="text-danger">*</span>
              </label>
              <input
                id="company-name"
                type="text"
                className="form-input"
                placeholder="e.g. Brain Station 23 / Pathao"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="location">
                Location <span className="text-danger">*</span>
              </label>
              <input
                id="location"
                type="text"
                className="form-input"
                placeholder="e.g. Dhaka, Bangladesh / Remote / Hybrid"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="salary">
                Stipend / Salary
              </label>
              <input
                id="salary"
                type="text"
                className="form-input"
                placeholder="e.g. ৳12,000 / month, Unpaid, Negotiable"
                value={salary}
                onChange={(e) => setSalary(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="deadline">
                Application Deadline
              </label>
              <input
                id="deadline"
                type="date"
                className="form-input"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                required
              />
            </div>

            <div className="form-group form-col-full">
              <label className="form-label">Opportunity Status</label>
              <div className="status-radio-group">
                <label className={`radio-pill ${status === "Open" ? "radio-pill-active-open" : ""}`}>
                  <input
                    type="radio"
                    name="status"
                    value="Open"
                    checked={status === "Open"}
                    onChange={() => setStatus("Open")}
                  />
                  🟢 Open (Accepting Applications)
                </label>
                <label className={`radio-pill ${status === "Closed" ? "radio-pill-active-closed" : ""}`}>
                  <input
                    type="radio"
                    name="status"
                    value="Closed"
                    checked={status === "Closed"}
                    onChange={() => setStatus("Closed")}
                  />
                  ⚪ Closed / Archived
                </label>
              </div>
            </div>

            <div className="form-group form-col-full">
              <label className="form-label" htmlFor="description">
                Job Description & Qualifications <span className="text-danger">*</span>
              </label>
              <textarea
                id="description"
                rows={4}
                className="form-textarea"
                placeholder="Describe role responsibilities, required technical skills (e.g. React, Python), and learning opportunities..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting
                ? "Saving..."
                : isEditing
                ? "💾 Save Changes"
                : "🚀 Publish Opportunity"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
