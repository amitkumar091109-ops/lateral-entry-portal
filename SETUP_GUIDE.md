# Setup Guide: Lateral Entry Officers Database

## 🚀 Quick Start

This guide will help you set up the development environment and run the platform.

---

## Prerequisites

- Python 3.9 or higher
- SQLite3
- Git

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/amitkumar091109-ops/lateral-entry-portal.git
cd lateral-entry-portal
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your configuration
nano .env
```

**Required Configuration**:
```bash
# Generate secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Generate token encryption key
TOKEN_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# Google OAuth (get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

### 4. Initialize Database

The database migrations have already been applied. To verify:

```bash
python database/run_migrations.py
```

Expected output:
```
✅ Successfully applied migrations
📊 Total tables in database: 39
```

---

## Running the Application

### Development Mode

```bash
# Start Flask API server
python api/server.py
```

The API will be available at `http://localhost:5000`

### Static Frontend

Open `index.html` in your browser, or serve with a simple HTTP server:

```bash
# Using Python
python -m http.server 8000

# Then visit http://localhost:8000
```

---

## Google OAuth Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API

### 2. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** user type
3. Fill in application details
4. Add scopes: `email`, `profile`, `openid`

### 3. Create OAuth 2.0 Credentials

1. Go to **Credentials** → **Create Credentials** → **OAuth client ID**
2. Application type: **Web application**
3. Authorized redirect URIs:
   - `http://localhost:5000/api/auth/google/callback` (development)
   - `https://your-domain.com/api/auth/google/callback` (production)
4. Copy **Client ID** and **Client Secret** to `.env`

---

## Database Schema

The database has been migrated with 39 tables organized into:

**Authentication & Users**:
- `users` - User accounts
- `pending_users` - Pending approvals
- `sessions` - Active sessions
- `admin_settings` - Configurable settings (22 defaults)
- `audit_log` - Action tracking

**Visibility & Privacy**:
- `field_visibility_settings` - 3-level permissions (Public/Lateral Entrants Only/Private)
- `visibility_audit` - Visibility change history

**Content Management**:
- `uploads` - Photos and documents
- `field_edit_requests` - Moderation queue
- `flagged_content` - Content moderation

**LinkedIn Integration**:
- `linkedin_connections` - OAuth connections
- `linkedin_sync_history` - Sync tracking

**AI Assistance**:
- `ai_suggestions` - AI-generated content
- `ai_usage` - API usage tracking

**Job Monitoring**:
- `job_listings` - AI-discovered jobs
- `user_job_preferences` - Job matching preferences
- `saved_jobs` - Bookmarked jobs
- `job_monitoring_config` - Parallel AI configuration
- `job_domains` - 15 default domains

**Social & News**:
- `social_feed_items` - Social media posts
- `news_articles` - News monitoring

---

## Current Implementation Status

✅ **Phase 0: Project Rebranding** (100% Complete)
- Updated all branding and clarification messaging
- 22 files modified

✅ **Phase 1: Database Schema** (100% Complete)
- 3 migrations created and applied
- 39 tables with 650+ default settings

🚧 **Phase 1: Authentication** (80% Complete)
- ✅ Google OAuth service (`api/auth/google_oauth.py`)
- ✅ Session management (`api/auth/session_manager.py`)
- ✅ Token encryption (`api/auth/token_encryption.py`)
- ✅ Authentication decorators (`api/auth/decorators.py`)
- ⏳ Authentication routes (TO DO)
- ⏳ Flask server (TO DO)
- ⏳ Frontend login UI (TO DO)

📋 **Phases 2-12** (Not Started)
- Comprehensive scaffolding in place
- Database ready
- See `IMPLEMENTATION_STATUS.md` for details

---

## Next Steps

### Immediate (Complete Phase 1)

1. **Create Authentication Routes** (`api/routes/auth_routes.py`)
2. **Create Flask Server** (`api/server.py`)
3. **Create Login Page** (`pages/login.html`)
4. **Test OAuth Flow**

### Phase 2: Admin Panel

1. Create user management APIs
2. Create moderation queue APIs
3. Build admin dashboard UI
4. Implement approval workflow

### Phase 3-12: See Implementation Plan

Refer to:
- `IMPLEMENTATION_STATUS.md` - Detailed progress tracking
- `openspec/changes/add-user-profiles-and-feeds/tasks.md` - Complete task list
- `openspec/changes/add-user-profiles-and-feeds/design.md` - Technical design

---

## Testing

### Run Migrations Test

```bash
python database/run_migrations.py
```

### Test OAuth Service (when complete)

```bash
python -c "from api.auth import google_oauth_service; print(google_oauth_service.get_authorization_url('test'))"
```

---

## Troubleshooting

### Database Errors

```bash
# Check database tables
sqlite3 database/lateral_entry.db ".tables"

# Re-run migrations
python database/run_migrations.py
```

### Google OAuth Errors

- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`
- Check redirect URI matches Google Console
- Ensure Google+ API is enabled

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

---

## Production Deployment

See `DEPLOYMENT_GUIDE.md` for production setup instructions.

**Key considerations**:
- Set `FLASK_ENV=production`
- Set `SESSION_COOKIE_SECURE=True`
- Use HTTPS
- Configure proper secret keys
- Set up database backups
- Configure firewall rules

---

## Documentation

- **Implementation Status**: `IMPLEMENTATION_STATUS.md`
- **API Documentation**: `docs/API.md` (TO CREATE)
- **User Guide**: `docs/USER_GUIDE.md` (TO CREATE)
- **Admin Manual**: `docs/ADMIN_MANUAL.md` (TO CREATE)

---

## Support

For issues or questions:
1. Check `IMPLEMENTATION_STATUS.md`
2. Review OpenSpec documentation in `openspec/`
3. Check GitHub issues

---

## License

See `LICENSE` file for details.
