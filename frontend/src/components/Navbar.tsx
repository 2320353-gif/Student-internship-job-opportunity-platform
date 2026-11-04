import React from "react";

interface NavbarProps {
  onOpenCreate: () => void;
  isBackendConnected: boolean;
  onRefresh: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenCreate,
  isBackendConnected,
  onRefresh,
}) => {
  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="brand-icon">🎓</div>
          <div>
            <div className="brand-title-wrap">
              <h1 className="brand-title">OpportunityHub</h1>
            </div>
            <p className="brand-subtitle">
              Student Internship & Job Opportunity Platform
            </p>
          </div>
        </div>

        <div className="navbar-actions">
          <button
            className="btn btn-secondary btn-icon"
            onClick={onRefresh}
            title="Reload data from server"
          >
            🔄 Refresh
          </button>

          <button className="btn btn-primary" onClick={onOpenCreate}>
            <span className="btn-icon-plus">+</span> Post Internship
          </button>
        </div>
      </div>
    </header>
  );
};
