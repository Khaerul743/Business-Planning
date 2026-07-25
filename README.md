# Business Planning AI & WhatsApp CS Platform

A multi-service platform featuring Next.js frontend dashboard, FastAPI backend API with Redis background queue workers, LangGraph AI agent service, and WhatsApp Web gateway bridge.

## Architecture

- **Frontend**: Next.js 14+ (Port 3000)
- **Backend API**: FastAPI (Port 8000)
- **Generator Worker**: Python Redis Queue Worker
- **Message Worker**: Python Redis Queue Worker
- **Agent Service**: LangGraph AI Agent Server (Port 2024)
- **WA Bridge**: Express + WhatsApp Web JS Gateway (Port 3001)
- **Redis**: Redis 7 Queue & Cache (Port 6379)

---

## Prerequisites

Ensure your system has the following installed:
- [Git](https://git-scm.com/)
- [Docker Engine & Docker Compose](https://docs.docker.com/get-docker/) (or Docker Desktop)

---

## Quick Start Guide

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd project_wa
```

### 2. Configure Environment Variables

Each service requires its `.env` file. You can create them based on template templates or copy from `.env.example`:

#### Backend API (`backend/apps/api/.env`)
Create `backend/apps/api/.env` with:
```env
SECRET_KEY=your_secret_key
WABA_VERIFY_TOKEN=aigear_secret_2025
WABA_ACCESS_TOKEN=your_waba_token
PHONE_NUMBER_ID=your_phone_id

REDIS_HOST=redis
REDIS_PORT=6379

SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_key
OPENAI_API_KEY=sk-proj-your_openai_key
CHROMADB_PATH=chromadb

WA_WEB_SERVICE=http://wa-bridge:3001
LANGGRAPH_SERVER=http://agent-service:2024
```

#### Agent Service (`backend/apps/agent/.env`)
Create `backend/apps/agent/.env` with:
```env
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_key
BACKEND_URL=http://backend-api:8000
```

#### WA Bridge (`backend/apps/wa-bridge/.env`)
Create `backend/apps/wa-bridge/.env` with:
```env
PORT=3001
NODE_ENV=production
FASTAPI_URL=http://backend-api:8000
SESSION_PATH=.wwebjs_auth
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
```

#### Frontend (`frontend/.env`)
Create `frontend/.env` with:
```env
BACKEND_SERVICE_URL=http://backend-api:8000
NEXT_PUBLIC_BACKEND_SERVICE_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

### 3. Build & Run Containers

Run Docker Compose to build images and launch all services in detached mode:

```bash
docker compose up -d --build
```

---

### 4. Access the Application

Once all containers are running (`docker compose ps`), access the services via browser:

- 🌐 **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- ⚡ **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 🤖 **LangGraph Agent Server**: [http://localhost:2024](http://localhost:2024)
- 📱 **WA Bridge Gateway**: [http://localhost:3001/api/health](http://localhost:3001/api/health)

---

## Useful Commands

```bash
# View live logs for all containers
docker compose logs -f

# View live logs for a specific service (e.g., wa-bridge)
docker compose logs -f wa-bridge

# Stop all services
docker compose down

# Stop services and remove persistent volumes (fresh reset)
docker compose down -v
```
