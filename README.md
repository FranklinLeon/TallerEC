# 🏍️ TallerEC

> Plataforma PWA + microservicios para la gestión integral de talleres de motos, con IA para transcripción de voz y lectura de placas, y notificaciones automáticas por WhatsApp. Pensada para el mercado latinoamericano (Ecuador).

<p align="left">
  <img alt="Vue" src="https://img.shields.io/badge/Vue_3-35495E?logo=vuedotjs&logoColor=4FC08D">
  <img alt="Vite" src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white">
  <img alt="Tailwind" src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwindcss&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/Django_4.2-092E20?logo=django&logoColor=white">
  <img alt="DRF" src="https://img.shields.io/badge/DRF-A30000?logo=django&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL_15-4169E1?logo=postgresql&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">
</p>

---

## 📖 Descripción

**TallerEC** es un sistema de gestión para talleres de motos. Permite al mecánico llevar el control de las motos en el taller desde su celular, comunicarse con los clientes por WhatsApp **sin que estos instalen ninguna app**, y cobrar con total claridad.

El proyecto integra tres servicios independientes (frontend PWA, backend Django y microservicio de IA) orquestados con Docker Compose, e incorpora capacidades de IA para acelerar el trabajo diario del mecánico.

### Diferenciador clave
El cliente **no instala nada**. Todo el flujo de cotización, aprobación y aviso de entrega ocurre por WhatsApp — el canal que el cliente ya usa — con botones interactivos que el taller configura una sola vez. El seguimiento se hace por un enlace público único (UUID no adivinable), sin login.

---

## ✨ Funcionalidades

| Módulo | Descripción |
|---|---|
| **Ingreso de motos** | Registro de cliente, placa y modelo. Envía automáticamente un WhatsApp de confirmación al cliente. |
| **Lectura de placa (OCR)** | Escanea la placa con la cámara del celular usando Google Cloud Vision. |
| **Tablero Kanban** | Vista principal con columnas *En Taller* y *Lista para entrega*; entrega registrando el monto cobrado. |
| **Muro de actividad** | Timeline por moto con fotos, notas de voz, tareas y cotizaciones. |
| **Notas de voz con IA** | El mecánico graba un audio → se transcribe con **Whisper** → **GPT-4o-mini** genera automáticamente una checklist de tareas. |
| **Cotizaciones por WhatsApp** | Se envían al cliente, que aprueba o rechaza respondiendo con botones interactivos. |
| **Seguimiento del cliente** | Enlace público único (sin login) donde el cliente ve el estado, fotos y detalle del trabajo. |
| **Historial y métricas** | Búsqueda de motos entregadas, facturación mensual, motos activas y motos "estancadas". |

---

## 🏗️ Arquitectura

```
┌──────────────┐      REST/JWT       ┌──────────────┐      HTTP interno     ┌──────────────┐
│  Frontend    │ ──────────────────▶ │   Core       │ ───────────────────▶  │  AI Service  │
│  Vue 3 (PWA) │                     │  Django+DRF  │  (Docker DNS)         │   FastAPI    │
└──────────────┘                     └──────┬───────┘                       └──────┬───────┘
                                            │                                      │
                                     ┌──────▼───────┐                       ┌──────▼───────────────┐
                                     │ PostgreSQL 15│                       │ OpenAI Whisper /GPT   │
                                     └──────────────┘                       │ Google Cloud Vision   │
                                            │                               └───────────────────────┘
                                     ┌──────▼──────────────┐
                                     │ Meta WhatsApp Cloud │
                                     │ API (notificaciones)│
                                     └─────────────────────┘
```

### Servicios y puertos

| Servicio | Stack | Puerto |
|---|---|---|
| `frontend` | Vue 3 + Vite + Tailwind (PWA) | 5173 (dev) / 4173 (preview) |
| `core` | Django 4.2 + DRF + PostgreSQL | 8000 |
| `ai_service` | FastAPI + Uvicorn | 8001 |
| `db` | PostgreSQL 15 | 5432 |

### Modelo de datos

```
Cliente (id, nombre, celular)
  └── Motocicleta (placa, modelo, propietario)
        └── OrdenTrabajo (estado, hash_seguimiento UUID, audio_nota, total_cobro)
              └── EventoMuro (tipo: foto | nota | tarea, contenido, archivo)
```

`OrdenTrabajo.estado`: `taller` · `listo` · `entregado`

---

## 🛠️ Stack tecnológico

- **Frontend:** Vue 3 (`<script setup>`), Vite, Tailwind CSS, PWA instalable (`vite-plugin-pwa`)
- **Backend:** Django 4.2, Django REST Framework, autenticación JWT
- **Microservicio IA:** FastAPI + Uvicorn
- **Base de datos:** PostgreSQL 15
- **IA / APIs externas:** OpenAI (Whisper + GPT-4o-mini), Google Cloud Vision, Meta WhatsApp Cloud API
- **Infraestructura:** Docker & Docker Compose

---

## 🚀 Puesta en marcha

### Requisitos
- Docker y Docker Compose
- Node.js 18+ (para el frontend)
- Claves de: OpenAI, Google Cloud Vision y Meta WhatsApp Cloud API

### 1. Clonar y configurar variables de entorno

Copia las plantillas `.env.example` y rellénalas con tus propias claves:

```bash
cp core/.env.example        core/.env
cp ai_service/.env.example  ai_service/.env
cp frontend/.env.example    frontend/.env

# Credenciales de Google Cloud Vision
cp ai_service/google_key.json.example ai_service/google_key.json
```

### 2. Levantar el backend, la IA y la base de datos

```bash
docker-compose up --build

# Migraciones
docker-compose run --rm core python manage.py migrate

# Crear usuario administrador (mecánico)
docker-compose run --rm core python manage.py createsuperuser
```

### 3. Levantar el frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

> En Windows puedes usar el script `iniciar.bat`, que levanta Docker y el frontend en un solo paso.

---

## 🔌 Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/token/` | Login JWT (mecánicos) |
| `POST` | `/api/motos/registrar/` | Ingreso de cliente + notificación WhatsApp |
| `POST` | `/api/motos/escanear/` | OCR de placa (Google Vision) |
| `POST` | `/api/muro/audio/` | Nota de voz → transcripción → checklist con IA |
| `GET`  | `/api/seguimiento/<uuid>/` | Seguimiento público del cliente (sin auth) |

El router estándar de DRF expone CRUD para `clientes`, `motocicletas`, `ordenes` y `eventos`.

---

## 🔒 Modelo de seguridad

- Los **mecánicos** se autentican con JWT (7 días de vigencia de acceso, 14 de refresco).
- Los **clientes** acceden a su orden mediante un **UUID aleatorio**, que evita la enumeración de órdenes.
- `/api/seguimiento/<uuid>/` es el **único** endpoint público (`AllowAny`).
- Todas las credenciales viven en archivos `.env` fuera del control de versiones.
