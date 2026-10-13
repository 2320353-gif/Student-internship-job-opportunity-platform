# TDD: Technical Design Document
## Student Internship & Job Opportunity Platform

## 1. Introduction

### 1.1 Purpose
This document describes the recommended frontend architecture, project structure, routing, components, sample data, state management, validation, and testing strategy for CareerLink.

### 1.2 Design Goals
- Keep the project manageable for a web development course.
- Separate UI components, pages, sample data, and styles.
- Support Student, Company, and Admin experiences.
- Avoid database and backend dependencies.
- Make the code easy to review and extend.

## 2. Recommended Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | React (recommended) | Reusable component-based interface |
| Language | JavaScript | Interaction logic |
| Markup | HTML5 / JSX | Semantic structure |
| Styling | CSS3 | Layout and responsive design |
| Routing | React Router, if used | Client-side navigation |
| Data | Local JavaScript/JSON | Fictional sample records |
| State | React state/context | In-session updates |
| Optional persistence | localStorage | Non-sensitive demo state only |
| Version control | Git/GitHub | Source history and collaboration |

Adapt this proposal to the framework already configured in the repository.

## 3. Architecture Overview

```text
Browser
  |
  v
Frontend Application
  |
  +-- Shared Layout (Header, Navigation, Footer)
  |
  +-- Public Pages
  |     +-- Home
  |     +-- Opportunity Catalog
  |     +-- Opportunity Details
  |     +-- About / Contact
  |
  +-- Role Flows
  |     +-- Student Dashboard / Profile / Applications
  |     +-- Company Dashboard / Listings / Applicants
  |     +-- Admin Dashboard / Listing Moderation
  |
  +-- Reusable Components
  |     +-- Opportunity Card
  |     +-- Search and Filters
  |     +-- Form Fields
  |     +-- Status Badge
  |     +-- Empty State / Confirmation
  |
  +-- Client-side State
  |     +-- Listings
  |     +-- Demo Applications
  |     +-- Student Profile
  |
  +-- Local Sample Data
        +-- Opportunities
        +-- Demo Users
        +-- Applications
```

There is no backend, database, or external API in this design.

## 4. Suggested Repository Structure

```text
careerlink/
├── public/
│   └── images/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── OpportunityCard.jsx
│   │   ├── SearchBar.jsx
│   │   ├── OpportunityFilters.jsx
│   │   ├── StatusBadge.jsx
│   │   └── EmptyState.jsx
│   ├── data/
│   │   ├── opportunities.js
│   │   ├── demoUsers.js
│   │   └── applications.js
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Opportunities.jsx
│   │   ├── OpportunityDetails.jsx
│   │   ├── RoleSelection.jsx
│   │   ├── DemoLogin.jsx
│   │   ├── StudentDashboard.jsx
│   │   ├── StudentProfile.jsx
│   │   ├── StudentApplications.jsx
│   │   ├── CompanyDashboard.jsx
│   │   ├── CompanyListings.jsx
│   │   ├── ListingForm.jsx
│   │   ├── CompanyApplicants.jsx
│   │   ├── AdminDashboard.jsx
│   │   └── AdminListings.jsx
│   ├── context/
│   │   └── DemoAppContext.jsx
│   ├── styles/
│   │   ├── global.css
│   │   ├── layout.css
│   │   └── dashboards.css
│   ├── App.jsx
│   └── main.jsx
├── docs/
│   ├── PRD.md
│   ├── SRS.md
│   └── TDD.md
├── package.json
├── README.md
└── .gitignore
```

This structure is a suggestion. Small projects may combine related files if that keeps the implementation clearer.

## 5. Route Design

If React Router is installed, suggested routes are:

| Route | Page |
|---|---|
| `/` | Home |
| `/opportunities` | Opportunity catalog |
| `/opportunities/:id` | Opportunity details |
| `/about` | About |
| `/contact` | Contact |
| `/login` | Role selection |
| `/login/student` | Student demo login |
| `/login/company` | Company demo login |
| `/login/admin` | Admin demo login |
| `/student/dashboard` | Student dashboard |
| `/student/profile` | Student profile |
| `/student/applications` | Student applications |
| `/company/dashboard` | Company dashboard |
| `/company/listings` | Company listing management |
| `/company/listings/new` | Create listing |
| `/company/listings/:id/edit` | Edit listing |
| `/company/applicants` | Illustrative applicants |
| `/admin/dashboard` | Admin dashboard |
| `/admin/listings` | Admin listing review |
| `*` | Not-found page |

**Security note:** These routes are only navigation in the demo. Client-side route guards do not securely protect data or enforce roles.

## 6. Component Responsibilities

### Header
Shows the brand and main navigation, with a mobile-friendly layout.

### OpportunityCard
Receives a listing object and displays title, company, type, location/work mode, summary, and a details link.

### SearchBar
Stores or emits the current query. It searches local data only and supports clearing the query.

### OpportunityFilters
Provides filters based on available sample fields and lets the user reset them.

### StatusBadge
Displays a readable application or listing status. Do not rely on color alone.

### EmptyState
Explains when a list has no results and may provide a link to reset filters or browse other listings.

### Student pages
Show profile information, application records, and the simulated application flow.

### Company pages
Show company sample listings, shared create/edit form, delete confirmation, and illustrative applicant records.

### Admin pages
Show sample metrics and listing review/moderation controls.

## 7. Sample Data Model

