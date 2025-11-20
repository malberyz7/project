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
#road to $$$