# PRD: Product Requirements Document
## Student Internship & Job Opportunity Platform

| Field | Details |
|---|---|
| Project | Student Internship & Job Opportunity Platform |
| Suggested product name | CareerLink |
| Version | 1.0 |
| Status | Initial Draft |
| Project type | Web Applications & Internet course project |
| Application | Frontend-only website |
| Main users | Student, Company, Admin |
| Database/backend | Not required |

## 1. Product Overview
CareerLink is a student-focused website concept for discovering internships and entry-level jobs. Students can browse, search, filter, view opportunity details, and demonstrate applying for a role. Companies can demonstrate creating and managing listings and viewing illustrative applicants. Administrators can review sample users and moderate sample listings.

The course prototype uses static sample data and client-side state. Login, application submission, notifications, and moderation are simulations. There is no database, backend API, real authentication, or real application delivery.

## 2. Problem Statement
Students may need to search several sources to find internships and entry-level roles. A centralized interface can make opportunities easier to discover and compare. Companies also need a clear way to present openings. CareerLink demonstrates these workflows through a simple, role-based web interface.

## 3. Product Vision
Provide a simple and accessible platform concept where students discover opportunities, companies showcase openings, and administrators oversee sample platform content.

## 4. Objectives
1. Build a responsive internship and job listing website.
2. Provide separate Student, Company, and Admin experiences.
3. Support opportunity search, filtering, sorting, and detail views.
4. Demonstrate student applications and application-status tracking.
5. Demonstrate company listing creation, editing, and deletion.
6. Demonstrate admin listing moderation and dashboard summaries.
7. Use reusable components and a maintainable code structure.
8. Validate forms and display helpful feedback.
9. Avoid database and backend dependencies.
10. Document the project for GitHub and course assessment.

## 5. Target Users
### Students
Want to discover opportunities, review requirements, submit demo applications, track sample statuses, and manage a basic profile.

### Companies
Want to create and manage sample job/internship listings and view illustrative applicants.

### Administrators
Want to inspect sample users and listings, view dashboard summaries, and demonstrate moderation actions.

### Guests
Want to browse public listings and details before selecting a demo role.

## 6. Roles and Capabilities

| Capability | Guest | Student | Company | Admin |
|---|---|---|---|---|
| Browse/search listings | Yes | Yes | Yes | Yes |
| View listing details | Yes | Yes | Yes | Yes |
| Submit demo application | No | Yes | No | No |
| View own sample applications | No | Yes | No | Demo overview |
| Manage student profile | No | Yes | No | No |
| Create/edit/delete own listings | No | No | Yes | Moderation only |
| View illustrative applicants | No | No | Yes | Demo overview |
| Review sample users/listings | No | No | No | Yes |

These are UI capabilities only, not secure authorization.

## 7. Scope
### In Scope
- Responsive homepage and navigation.
- Opportunity catalog and detail pages.
- Search, filters, and sorting.
- Student, Company, and Admin demo login/role selection.
- Student dashboard, profile, and application-status list.
- Simulated application submission.
- Company dashboard and listing management.
- Illustrative applicant list.
- Admin dashboard and sample listing moderation.
- Form validation, confirmation messages, and empty states.
- Static JavaScript/JSON sample data.
- Client-side state management.
- GitHub documentation.

### Out of Scope
- Database, backend, or API.
- Real authentication, password reset, or email verification.
- Secure role authorization.
- Real resume uploads or secure document storage.
- Real applications sent to employers.
- Email/SMS notifications, chat, and interview scheduling.
- Real-time updates, production analytics, or AI matching.
- Payment processing.

## 8. Functional Requirements
### FR-01 Homepage
Display the product name, purpose, navigation, featured sample opportunities, and calls to action.

### FR-02 Opportunity Catalog
Display title, company, opportunity type, location/work mode, and summary. Provide links to details and an empty state when no results exist.

### FR-03 Search and Filtering
Search titles, company names, locations, and available keywords. Filter by type, category, or work mode when those fields exist. Support sorting by a selected available field and clearing filters.

### FR-04 Opportunity Details
Show description, responsibilities, qualifications, company, type, location, and work arrangement. Provide an Apply action for the student demo flow.

### FR-05 Demo Login
Provide separate Student, Company, and Admin entry points. Validate required fields, navigate to the selected dashboard, and clearly state that login is simulated.

### FR-06 Student Dashboard
Provide links to profile, opportunities, and applications. Show illustrative application summaries and useful empty states.

### FR-07 Student Application
Allow a student to complete a demo application form. Validate required fields, display a confirmation, and optionally add a local sample record. Do not send the application to an employer.

### FR-08 Application Status
Show sample applications with statuses such as Submitted, Under Review, Shortlisted, or Not Selected.

