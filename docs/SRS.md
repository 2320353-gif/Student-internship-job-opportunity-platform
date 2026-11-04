# SRS: Software Requirements Specification
## Student Internship & Job Opportunity Platform

## 1. Introduction

### 1.1 Purpose
This document defines the functional and non-functional requirements for CareerLink, a student internship and job opportunity platform prototype. It is intended for developers, testers, instructors, and reviewers.

### 1.2 Scope
The system is a frontend-only website demonstrating opportunity discovery and role-specific workflows for Students, Companies, and Admins. It uses static sample data and client-side state. It does not provide production authentication, centralized persistence, or real application delivery.

### 1.3 Definitions
- **Opportunity:** A job or internship listing.
- **Demo login:** A simulated flow that navigates to a role dashboard without secure authentication.
- **Client-side state:** Data held by the running browser application.
- **Sample data:** Fictional records used for demonstration.

## 2. Overall Description

### 2.1 Product Perspective
The application is a standalone frontend. Local JavaScript or JSON modules supply sample records. React state or context can share updates between pages. Optional localStorage may preserve non-sensitive demo state but is not a database.

### 2.2 Main Functions
- Homepage and opportunity catalog.
- Search, filters, sorting, and detail pages.
- Demo login for Student, Company, and Admin.
- Student profile and simulated applications.
- Application-status list.
- Company listing management and illustrative applicant review.
- Admin dashboard and listing moderation.
- Form validation, confirmation messages, and empty states.
- Responsive layout.

### 2.3 User Classes
- **Guest:** Browses public listings and details.
- **Student:** Views a demo profile, submits simulated applications, and reviews sample statuses.
- **Company:** Creates and manages sample listings and views illustrative applicants.
- **Admin:** Reviews sample records and demonstrates moderation.

### 2.4 Operating Environment
A modern desktop or mobile browser and a local JavaScript development environment. React is recommended if it matches the repository setup.

### 2.5 Constraints
- No database, backend API, or external authentication service.
- No secure role authorization.
- No real resume uploads or sensitive personal information.
- No real employer application delivery or notifications.
- Changes may be session-only unless optional browser storage is used.

## 3. External Interface Requirements

### 3.1 User Interface
The site shall include a common header/footer, homepage, opportunity catalog, opportunity details, role selection/demo login, Student dashboard, Company dashboard, Admin dashboard, relevant forms, and not-found/empty/confirmation states.

### 3.2 Hardware Interface
No special hardware is required; a supported web browser is sufficient.

### 3.3 Software Interface
No external API, database, payment provider, email service, or authentication provider is required.

### 3.4 Communication Interface
Core functionality requires no application-level network communication beyond loading the site.

## 4. Functional Requirements

### FR-01: Homepage
Display the product name, purpose, navigation, featured sample opportunities if available, and links to browse listings and select a demo role.

**Acceptance:** Users can navigate from the homepage to the catalog and role selection.

### FR-02: Opportunity Catalog
Display each sample listing's title, company, type, location/work arrangement, and summary. Provide detail links and an empty state.

**Acceptance:** Each listing opens its matching detail page.

### FR-03: Search
Search relevant local fields such as title, company, location, and keywords. Display matching results and a no-results message.

**Acceptance:** A matching query returns relevant entries; a non-matching query shows an empty state.

### FR-04: Filters and Sorting
Filter by opportunity type and, if present, category or work arrangement. Support a selected sort order and a reset action.

**Acceptance:** Filters affect visible results and can be cleared.

### FR-05: Opportunity Details
Display description, responsibilities, qualifications, company, type, location, and work arrangement when available. Provide an Apply action for the student demo.

**Acceptance:** Details correspond to the selected listing; unknown IDs show a not-found state.

### FR-06: Role Selection and Demo Login
Provide separate Student, Company, and Admin entry points. Validate required fields, navigate to the appropriate dashboard, and clearly state that authentication is simulated.

**Acceptance:** Each role entry point reaches its matching dashboard without implying secure login.

### FR-07: Student Dashboard
Provide navigation to profile, opportunities, and applications. Display sample summary information and empty states.

**Acceptance:** The student can access supported dashboard sections.

### FR-08: Student Profile
Allow edits to non-sensitive fields such as display name, education, skills, and a resume filename placeholder. Validate required fields and show feedback.

**Acceptance:** Valid edits appear in local state; invalid required fields are identified.

### FR-09: Demo Application Submission
Allow the student to open an application form, validate required fields, submit, and see a simulated confirmation. An application record may be added to local state.

**Acceptance:** Valid submission displays confirmation; invalid submission displays validation errors. No employer or server receives the application.

### FR-10: Application Status
Display illustrative application records with statuses such as Submitted, Under Review, Shortlisted, and Not Selected.

**Acceptance:** Status labels are readable and sample records are identified appropriately.

### FR-11: Company Dashboard
Show sample listing summaries and links to listing management and applicant views.

**Acceptance:** Company users can access implemented company workflows.

### FR-12: Create and Edit Listings
Provide fields such as title, company, description, type, location, and work arrangement. Validate required fields and update client-side state.

