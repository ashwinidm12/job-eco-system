<<<<<<< HEAD
# Job Eco System

AI-powered job aggregation and career platform (React + FastAPI + MongoDB).

## Phase 1: Authentication + User Session + Protected Dashboard ✅

### What’s included

- **Backend**
  - JWT-based auth: login returns an access token; register creates a user with hashed password.
  - Protected routes: `/jobs` and `/me` require `Authorization: Bearer <token>`.
  - Pydantic models for register/login and token response.
  - `auth.py`: create/verify JWT, `get_current_user` dependency.
  - `config.py`: `MONGODB_URI`, `JWT_SECRET` from env (with dev defaults).

- **Frontend**
  - Login/Register forms call backend `/login` and `/register`.
  - On success, token and user stored in `localStorage`; dashboard loads.
  - All authenticated requests use `authFetch()` (adds `Authorization` header).
  - On 401, token/user are cleared and user is sent back to login.
  - Navbar shows user email and **Logout** (clears session).

### How to run

1. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt   # or use project venv
   # Optional: copy .env.example to .env and set MONGODB_URI, JWT_SECRET
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Uses `proxy` in `package.json` so API calls go to `http://localhost:8000`.

3. **Database**
   - Set `MONGODB_URI` in `.env` (e.g. MongoDB Atlas connection string).
   - Default is `mongodb://localhost:27017` if not set.

### Usage

- **Register**: Create account (email + password). Then log in.
- **Login**: Submit email/password; backend returns JWT; frontend stores it and shows the job dashboard.
- **Dashboard**: Lists jobs from Remotive API; filters by title, location, company. Requires valid token.
- **Logout**: Clears token and user; next request to `/jobs` would get 401 and redirect to login.

### API (Phase 1)

| Method | Path      | Auth   | Description                |
|--------|-----------|--------|----------------------------|
| POST   | /register | No     | Create user                |
| POST   | /login    | No     | Login; returns JWT         |
| GET    | /me       | Bearer | Current user profile       |
| GET    | /jobs     | Bearer | Live jobs (protected)      |

### Project layout (Phase 1)

```
job-eco-system/
├── backend/
│   ├── api.py          # FastAPI app, routes, DB
│   ├── auth.py         # JWT create/verify, get_current_user
│   ├── config.py       # Settings (MONGODB_URI, JWT_SECRET)
│   ├── models.py       # Pydantic schemas
│   ├── requirements.txt
│   ├── .env.example
│   └── fetch_jobs.py   # (existing) job fetch script
├── frontend/
│   └── src/
│       ├── App.js      # Dashboard, auth state, logout
│       ├── api.js      # authFetch(), getAuthHeader()
│       ├── Login.js    # Register/Login → backend, store token
│       └── ...
└── README.md
```

Next: **Phase 2** – Live job API integration (multiple sources, apply links).