### FR-09 Student Profile
Allow editing of non-sensitive demonstration fields such as display name, education, skills, and a resume filename placeholder. Do not require a real resume upload.

### FR-10 Company Dashboard
Show sample listing summaries and navigation to listing management and applicant views.

### FR-11 Listing Management
Allow a company demo user to add, edit, and remove listings in client-side state. Validate required fields including title, description, company, and type.

### FR-12 Applicant Review
Display illustrative applicant records associated with sample listings. Do not imply that they are real applicants.

### FR-13 Admin Dashboard
Display illustrative counts for users, companies, listings, and applications.

### FR-14 Admin Moderation
Allow review or local removal of sample listings, with confirmation for destructive actions and feedback afterward.

### FR-15 Validation and Error States
Handle invalid forms, empty search results, missing listing IDs, empty lists, and successful demo actions with clear messages.

### FR-16 Responsive Navigation
Keep navigation, forms, listing cards, and dashboards usable on desktop, tablet, and mobile layouts.

## 9. Non-Functional Requirements
- **Usability:** Clear labels, consistent navigation, and understandable actions.
- **Responsiveness:** Adapt to common desktop, tablet, and mobile widths.
- **Accessibility:** Semantic HTML, labeled inputs, keyboard support, visible focus, and meaningful alt text.
- **Performance:** Appropriately sized assets and minimal unnecessary dependencies.
- **Maintainability:** Separate pages, components, data, and styles.
- **Reliability:** Empty or invalid states must not crash the interface.
- **Privacy:** Do not request real passwords, sensitive data, or real resumes.
- **Transparency:** Clearly label demo authentication, sample records, and simulated applications.

## 10. Main User Journeys
### Student applies
1. Open the site and browse/search listings.
2. Open a listing's detail page.
3. Select Apply and complete the demo form.
4. Submit and see a simulated confirmation.
5. View a local/sample application status if implemented.

### Company publishes a listing
1. Select Company and enter the demo login flow.
2. Open the company dashboard.
3. Add a listing and complete required fields.
4. Save and see the listing in local state.
5. Edit or remove it as needed.

### Admin moderates a listing
1. Select Admin and open the dashboard.
2. Review sample listings.
3. Choose a moderation action and confirm.
4. See the local display update.

## 11. Design Guidelines
Use a clean, professional career-focused visual style. Keep search prominent, display listing details consistently, use readable status labels, provide confirmation before destructive actions, and include useful empty states. Dashboards should prioritize role-specific tasks.

## 12. Sample Data
Use fictional opportunities such as Software Engineering Intern, UI/UX Design Intern, Data Analyst Intern, Junior Web Developer, Marketing Intern, and Graduate Trainee. All company names, people, applications, dates, and descriptions are illustrative.

## 13. Technical Constraints
Use a frontend framework such as React, JavaScript, HTML5, and CSS3. Keep sample records in local modules and use client-side state. Optional localStorage may preserve non-sensitive demo data, but it does not provide centralized or secure persistence. Changes may be lost on refresh if browser storage is not used.

## 14. Success Metrics
- Student, Company, and Admin views are accessible.
- Search and filters work with sample listings.
- Listing details display correctly.
- Demo application workflow shows validation and confirmation.
- Company listing CRUD operations work in client-side state.
- Admin moderation screens work with sample data.
- Main pages are responsive.
- Documentation includes PRD, SRS, and TDD.
- No database or backend is required.

## 15. Risks and Mitigation
| Risk | Mitigation |
|---|---|
| Demo login mistaken for secure authentication | Show a demo-only notice |
| Data resets | Explain reset behavior; optionally use localStorage |
| Scope grows too large | Prioritize catalog, application flow, and dashboards |
| Sample records seem real | Label them as fictional/demo data |
| Sensitive resume data is collected | Use a filename placeholder only |
| UI permissions mistaken for security | Document lack of server-side authorization |

## 16. Future Enhancements
A later version could add a backend, database, secure authentication, resume storage, real application delivery, email notifications, saved jobs, matching, messaging, interview scheduling, and analytics. These are outside the current scope.

## 17. Acceptance Criteria
1. Homepage and navigation work.
2. Listings can be browsed, searched, and filtered.
3. Detail pages show relevant listing information.
4. Each role has a separate demo entry point and dashboard.
5. Student application flow validates input and shows confirmation.
6. Company can add, edit, and remove local listings.
7. Admin can review and moderate sample listings.
8. Forms and empty states provide useful feedback.
9. Core pages work at desktop and mobile widths.
10. The site runs without a database or backend.
11. Documentation explains demo limitations.

## 18. Conclusion
CareerLink is a frontend-only educational prototype for demonstrating opportunity discovery, simulated student applications, company listing management, and admin moderation. Its intentionally limited scope keeps it manageable while providing a foundation for future development.
