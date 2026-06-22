# Draft Together

A learning project for building real-time applications with **Django**, **Django Channels**, **Daphne (ASGI)**, **Redis**, and **PostgreSQL**.

## Stack

| | |
|---|---|
| ASGI server | Daphne 4 |
| Framework | Django 5 |
| WebSockets | Django Channels 4 |
| Channel layer | Redis 7 |
| Database | PostgreSQL 16 |
| Container base | python:3.12-alpine |

## Quick start

```bash
# 1. Copy env file
cp .env.example .env

# 2. Build and start
docker compose up --build
```

The app is available at `http://localhost:8000`.

On every start the container runs `migrate` automatically before Daphne starts (see `entrypoint.sh`).

## Development (live reload)

Docker Compose Watch syncs local file changes into the running container without a rebuild:

```bash
docker compose watch
```

Edit any Python file and Daphne reloads. No manual restart needed.

## Common commands

```bash
# View logs
docker compose logs -f web

# Open a Django shell inside the container
docker compose exec web python manage.py shell

# Create a superuser
docker compose exec web python manage.py createsuperuser

# Run a one-off management command
docker compose exec web python manage.py <command>

# Stop everything
docker compose down

# Stop and delete volumes (wipes DB + Redis data)
docker compose down -v
```

## Project layout

```
draft_together/
├── config/
│   ├── asgi.py        # ASGI entrypoint — ProtocolTypeRouter
│   ├── settings.py    # All config via environment variables
│   ├── urls.py
│   └── wsgi.py
├── entrypoint.sh      # migrate → daphne start
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Environment variables

All variables are read from `.env` (copy from `.env.example`).

| Variable | Default | Notes |
|---|---|---|
| `SECRET_KEY` | insecure placeholder | Change in production |
| `DEBUG` | `True` | Set `False` in production |
| `ALLOWED_HOSTS` | `localhost 127.0.0.1 0.0.0.0` | Space-separated |
| `POSTGRES_DB` | `draft_together` | |
| `POSTGRES_USER` | `draft_user` | |
| `POSTGRES_PASSWORD` | `draft_pass` | |
| `POSTGRES_HOST` | `db` | Service name in Compose |
| `POSTGRES_PORT` | `5432` | |
| `REDIS_HOST` | `redis` | Service name in Compose |
| `REDIS_PORT` | `6379` | |

## How the pieces connect

```
Browser
  │
  │  HTTP  ──▶  Daphne ──▶ Django (WSGI-style handlers)
  │  WS    ──▶  Daphne ──▶ Django Channels ──▶ Consumer
  │                                                │
  │                                           Redis (channel layer)
  │                                           broadcasts to all
  │                                           connected clients
  │
  └── Django ORM ──▶ PostgreSQL (persistent storage)
```
