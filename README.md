# Event Management API

Django REST API for managing events (conferences, meetups, etc.) with user registration.

## Features

- **User Authentication** - JWT-based authentication
- **Event CRUD** - Create, read, update, delete events
- **Event Registration** - Users can register/unregister for events
- **Search & Filtering** - Filter events by title, location, date, upcoming
- **Email Notifications** - Email on event registration/unregistration
- **API Documentation** - Swagger/OpenAPI docs (DEBUG mode only)
- **Admin Panel** - Django Unfold admin with search and filters
- **Health Check** - Root endpoint for API status

## Tech Stack

- Django 4.2 + Django REST Framework
- PostgreSQL (Docker) / SQLite (local)
- JWT Authentication (simplejwt)
- drf-spectacular (Swagger)
- Django Unfold (admin)
- NGINX (reverse proxy)
- pytest (testing)
- Black (formatting)

## Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Docker

```bash
# Copy env file and configure
cp .env.example .env

# Build and run (accessible at http://localhost)
docker-compose up --build

# Run migrations (first time)
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Health Check

- `GET /` - API status and version

### Authentication

- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Get JWT tokens
- `POST /api/users/token/refresh/` - Refresh token
- `GET /api/users/me/` - Current user profile

### Events

- `GET /api/events/` - List events (with filtering)
- `POST /api/events/` - Create event (auth required)
- `GET /api/events/{id}/` - Event details
- `PUT/PATCH /api/events/{id}/` - Update event (organizer only)
- `DELETE /api/events/{id}/` - Delete event (organizer only)
- `POST /api/events/{id}/register/` - Register for event
- `DELETE /api/events/{id}/register/` - Unregister from event
- `GET /api/events/{id}/participants/` - List participants

### Documentation (DEBUG=True only)

- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc
- `GET /api/schema/` - OpenAPI schema

## Event Filters

- `?title=python` - Filter by title (case-insensitive)
- `?location=kyiv` - Filter by location
- `?date_from=2025-01-01` - Events from date
- `?date_to=2025-12-31` - Events until date
- `?upcoming=true` - Only future events
- `?organizer=1` - Filter by organizer ID
- `?search=conference` - Search in title, description, location
- `?ordering=-date` - Order by date (descending)

## Testing

```bash
# Run all tests
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=apps

# In Docker
docker-compose exec web pytest -v
```

## Code Formatting

```bash
# Format code with Black
black .

# Check without changes
black --check .
```

## Environment Variables

See `.env.example` for all available options.

Key variables:

- `DEBUG` - Enable debug mode (shows Swagger docs)
- `SECRET_KEY` - Django secret key
- `POSTGRES_*` - Database configuration
- `EMAIL_*` - SMTP email configuration

## Project Structure

```text
├── apps/
│   ├── core/              # Health check, exceptions
│   │   ├── views.py       # HealthCheckView
│   │   └── exceptions.py  # Custom API exceptions
│   ├── users/             # User authentication
│   │   ├── views.py       # Registration, profile
│   │   └── schemas/       # Swagger schemas
│   └── events/            # Event management
│       ├── views.py       # EventViewSet
│       ├── filters.py     # Event filters
│       ├── services.py    # Email notifications
│       └── schemas/       # Swagger schemas
├── config/
│   └── settings/
│       ├── base.py        # Base settings
│       ├── local.py       # SQLite, console email
│       ├── production.py  # PostgreSQL, SMTP
│       └── logging.py     # Logging configuration
├── docs/
│   └── logs/              # Application logs
├── nginx.conf             # NGINX configuration
├── Dockerfile
└── docker-compose.yml
```

## Admin Panel

Access at `/admin/` with superuser credentials.

Features:

- Clickable ID and title/username fields
- Search with help text
- Date hierarchy navigation
- Filters for all models