### Opportunity
```javascript
{
  id: "opp-001",
  title: "Software Engineering Intern",
  companyName: "Example Technology Ltd.",
  description: "A fictional internship description.",
  responsibilities: ["Assist with frontend tasks", "Work with a mentor"],
  qualifications: ["Basic JavaScript knowledge"],
  type: "Internship",
  category: "Software Development",
  location: "Dhaka",
  workMode: "Hybrid",
  postedDateLabel: "Recently posted",
  status: "Active"
}
```

### Application
```javascript
{
  id: "app-001",
  opportunityId: "opp-001",
  opportunityTitle: "Software Engineering Intern",
  companyName: "Example Technology Ltd.",
  status: "Submitted",
  submittedDateLabel: "Demo date"
}
```

All example data is fictional. IDs should be unique and stable so records can be updated correctly.

## 8. State Management

Use local component state for page-specific controls. If multiple pages need to share edited listings or demo applications, use React Context or a small state provider.

Suggested state groups:
- `opportunities`: sample listings and local edits.
- `applications`: sample applications and demo submissions.
- `studentProfile`: non-sensitive profile fields.
- `demoRole`: selected role for navigation convenience only.
- `filters`: current query, category, type, and work mode.

Do not treat `demoRole` as an authenticated identity or a security permission.

### Optional localStorage
If persistence is useful:
- Store fictional, non-sensitive demo state only.
- Handle missing or malformed stored data.
- Provide a reset-to-sample-data option.
- Never store passwords, secrets, real resumes, or sensitive information.
- Explain that browser storage is local to one browser and does not synchronize between users.

## 9. Core Interaction Flows

### Search and Filter
1. Read query and selected filters.
2. Filter the local opportunities array by fields that exist.
3. Apply the selected sort order.
4. Render the filtered list.
5. Show an empty state when there are no matches.

### Create/Edit Listing
1. Open the shared listing form.
2. Populate existing values when editing.
3. Validate required fields.
4. Create a unique local ID for new listings.
5. Add or replace the listing in client-side state.
6. Display confirmation and return to the list.

### Simulated Application
1. Student opens listing details.
2. Student selects Apply.
3. Validate required form fields.
4. Display a clear demo notice.
5. Optionally add a sample record to local state.
6. Display a simulated confirmation.

No application is sent to an employer.

### Admin Moderation
1. Admin opens sample listings.
2. Selects a review or remove action.
3. Confirms destructive actions.
4. Update local state.
5. Display the outcome.

## 10. UI and Responsive Design
- Use consistent typography, spacing, and button styles.
- Keep search and filters easy to locate.
- Use responsive grids for listing cards.
- Adapt tables for small screens using card layouts or horizontal scrolling.
- Ensure forms and controls fit mobile widths.
- Use semantic links and buttons.
- Provide visible keyboard focus.
- Include labels, validation messages, and useful empty states.
- Provide alt text for meaningful images.

## 11. Validation and Error Handling
- Require essential listing and application fields.
- Trim whitespace before validation.
- Validate any numeric fields if introduced.
- Display field-level errors.
- Prevent invalid forms from saving.
- Show a not-found page for unknown listing IDs.
- Handle empty catalog, applications, and applicant lists.
- Ask for confirmation before destructive demo actions.
- Display success messages only after the local action succeeds.

## 12. Security and Privacy Limitations
This is an educational frontend prototype:
- Demo login is not real authentication.
- Client-side navigation does not enforce permissions.
- Sample records can be inspected or changed in the browser.
- localStorage is not secure storage.
- No real applications or notifications are sent.
- Do not use real student or employer information.

A production system would require a backend, database, secure authentication, server-side authorization, server-side validation, safe file handling, and privacy controls.

## 13. Testing Strategy
### Functional tests
- Visit every implemented route.
- Search matching and non-matching terms.
- Apply and clear filters.
- Open valid and invalid listing IDs.
- Check each role's demo navigation.
- Submit valid and invalid application forms.
- Create, edit, and delete a listing.
- View illustrative applicants.
- Confirm and cancel admin moderation actions.

### Responsive tests
Check the homepage, catalog, forms, and dashboards at desktop, tablet, and mobile widths. Confirm there is no unwanted horizontal overflow.

### Accessibility tests
Use keyboard-only navigation, check focus visibility, verify form labels, inspect contrast, and ensure status is not indicated by color alone.

### Regression tests
After changes to shared components or state logic, recheck navigation, search, listing updates, application forms, and dashboards.

## 14. GitHub Development Workflow
1. Create an issue describing the task.
2. Create a feature branch.
3. Implement a focused change.
4. Commit with a descriptive message.
5. Push the branch.
6. Open a pull request against `main`.
7. Link the issue using `Closes #ISSUE_NUMBER`.
8. Review and test changed files.
9. Merge when approved.

Suggested branch names:
- `feature/opportunity-catalog`
- `feature/student-dashboard`
- `feature/company-listings`
- `feature/admin-dashboard`
- `docs/project-documentation`

## 15. Setup and Run
For a repository configured with Vite and React, the usual commands are:

```bash
npm install
npm run dev
```

The actual commands depend on `package.json`. Keep the existing project setup unless a change is needed.

## 16. Future Technical Extensions
Future versions may add a backend API, database, secure authentication, resume storage, real application delivery, notifications, messaging, interview scheduling, audit logs, and analytics. None are part of this frontend-only design.

## 17. Conclusion
CareerLink uses a simple frontend architecture, reusable components, local sample data, and client-side state to demonstrate the main workflows for Students, Companies, and Admins. The design avoids database and backend dependencies while clearly documenting that authentication, applications, and moderation are simulations.
