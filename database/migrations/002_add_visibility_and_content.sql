-- Migration 002: Add Visibility Controls and Content Management
-- Created: 2025-11-26
-- Purpose: Add granular visibility controls, file uploads, moderation, and content management

-- ====================
-- GRANULAR VISIBILITY CONTROLS
-- ====================

-- Field-level visibility settings (3 levels: public, lateral_entrants_only, private)
CREATE TABLE IF NOT EXISTS field_visibility_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL, -- Name of the field (e.g., 'email', 'phone', 'achievements')
    visibility_level VARCHAR(50) DEFAULT 'public', -- 'public', 'lateral_entrants_only', 'private'
    updated_by INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE(entrant_id, field_name) -- Each field can only have one visibility setting
);

-- Visibility change audit trail
CREATE TABLE IF NOT EXISTS visibility_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_visibility VARCHAR(50),
    new_visibility VARCHAR(50) NOT NULL,
    changed_by INTEGER NOT NULL,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE CASCADE
);

-- ====================
-- FILE UPLOADS AND MEDIA
-- ====================

-- Photos and documents with moderation
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL, -- User who uploaded
    file_type VARCHAR(50) NOT NULL, -- 'photo', 'document', 'certificate'
    original_filename VARCHAR(255),
    stored_filename VARCHAR(255) NOT NULL, -- UUID-based filename
    file_path TEXT NOT NULL, -- Full path to file
    file_size INTEGER, -- Size in bytes
    mime_type VARCHAR(100),
    width INTEGER, -- For images
    height INTEGER, -- For images
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE, -- Primary profile photo
    moderation_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    moderated_by INTEGER,
    moderated_at TIMESTAMP,
    moderation_notes TEXT,
    is_public BOOLEAN DEFAULT FALSE, -- Only true after approval
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (moderated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Education credentials with verification
CREATE TABLE IF NOT EXISTS education_credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    education_detail_id INTEGER NOT NULL,
    credential_type VARCHAR(100), -- 'degree_certificate', 'transcript', 'award'
    upload_id INTEGER,
    verification_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'verified', 'rejected'
    verified_by INTEGER,
    verified_at TIMESTAMP,
    verification_notes TEXT,
    FOREIGN KEY (education_detail_id) REFERENCES education_details(id) ON DELETE CASCADE,
    FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE SET NULL,
    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ====================
-- PROFILE EDITING AND MODERATION
-- ====================

-- Field edit requests (for admin approval before going live)
CREATE TABLE IF NOT EXISTS field_edit_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    entrant_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL, -- Which field to edit
    current_value TEXT, -- Current value in database
    requested_value TEXT, -- New value requested by user
    change_reason TEXT, -- Optional: why this change
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    reviewed_by INTEGER,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ====================
-- LINKEDIN INTEGRATION
-- ====================

-- LinkedIn OAuth tokens and sync configuration
CREATE TABLE IF NOT EXISTS linkedin_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    entrant_id INTEGER UNIQUE NOT NULL,
    linkedin_profile_url TEXT,
    linkedin_user_id VARCHAR(255), -- LinkedIn unique ID
    access_token TEXT, -- Encrypted LinkedIn OAuth token
    refresh_token TEXT, -- Encrypted refresh token
    token_expires_at TIMESTAMP,
    connection_type VARCHAR(50) DEFAULT 'manual', -- 'oauth', 'manual'
    last_sync_at TIMESTAMP,
    sync_enabled BOOLEAN DEFAULT FALSE,
    field_mappings TEXT, -- JSON: which LinkedIn fields sync to which portal fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE CASCADE
);

-- LinkedIn sync history
CREATE TABLE IF NOT EXISTS linkedin_sync_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    linkedin_connection_id INTEGER NOT NULL,
    sync_status VARCHAR(50) NOT NULL, -- 'success', 'failed', 'partial'
    fields_synced TEXT, -- JSON array of synced fields
    fields_failed TEXT, -- JSON array of failed fields
    error_message TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (linkedin_connection_id) REFERENCES linkedin_connections(id) ON DELETE CASCADE
);

-- ====================
-- AI ASSISTANCE
-- ====================

