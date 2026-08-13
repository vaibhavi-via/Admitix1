# Admitix — Vaibhavi's Project

> A workflow system for educational institutions managing applications, counseling, document verification, and admission approvals across multiple programs.

A working React + Vite starter for student ERP-style projects. Every student
clones this same repo, so every project starts from a consistent, working
foundation instead of an empty folder.

**This is Stage 1** of the full starter kit: project setup, routing,
authentication, and the dashboard shell. See "What's next" at the bottom for
the remaining stages (reusable component pack, CRUD template pack, forms &
validation, charts).

## What's included

- Vite + React 19
- React Router DOM (public routes, protected routes, 404)
- Axios instance with auth-token interceptor and centralized error handling
- Auth context (`login`, `logout`, `user`, `isAuthenticated`) with a mock-auth
  mode so students can build UI before the backend's auth endpoint exists
- Dashboard layout: responsive sidebar, navbar with user menu, footer
- Login page, dashboard page, settings placeholder, 404 page
- A `src/features/_template` folder to copy for each new module

## Getting started

```bash
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173. The mock auth is on by default
(`VITE_USE_MOCK_AUTH=true` in `.env`), so any email/password logs you in.

## Folder structure

```
src/
â”œâ”€â”€ api/            # axios instance â€” the only place baseURL/headers are configured
â”œâ”€â”€ components/     # shared UI: Sidebar, Navbar, Footer, LoadingSpinner
â”œâ”€â”€ context/         # AuthContext (auth state used across the app)
â”œâ”€â”€ features/        # one folder per domain module (students, leads, jobs...)
â”‚   â””â”€â”€ _template/    # copy this to start a new module
â”œâ”€â”€ layouts/         # DashboardLayout (protected pages), AuthLayout (login)
â”œâ”€â”€ pages/            # top-level routed pages
â”œâ”€â”€ routes/           # ProtectedRoute guard
â”œâ”€â”€ styles/           # global.css â€” design tokens (colors, spacing, radius)
â””â”€â”€ utils/            # constants.js, shared helpers
```

## Connecting to your FastAPI backend

Edit `.env`:

```
VITE_API_BASE_URL=http://localhost:8000/api
VITE_USE_MOCK_AUTH=false
```

Then in `src/context/AuthContext.jsx`, the real login call is already
written â€” check the field names in `data.access_token` and `data.user`
match your backend's response shape and adjust if needed.

Every feature module's `services.js` should import the shared instance:

```js
import api from '../../api/axios'

export const getStudents = () => api.get('/students')
export const createStudent = (payload) => api.post('/students', payload)
```

Never call `axios` directly inside a feature module â€” always go through
`src/api/axios.js` so the auth token and error handling stay consistent
across all 19 projects.

## Adding a new module

1. Copy `src/features/_template` â†’ `src/features/<your-module>`.
2. Build out `pages/`, `components/`, and `services.js` inside it.
3. Add its routes inside the `<ProtectedRoute>` block in `src/App.jsx`.
4. Add a link to it in `NAV_ITEMS` in `src/components/Sidebar.jsx`.

No changes to the layout, auth, or routing infrastructure are needed â€”
that's the point of the shared starter.

## Coding standards

- Components: PascalCase filenames (`StudentTable.jsx`)
- Hooks: camelCase, prefixed with `use` (`useStudents.js`)
- One component per file; keep feature-specific components inside that
  feature's `components/` folder, not the shared `src/components/`
- Shared, cross-feature components only go in `src/components/`
- Keep API calls out of components â€” always go through a module's
  `services.js`

## What's next

This repo covers project setup, routing, and auth. The remaining packs
(deliver as separate, incremental updates to this same repo so it keeps
compiling at every stage):

1. âœ… Starter Kit â€” Vite, routing, axios, auth, layout (this stage)
2. Reusable Components Pack â€” Modal, DataTable, Badge, EmptyState, ErrorState
3. CRUD Template Pack â€” List/Create/Edit/Details pages wired to a real module
4. Forms & Validation Pack â€” React Hook Form + Zod
5. Charts & Reports Pack
6. Final production starter â€” polish pass + submission checklist
