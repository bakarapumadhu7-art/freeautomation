# ANTIGRAVITY — Creator Referral & Instagram Comment Automation Ecosystem

Enterprise-grade, event-driven Instagram comment automation and creator referral engine structurally inspired by Superprofile and Zorcha. Combines sub-second Gemini NLP intent classification, Claude generative anti-spam DM copy synthesis, dual Meta Graph API / instagrapi fallback adapters, and a strict dark-mode WebGL glassmorphic interface with kinetic typography and zero 2D icons.

---

## Architecture Flow

```
   Follower Comments on Reel / Post
                  │
                  ▼
   [ Flask Webhook Ingestion Route ]
    - X-Hub-Signature-256 HMAC-SHA256 validation
    - Sub-50ms HTTP 200 immediate response
                  │
                  ▼ (Async Offload)
   [ Celery & Redis Distributed Task Queue ]
                  │
                  ├──────────────────────────────┐
                  ▼                              ▼
     [ Gemini NLP Classifier ]        [ Creator Database ]
     - Strict JSON output schema      - Fetch active TriggerKeywords
     - Sub-second intent extraction   - Fetch target DestinationURLs
                  │                              │
                  └──────────────┬───────────────┘
                                 ▼
                 [ Claude Generative DM Engine ]
                 - Bespoke anti-spam copy synthesis
                 - Embeds wrapped referral URL
                                 │
                                 ▼
                 [ Instagram Dispatch Adapter ]
                 - Mode 1: Meta Graph API (Production)
                 - Mode 2: Instagrapi Client (Staging/Dev)
                                 │
                                 ▼
             Follower Receives DM & Clicks Link
                                 │
                                 ▼
             [ Link Tracker Service /r/<code\> ]
             - Click & conversion analytics recorded
             - Real-time CTR streamed to 3D Dashboard
```

---

## Folder Structure

```
antigravity/
├── backend/
│   ├── app/
│   │   ├── __init__.py                # Flask factory and CORS setup
│   │   ├── config.py                  # Environment config and adapter settings
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schema.py              # Creator_Profiles, Media_Objects, Triggers, Destinations
│   │   ├── services/
│   │   │   ├── instagram_adapter.py   # Dual Graph API / instagrapi adapter pattern
│   │   │   ├── ai_orchestrator.py     # Gemini classification & Claude DM synthesis
│   │   │   └── link_tracker.py        # Outbound link-wrapping & CTR metrics
│   │   ├── tasks/
│   │   │   ├── celery_app.py          # Celery/Redis configuration
│   │   │   └── automation_tasks.py    # Async event processing pipeline
│   │   └── webhooks/
│   │       └── routes.py              # GET hub challenge & POST event listener
│   ├── requirements.txt
│   └── wsgi.py
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        └── components/
            ├── ThreeCanvas.jsx         # Global Three.js reactive soft-body & particle scene
            └── GlassDashboard.jsx      # Icon-less glassmorphic UI with 3D micro-geometries
```

---

## Quickstart

### 1. Backend Service

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Redis (Required for Celery)
# docker run -d -p 6379:6379 redis:alpine

# Start Celery Worker
celery -A app.tasks.celery_app.celery_app worker --loglevel=info

# Start Flask Microservice
python wsgi.py
```

### 2. Frontend WebGL Dashboard

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to interact with the 3D dark-mode glassmorphic interface.
