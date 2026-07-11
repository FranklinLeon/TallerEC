# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**MotoFlow** is a PWA + microservices platform for motorcycle repair shops. It combines a Vue 3 frontend, a Django REST API backend, and a FastAPI AI microservice. The target market is Latin America (Spanish UI, Ecuador-specific phone formats).

## Services & Ports

| Service | Stack | Port |
|---|---|---|
| `frontend` | Vue 3 + Vite + Tailwind (PWA) | 5173 (dev), 4173 (preview) |
| `core` | Django 4.2 + DRF + PostgreSQL | 8000 |
| `ai_service` | FastAPI + Uvicorn | 8001 |
| `db` | PostgreSQL 15 | 5432 |

## Commands

### Frontend (`frontend/`)
```bash
npm run dev       # Dev server with hot reload
npm run build     # Production build → dist/
npm run preview   # Preview production build
```

### Backend & AI (Docker)
```bash
# Start all services
docker-compose up --build

# Database migrations
docker-compose run --rm core python manage.py makemigrations
docker-compose run --rm core python manage.py migrate

# Create admin user
docker-compose run --rm core python manage.py createsuperuser

# Full clean restart
docker-compose down && docker-compose up --build
```

### Django Shell / DB Access
```bash
docker-compose exec core python manage.py shell
docker-compose exec db psql -U admin -d motoflow_db
```

## Architecture

### Data Flow
- Frontend (Vue) → Django REST API → PostgreSQL
- Django → AI Service via internal Docker DNS (`http://ai_service:8001/`)
- Django → Meta WhatsApp Cloud API (customer notifications)

### Core Data Models (`core/motoflow_core/models.py`)
```
Cliente (id, nombre, celular unique)
  └── Motocicleta (placa unique, modelo, propietario FK)
        └── OrdenTrabajo (moto FK, estado, hash_seguimiento UUID, audio_nota, total_cobro)
              └── EventoMuro (orden FK, tipo, contenido_texto, archivo, completada)
```

`OrdenTrabajo.estado` values: `'taller'` | `'listo'` | `'entregado'`

`EventoMuro.tipo` values: `'foto'` | `'nota'` | `'tarea'`

### Key API Endpoints (`core/motoflow_core/urls.py`)
- `POST /api/token/` — JWT login (mechanics only)
- `POST /api/motos/registrar/` — Customer intake + WhatsApp notification
- `POST /api/muro/audio/` — Voice note → Whisper transcription → GPT checklist
- `GET /api/seguimiento/<uuid>/` — Public customer tracking (no auth)
- `POST /api/motos/escanear/` — License plate OCR via Google Vision

Standard DRF router provides CRUD for: `clientes`, `motocicletas`, `ordenes`, `eventos`

### AI Service Endpoints (`ai_service/main.py`)
- FastAPI handles audio transcription (OpenAI Whisper) and OCR (Google Cloud Vision)
- Called internally by Django, not directly by the frontend

### Frontend Routing (`frontend/src/router.js`)
- Auth guard on all routes except `/seguimiento/:hash`
- JWT token stored in `localStorage`
- JWT lifetime: 7-day access, 14-day refresh (configured in Django settings)

### Security Model
- Mechanics authenticate with JWT
- Customers access their work order via a random UUID hash (prevents enumeration)
- `/api/seguimiento/<uuid>/` is `AllowAny` — the only public Django endpoint

## External APIs Required

| API | Used For | Credentials |
|---|---|---|
| OpenAI (Whisper + GPT-4o-mini) | Voice transcription + checklist generation | `ai_service/.env` |
| Google Cloud Vision | License plate OCR | `ai_service/google_key.json` |
| Meta WhatsApp Cloud API | Customer SMS-style notifications | `core/.env` |

## Environment Files

- `core/.env` — Django secret key, DB credentials, WhatsApp tokens
- `ai_service/.env` — OpenAI API key
- `ai_service/google_key.json` — Google Cloud service account credentials

CORS in `settings.py` whitelists `localhost:5173`, `localhost:4173`, plus a dev tunnel URL (update if the tunnel URL changes).
