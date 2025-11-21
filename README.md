# IELTS Prep Project

This repository contains a small IELTS preparation application with:

- Backend: FastAPI (in `/backend`)
- Frontend: Vite + React (in `/frontend`)

Quick start

1) Backend (Python)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

2) Frontend (Node)

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `/api/*` (same host). When developing locally you can run the backend on port `8000` and configure a proxy in Vite if needed.

If you want, я могу добавить: прокси-конфиг для Vite, Dockerfile, или автозагрузку данных.

Serve built frontend from backend (single-server mode)

1) Build frontend and start backend with one script:

```bash
cd /workspaces/project
./start_all.sh
```

This will run `npm install` and `npm run build` in `frontend`, then start `uvicorn` which will serve the built files from `frontend/dist` together with the `/api` endpoints.

2) Or build and run manually:

```bash
cd /workspaces/project/frontend
npm install
npm run build

# then in project root
cd /workspaces/project
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

After build, opening `http://localhost:8000` will serve the frontend app (index.html) and API remains available at `/api`.
#road to $$$