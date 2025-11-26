# Capability Spec: Google OAuth Authentication

**Feature**: `google-oauth-authentication`  
**Parent Change**: `add-user-profiles-and-feeds`  
**Status**: Draft

## Overview

Implement Google OAuth 2.0 authentication to allow lateral entry appointees to securely sign in using their Google accounts. This eliminates the need for password management while leveraging Google's security infrastructure.

## Requirements

### Functional Requirements

1. **Sign In with Google**:
   - Users click "Sign in with Google" button
   - Redirect to Google OAuth consent screen
   - User authorizes application
   - System receives authorization code
   - Exchange code for access and refresh tokens
   - Extract user information from ID token

2. **Session Management**:
   - Create secure session after successful authentication
   - Store encrypted OAuth tokens in database
   - Set HTTP-only, secure session cookie
   - Validate session on each authenticated request
   - Automatic token refresh when expired
   - Session expiry after 7 days of inactivity

3. **User Registration Flow**:
   - First-time users create pending access request
   - Admin reviews and approves request
   - Admin links Google account to entrant profile
   - Approved users can access editing features

4. **Logout**:
   - Clear session from database
   - Delete session cookie
   - Optionally revoke Google tokens

### Non-Functional Requirements

1. **Security**:
   - CSRF protection using state parameter
   - Encrypted token storage using Fernet encryption
   - HTTP-only, secure cookies
   - Session validation on every request
   - Audit logging of authentication events

2. **Performance**:
   - OAuth flow completes in < 5 seconds
   - Session validation in < 50ms
   - Token refresh in < 2 seconds

3. **Reliability**:
   - Handle Google API failures gracefully
   - Retry logic for transient errors
   - Clear error messages for users

## Technical Specification

### API Endpoints

```
GET  /api/auth/google/login     - Initiate OAuth flow
GET  /api/auth/google/callback  - Handle OAuth callback
POST /api/auth/logout           - End session
GET  /api/auth/me               - Get current user
GET  /api/auth/status           - Check approval status
```

### Database Tables

```sql
-- User accounts
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER UNIQUE,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    picture_url TEXT,
    role VARCHAR(50) DEFAULT 'appointee',
    is_approved BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    approved_by INTEGER,
    approved_at TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Pending user requests
CREATE TABLE pending_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    picture_url TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    request_notes TEXT
);

-- Active sessions
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    google_access_token TEXT,
    google_refresh_token TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Configuration

Required environment variables:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=<user-provides>
GOOGLE_CLIENT_SECRET=<user-provides>
BASE_URL=https://prabhu.app/lateral-entry

# Token encryption
TOKEN_ENCRYPTION_KEY=<generate-with-fernet>

# Session configuration
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
SESSION_LIFETIME_DAYS=7
```

### Dependencies

```python
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
cryptography==41.0.4
```

## User Interface

### Login Page (`pages/login.html`)

```html
<div class="login-container">
    <h1>Lateral Entry Portal</h1>
    <p>Sign in to manage your profile</p>
    
    <button id="google-signin-btn" class="btn-google">
        <img src="/assets/google-icon.svg" alt="Google" />
        Sign in with Google
    </button>
    
    <p class="help-text">
        First time? You'll need admin approval after signing in.
    </p>
</div>
```

### Pending Approval Page

```html
<div class="pending-container">
    <h1>Access Request Submitted</h1>
    <p>Your access request has been submitted for admin review.</p>
    <p>You'll receive an email once your account is approved.</p>
    
    <div class="user-info">
        <img src="<user.picture_url>" alt="Profile" />
        <div>
            <strong><span id="user-name"></span></strong>
            <span id="user-email"></span>
        </div>
    </div>
    
    <button onclick="checkStatus()">Check Status</button>
</div>
```

## Security Considerations

1. **CSRF Protection**: Use cryptographically random state parameter
2. **Token Encryption**: Store OAuth tokens encrypted at rest
3. **Secure Cookies**: HTTP-only, secure, SameSite=Lax
4. **Session Validation**: Check user approval status on every request
5. **Audit Logging**: Log all authentication events
6. **Token Refresh**: Automatic refresh before expiry
7. **IP Tracking**: Store IP address for security monitoring

## Testing Strategy

### Unit Tests

```python
def test_google_oauth_url_generation():
    """Test authorization URL is correctly generated"""
    
def test_token_exchange():
    """Test authorization code exchange for tokens"""
    
def test_user_info_extraction():
    """Test extracting user info from ID token"""
    
def test_session_creation():
    """Test creating session after successful auth"""
    
def test_session_validation():
    """Test validating existing session"""
    
def test_token_encryption():
    """Test token encryption and decryption"""
```

### Integration Tests

```python
def test_oauth_flow_end_to_end():
    """Test complete OAuth flow from login to session"""
    
def test_pending_user_workflow():
    """Test first-time user access request"""
    
def test_approved_user_login():
    """Test approved user can access features"""
    
def test_session_expiry():
    """Test expired sessions are rejected"""
```

## Rollback Plan

If OAuth authentication fails:

1. Disable authentication requirement temporarily
2. Roll back database migrations
3. Restore previous session system (if any)
4. Investigate OAuth configuration issues
5. Fix and redeploy

## Success Criteria

- [ ] Users can successfully sign in with Google
- [ ] Sessions persist for 7 days
- [ ] Token refresh works automatically
- [ ] CSRF protection prevents attacks
- [ ] Audit log captures all auth events
- [ ] Error messages are clear and helpful
- [ ] Performance meets requirements (< 5s OAuth flow)
- [ ] All security measures implemented

## Related Specs

- [Admin User Approval](../admin-panel/user-approval.md)
- [Session Management](./session-management.md)
- [Permission System](./permissions.md)