-- AI-generated content suggestions
CREATE TABLE IF NOT EXISTS ai_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    entrant_id INTEGER,
    content_type VARCHAR(100), -- 'summary', 'achievement', 'education', 'experience'
    input_data TEXT, -- User's raw input/bullet points
    generated_content TEXT, -- AI's suggestion
    was_accepted BOOLEAN,
    edited_content TEXT, -- User's final version after editing AI suggestion
    model_version VARCHAR(100),
    generation_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE CASCADE
);

-- AI API usage tracking (for rate limiting and billing)
CREATE TABLE IF NOT EXISTS ai_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    request_type VARCHAR(100), -- 'summary', 'achievement', 'improve', 'translate'
    tokens_used INTEGER,
    response_time_ms INTEGER,
    success BOOLEAN,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ====================
-- CONTENT MODERATION
-- ====================

-- Flagged content for review
CREATE TABLE IF NOT EXISTS flagged_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type VARCHAR(50), -- 'upload', 'profile_text', 'achievement', 'comment'
    content_id INTEGER,
    flagged_by INTEGER, -- NULL for automated AI flags
    flag_reason VARCHAR(255),
    flag_type VARCHAR(50), -- 'inappropriate', 'inaccurate', 'spam', 'duplicate'
    ai_confidence_score FLOAT, -- 0-1 if flagged by AI
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'reviewed', 'approved', 'removed'
    reviewed_by INTEGER,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flagged_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ====================
-- INDEXES FOR PERFORMANCE
-- ====================

-- Visibility settings lookups
CREATE INDEX IF NOT EXISTS idx_visibility_entrant_id ON field_visibility_settings(entrant_id);
CREATE INDEX IF NOT EXISTS idx_visibility_field_name ON field_visibility_settings(field_name);
CREATE INDEX IF NOT EXISTS idx_visibility_audit_entrant ON visibility_audit(entrant_id);

-- Upload queries
CREATE INDEX IF NOT EXISTS idx_uploads_entrant_id ON uploads(entrant_id);
CREATE INDEX IF NOT EXISTS idx_uploads_status ON uploads(moderation_status);
CREATE INDEX IF NOT EXISTS idx_uploads_type ON uploads(file_type);
CREATE INDEX IF NOT EXISTS idx_uploads_uploaded_by ON uploads(uploaded_by);

-- Edit requests moderation
CREATE INDEX IF NOT EXISTS idx_edit_requests_status ON field_edit_requests(status);
CREATE INDEX IF NOT EXISTS idx_edit_requests_entrant ON field_edit_requests(entrant_id);
CREATE INDEX IF NOT EXISTS idx_edit_requests_user ON field_edit_requests(user_id);

-- LinkedIn integration
CREATE INDEX IF NOT EXISTS idx_linkedin_user_id ON linkedin_connections(user_id);
CREATE INDEX IF NOT EXISTS idx_linkedin_entrant_id ON linkedin_connections(entrant_id);

-- AI suggestions and usage
CREATE INDEX IF NOT EXISTS idx_ai_suggestions_user ON ai_suggestions(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_usage_user_time ON ai_usage(user_id, created_at);

-- Flagged content moderation
CREATE INDEX IF NOT EXISTS idx_flagged_status ON flagged_content(status);
CREATE INDEX IF NOT EXISTS idx_flagged_type ON flagged_content(content_type, content_id);

-- ====================
-- DEFAULT VISIBILITY SETTINGS
-- ====================

-- Create default public visibility for all existing entrants
-- This ensures backward compatibility (all data remains public by default)

INSERT OR IGNORE INTO field_visibility_settings (entrant_id, field_name, visibility_level)
SELECT
    id as entrant_id,
    field_name,
    'public' as visibility_level
FROM
    lateral_entrants
CROSS JOIN (
    SELECT 'name' as field_name UNION ALL
    SELECT 'position' UNION ALL
    SELECT 'department' UNION ALL
    SELECT 'ministry' UNION ALL
    SELECT 'profile_summary' UNION ALL
    SELECT 'educational_background' UNION ALL
    SELECT 'previous_experience' UNION ALL
    SELECT 'email' UNION ALL
    SELECT 'phone' UNION ALL
    SELECT 'achievements'
);

-- ====================
-- MIGRATION COMPLETE
-- ====================
-- Run this migration with:
-- sqlite3 database/lateral_entry.db < database/migrations/002_add_visibility_and_content.sql
