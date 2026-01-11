# OctoFit Tracker - GitHub Copilot Instructions

**Project**: Fitness tracking application for Mergington High School built with GitHub Copilot agent mode.
**Stack**: Python Django (backend), React (frontend), MongoDB (database)
**Deployment**: GitHub Codespaces

## Architecture Overview

### Multi-Tier Application Structure
```
octofit-tracker/
├── backend/                           # Django REST API
│   ├── venv/                          # Python virtual environment
│   ├── octofit_tracker/               # Django project directory
│   │   ├── manage.py
│   │   ├── settings.py               # Django configuration
│   │   ├── urls.py                   # API routing
│   │   └── [apps]/                   # Django apps (models, serializers, views)
│   └── requirements.txt               # Python dependencies
└── frontend/                          # React SPA
    └── src/                           # React components
```

### Key Service Boundaries
- **Backend (Port 8000)**: Django REST API with MongoDB integration via Djongo ORM
- **Frontend (Port 3000)**: React app consuming backend APIs
- **Database (Port 27017)**: MongoDB with database name `octofit_db`
- **Environment-aware URLs**: Uses `CODESPACE_NAME` environment variable for GitHub Codespaces compatibility

## Critical Developer Workflows

### Backend Startup
1. **Activate virtual environment**: `source octofit-tracker/backend/venv/bin/activate`
2. **Install dependencies**: `pip install -r octofit-tracker/backend/requirements.txt`
3. **Run migrations**: `python manage.py migrate` (from project root, not inside backend/)
4. **Start server**: Use `.vscode/launch.json` "Launch Django Backend" configuration (binds to `0.0.0.0:8000`)

### Frontend Startup
- Use `.vscode/launch.json` "Launch React Frontend" configuration
- React app runs at `http://localhost:3000` locally or `https://<CODESPACE_NAME>-3000.app.github.dev` in Codespaces

### Database Management
- MongoDB starts automatically in Codespaces (installed in `post_create.sh`)
- **Never use direct MongoDB scripts** - always use Django ORM via Django management commands
- Example: Create population command at `octofit-tracker/backend/octofit_tracker/management/commands/populate_db.py`
- Verify with: `mongosh` (official client tool, not `mongo`)

### Testing Endpoints
- Use `curl` to test REST API endpoints from terminal
- Backend provides API root at `/api/` with routing for all models

## Project-Specific Conventions

### Never Change Directories in Commands
- **Critical rule**: When using agent mode, NEVER `cd` into subdirectories
- Always use full paths: `python octofit-tracker/backend/manage.py migrate` not `cd backend && python manage.py migrate`
- This ensures commands work consistently in Codespaces environment

### Port Forwarding Rules
- **Port 8000** (Django): Public access
- **Port 3000** (React): Public access  
- **Port 27017** (MongoDB): Private (do not propose other ports)

### Settings.py Configuration
Always include Codespaces URL generation:
```python
import os
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if os.environ.get('CODESPACE_NAME'):
    ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")
```

### URLs.py Configuration
Always use environment-aware base URL:
```python
import os
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"
```

### Serializers
- Convert MongoDB `ObjectId` fields to strings in serializers (required for JSON serialization)
- Use Djongo ORM models with DRF serializers

### Frontend Commands
- Always prefix React commands with `--prefix octofit-tracker/frontend`
- Example: `npm install bootstrap --prefix octofit-tracker/frontend`
- Bootstrap CSS import must be at top of `src/index.js`: `import 'bootstrap/dist/css/bootstrap.min.css';`

## Integration Points & Data Flow

### MongoDB → Django → React
1. Django models use Djongo for MongoDB integration (ORM handles `ObjectId`)
2. DRF serializers expose models as REST endpoints at `/api/[resource]/`
3. React components fetch via `fetch()` or axios to backend URLs
4. Frontend respects CORS headers configured in Django settings

### CORS Configuration (Backend)
- Must enable CORS for all origins, methods, and headers in production dev environment
- Configure middleware and add `'*'` to allowed hosts
- Required for Codespaces multi-tier development

### Database Collections (as per populate_db.py)
- **users**: Team member profiles
- **teams**: Team definitions (e.g., "Team Marvel", "Team DC")
- **activities**: User workout logs
- **leaderboard**: Competitive rankings
- **workouts**: Pre-defined workout suggestions

## Key Dependencies & Versions

### Backend (Python)
- Django 4.1.7
- djangorestframework 3.14.0
- Djongo 1.3.6 (MongoDB ORM layer)
- pymongo 3.12
- django-cors-headers 4.5.0
- dj-rest-auth 2.2.6, django-allauth 0.51.0 (authentication)

### Frontend (Node)
- React (via create-react-app)
- react-router-dom (routing)
- Bootstrap (styling)

### Services
- MongoDB 6.0
- Node.js LTS
- Python 3.x with pip/venv

## Development Environment

### Codespaces Configuration
- Base image: `mcr.microsoft.com/devcontainers/base:jammy`
- Extensions: Copilot, Copilot Chat, Python, Pylance, DebugPy, markdown-lint, GitHub CLI
- `post_create.sh`: Installs MongoDB, Python venv tools
- `post_start.sh`: Runs on every container restart

### Launch Configurations (.vscode/launch.json)
- **Launch Django Backend**: Python debugger, `manage.py runserver 0.0.0.0:8000`
- **Launch React Frontend**: Node/npm, `react-scripts start` in frontend directory

## Common Patterns

### Creating Django Apps
1. Structure: One app per feature (e.g., `users`, `activities`, `teams`, `leaderboard`)
2. Use standard Django layout: models.py, serializers.py, views.py, urls.py
3. Register in INSTALLED_APPS in settings.py

### Adding Endpoints
1. Create ViewSet or APIView in views.py
2. Register with DefaultRouter in urls.py
3. Router auto-generates CRUD endpoints at `/api/[resource]/` and `/api/[resource]/{id}/`

### Authentication Flow
- Use dj-rest-auth + django-allauth for user registration/login
- Token-based authentication for API calls

## Tips for AI Agents

- **Always read full requirements** from `.github/instructions/` files before coding
- **Preserve MongoDB indices** (e.g., unique constraint on email field)
- **Test with curl** before implementing frontend integration
- **Use Django management commands** for data population, not raw MongoDB scripts
- **Validate CORS is properly configured** when debugging frontend-backend communication
- **Use full paths** in all terminal commands - never change directories
- **Check environment variables** - Codespaces provides `CODESPACE_NAME` for URL generation
