-- Migration 001: Add Authentication System
-- Created: 2025-11-26
-- Purpose: Add user authentication, sessions, and admin management tables

-- ====================
-- USER AUTHENTICATION
-- ====================

-- User accounts for appointees and admins
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER UNIQUE, -- Links to lateral_entrants table (NULL for admins)
    google_id VARCHAR(255) UNIQUE NOT NULL, -- Google account ID from OAuth
    email VARCHAR(255) UNIQUE NOT NULL, -- Email from Google account
    name VARCHAR(255), -- Full name from Google account
    picture_url TEXT, -- Google profile picture URL
    role VARCHAR(50) DEFAULT 'appointee', -- 'appointee' or 'admin'
    is_approved BOOLEAN DEFAULT FALSE, -- Admin approval required
    is_active BOOLEAN DEFAULT TRUE, -- Can be deactivated by admin
    approved_by INTEGER, -- Admin who approved this user
    approved_at TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Pending user access requests (before admin approval)
CREATE TABLE IF NOT EXISTS pending_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    picture_url TEXT,
    request_notes TEXT, -- User can explain who they are
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Active user sessions
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) PRIMARY KEY, -- Random session ID
    user_id INTEGER NOT NULL,
    google_access_token TEXT, -- OAuth access token (encrypted)
    google_refresh_token TEXT, -- OAuth refresh token (encrypted)
    ip_address VARCHAR(45), -- IPv4 or IPv6
    user_agent TEXT, -- Browser user agent string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL, -- Session expiry time (7 days default)
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ====================
-- ADMIN CONFIGURATION
-- ====================

-- Admin configurable settings
CREATE TABLE IF NOT EXISTS admin_settings (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT NOT NULL,
    value_type VARCHAR(50) DEFAULT 'string', -- 'string', 'int', 'float', 'bool', 'json'
    description TEXT,
    updated_by INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Audit log for all important actions
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL, -- 'create', 'update', 'delete', 'upload', 'approve', 'reject', 'login', 'logout'
    entity_type VARCHAR(50) NOT NULL, -- 'profile', 'photo', 'achievement', 'user', 'session', etc.
    entity_id INTEGER,
    old_value TEXT, -- JSON representation of old state
    new_value TEXT, -- JSON representation of new state
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ====================
-- INDEXES FOR PERFORMANCE
-- ====================

-- User lookups
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_entrant_id ON users(entrant_id);
CREATE INDEX IF NOT EXISTS idx_users_role_approved ON users(role, is_approved, is_active);

-- Session lookups
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);

-- Audit log queries
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_entity ON audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);

-- ====================
-- DEFAULT ADMIN SETTINGS
-- ====================

-- Word limits for text fields
INSERT OR IGNORE INTO admin_settings (key, value, value_type, description) VALUES
    ('word_limit_profile_summary', '200', 'int', 'Maximum words for profile summary field'),
    ('word_limit_professional_experience', '150', 'int', 'Maximum words for professional experience field'),
    ('word_limit_achievement_description', '100', 'int', 'Maximum words for achievement description field'),
    ('word_limit_education_description', '75', 'int', 'Maximum words for education description field'),
    ('word_limit_contact_info_note', '50', 'int', 'Maximum words for contact info note field'),
    ('word_limit_social_media_bio', '30', 'int', 'Maximum words for social media bio field');

-- Moderation settings
INSERT OR IGNORE INTO admin_settings (key, value, value_type, description) VALUES
    ('moderation_require_upload_approval', 'true', 'bool', 'Require admin approval for file uploads'),
    ('moderation_require_text_approval', 'true', 'bool', 'Require admin approval for text field edits'),
    ('moderation_auto_approve_minor_edits', 'false', 'bool', 'Auto-approve typo fixes and minor edits'),
    ('moderation_flag_threshold_score', '0.7', 'float', 'AI flagging threshold (0-1)'),
    ('moderation_admin_notification_email', 'true', 'bool', 'Send email notifications for new content'),
    ('moderation_daily_digest_enabled', 'true', 'bool', 'Send daily digest of pending items');

-- File upload limits
INSERT OR IGNORE INTO admin_settings (key, value, value_type, description) VALUES
    ('file_max_photo_size_mb', '5', 'int', 'Maximum photo size in megabytes'),
    ('file_max_document_size_mb', '10', 'int', 'Maximum document size in megabytes'),
    ('file_max_photos_per_profile', '10', 'int', 'Maximum photos per profile'),
    ('file_max_documents_per_profile', '5', 'int', 'Maximum documents per profile'),
    ('file_total_storage_per_user_mb', '100', 'int', 'Total storage quota per user in megabytes');

-- AI assistance settings
INSERT OR IGNORE INTO admin_settings (key, value, value_type, description) VALUES
    ('ai_enabled', 'true', 'bool', 'Enable AI assistance features'),
    ('ai_requests_per_user_per_hour', '10', 'int', 'AI requests per user per hour'),
    ('ai_requests_per_user_per_day', '50', 'int', 'AI requests per user per day'),
    ('ai_show_attribution', 'true', 'bool', 'Show AI attribution on suggestions'),
    ('ai_log_suggestions', 'true', 'bool', 'Log AI suggestions for training');

-- ====================
-- EXTEND LATERAL_ENTRANTS TABLE
-- ====================

-- Add new columns to existing lateral_entrants table
-- These track profile claiming and completeness

-- Check if columns exist before adding them
PRAGMA table_info(lateral_entrants);

-- Add profile management columns (will fail silently if already exist)
ALTER TABLE lateral_entrants ADD COLUMN is_profile_claimed BOOLEAN DEFAULT FALSE;
ALTER TABLE lateral_entrants ADD COLUMN profile_completeness INTEGER DEFAULT 0; -- 0-100%
ALTER TABLE lateral_entrants ADD COLUMN profile_views INTEGER DEFAULT 0;
ALTER TABLE lateral_entrants ADD COLUMN last_profile_update TIMESTAMP;
ALTER TABLE lateral_entrants ADD COLUMN ai_generated_summary TEXT; -- AI suggestion
ALTER TABLE lateral_entrants ADD COLUMN custom_summary TEXT; -- User override

-- ====================
-- MIGRATION COMPLETE
-- ====================
-- Run this migration with:
-- sqlite3 database/lateral_entry.db < database/migrations/001_add_authentication.sql