**Acceptance:** Valid changes appear in the local listing view; invalid forms cannot be saved.

### FR-13: Delete Listings
Allow removal of sample listings after confirmation and update the current interface.

**Acceptance:** Confirmed removal updates local state; canceling leaves the listing unchanged.

### FR-14: Applicant Review
Show illustrative applicant records for sample listings, with an empty state where appropriate.

**Acceptance:** The company can inspect the available sample applicants without the interface implying they are real applicants.

### FR-15: Admin Dashboard
Display sample metrics for users, companies, listings, and applications, and provide access to relevant sample records.

**Acceptance:** The dashboard displays configured sample metrics and identifies them as illustrative.

### FR-16: Admin Moderation
Allow review, marking as reviewed, or local removal of a sample listing. Ask for confirmation before destructive actions and show feedback.

**Acceptance:** The local interface reflects the action and provides confirmation.

### FR-17: Validation and Error Handling
Validate required fields, handle empty lists and search results, handle unknown listing IDs, and display clear error or success messages.

**Acceptance:** Common invalid and empty states do not cause the interface to fail silently or crash.

### FR-18: Responsive Layout
Keep navigation, forms, listings, and dashboards usable on common desktop, tablet, and mobile widths.

**Acceptance:** Primary workflows remain usable at desktop and mobile sizes.

## 5. Non-Functional Requirements

- **Usability:** Consistent labels and understandable actions.
- **Accessibility:** Semantic HTML, associated form labels, keyboard operation, visible focus, and meaningful alt text.
- **Performance:** Avoid unnecessary dependencies and oversized assets.
- **Maintainability:** Organize pages, reusable components, sample data, and styles separately.
- **Reliability:** Handle invalid input, missing records, and empty states gracefully.
- **Privacy:** Do not collect real passwords, sensitive personal data, or real resumes.
- **Compatibility:** Support current mainstream browsers compatible with the selected framework.
- **Transparency:** State clearly that authentication, applications, records, and moderation are simulated.

## 6. Data Requirements

### Opportunity record
May contain `id`, `title`, `companyName`, `description`, `responsibilities`, `qualifications`, `type`, `category`, `location`, `workMode`, `postedDateLabel`, and `status`.

### Student profile
May contain `displayName`, `education`, `skills`, and `resumeLabel`. Use fictional, non-sensitive data.

### Application record
May contain `id`, `opportunityId`, `opportunityTitle`, `companyName`, `status`, and `submittedDateLabel`.

### Persistence
By default, records are local sample data and client-side state. Changes may reset on refresh. Optional localStorage is browser-specific and does not synchronize users or devices.

## 7. Use Cases

### UC-01: Browse opportunities
**Actor:** Guest or any role  
**Precondition:** The site is open.  
**Flow:** Open catalog, search or filter, inspect results, open a listing.  
**Result:** Selected listing details are displayed.  
**Alternative:** No matches produces an empty state.

### UC-02: Submit a demo application
**Actor:** Student  
**Precondition:** An opportunity detail page is open.  
**Flow:** Select Apply, complete required fields, submit, view confirmation.  
**Result:** Confirmation appears and an optional local record is created.  
**Alternative:** Invalid fields are identified and submission is not completed.

### UC-03: Manage a listing
**Actor:** Company  
**Precondition:** Company dashboard is open.  
**Flow:** Open listing form, enter details, validate, save, review the listing.  
**Result:** Client-side listing state updates.  
**Alternative:** Invalid fields trigger validation feedback.

### UC-04: Moderate a listing
**Actor:** Admin  
**Precondition:** Admin dashboard is open.  
**Flow:** Inspect a sample listing, choose an action, confirm, review updated display.  
**Result:** Local demo state reflects the action.  
**Alternative:** Canceling leaves the record unchanged.

## 8. Business Rules
- A listing must include a title, company name, description, and type.
- Required application fields must be completed before demo submission.
- Search and filters operate on local sample records only.
- Role dashboards are not security boundaries.
- Admin and company actions update local demonstration state only.
- All fictional records must be treated as sample data.
- The site must not claim that a real employer received an application.

## 9. Testing Requirements
Test:
- Main navigation and all implemented routes.
- Matching and non-matching search queries.
- Filters and filter reset.
- Valid and unknown listing details.
- Each role's demo navigation.
- Valid and invalid application forms.
- Listing creation, editing, and deletion.
- Applicant sample view and admin moderation.
- Empty states and confirmation messages.
- Responsive layout and keyboard navigation.

## 10. Acceptance Criteria
The prototype satisfies this specification when:
1. Main pages are navigable.
2. Sample opportunities can be searched and filtered.
3. Detail pages show relevant information.
4. Three demo role flows open separate dashboards.
5. Demo applications provide validation and confirmation.
6. Company listing operations work in client-side state.
7. Admin moderation works on sample data.
8. Empty and error states are understandable.
9. Core pages are responsive and keyboard usable.
10. No database or backend is required.
11. Demo limitations are documented.

## 11. Limitations
Without a backend, the site cannot securely authenticate users, enforce permissions, deliver real applications, synchronize shared records, or guarantee persistent data. These capabilities require a separate future phase.
