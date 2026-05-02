# CS2 Stat Clash

A web app that compares Counter-Strike 2 player stats using Steam profile URLs and the Leetify Public API. Users paste two Steam profile links and see a side-by-side comparison of key performance metrics.

## What It Does

- Accepts two Steam profile URLs (`/profiles/<steamId64>` or `/id/<customName>`)
- Resolves custom Steam IDs to Steam64 IDs
- Fetches public CS2 stats from the Leetify API
- Compares metrics like win rate, aim, utility, clutch, opening duels, and trade success
- Shows a visual comparison on the frontend
- Stores comparisons locally (SQLite by default)

## Requirements

- Python 3.10+
- Node.js 18+
- (Optional) Leetify API key

## Setup

### 1) Backend

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r backend/requirements.txt
```

Create the env file:

```bash
copy backend\.env.example backend\.env
```

Edit `backend/.env` and set:

- `DATABASE_URL` (default SQLite: `sqlite:///app.db`)
- `LEETIFY_API_KEY` (optional but recommended)

### 2) Frontend

```bash
cd frontend
npm install
```

## Run

### Backend

```bash
python backend/run.py
```

Runs at: http://127.0.0.1:5000

### Frontend

```bash
cd frontend
npm run dev
```

Open: http://localhost:5173

## Notes

- The backend uses Leetify v3 endpoints (`/v3/profile` and `/v3/profile/matches`).
- If you hit rate limits, add a Leetify API key in `backend/.env`.
- SQLite is used by default for easy local testing.

## API Endpoints

- `POST /api/compare` - compare two players
- `GET /api/comparisons` - recent comparisons
- `GET /api/comparisons/<id>` - comparison by id
- `GET /api/players/<steamId>` - cached player info
