-- Migration 003: Add Comprehensive Job Monitoring System
-- Created: 2025-11-26
-- Purpose: AI-powered job vacancy monitoring across thousands of organizations

-- ====================
-- JOB LISTINGS AND MONITORING
-- ====================

-- Job listings discovered by AI monitoring
CREATE TABLE IF NOT EXISTS job_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title VARCHAR(500) NOT NULL,
    organization_name VARCHAR(255) NOT NULL,
    organization_type VARCHAR(100), -- 'central_govt', 'state_govt', 'psu', 'private', 'autonomous', 'international'
    department VARCHAR(255),
    position_level VARCHAR(100), -- 'joint_secretary', 'director', 'deputy_secretary', 'other'
    location VARCHAR(255),
    job_description TEXT,
    responsibilities TEXT,
    qualifications_required TEXT,
    experience_required VARCHAR(100),
    salary_range VARCHAR(255),
    application_deadline DATE,
    job_url TEXT UNIQUE, -- Original job posting URL
    source_url TEXT, -- Where we found it
    discovered_by VARCHAR(50) DEFAULT 'parallel_ai', -- 'parallel_ai', 'manual', 'rss', 'api'
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    relevance_score FLOAT, -- 0-1, calculated by AI
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    admin_verified BOOLEAN DEFAULT FALSE,
    verified_by INTEGER,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Domains/expertise areas for job matching
CREATE TABLE IF NOT EXISTS job_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_name VARCHAR(100) UNIQUE NOT NULL, -- 'finance', 'technology', 'healthcare', etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Link jobs to domains (many-to-many)
CREATE TABLE IF NOT EXISTS job_domain_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    domain_id INTEGER NOT NULL,
    FOREIGN KEY (job_id) REFERENCES job_listings(id) ON DELETE CASCADE,
    FOREIGN KEY (domain_id) REFERENCES job_domains(id) ON DELETE CASCADE,
    UNIQUE(job_id, domain_id)
);

-- ====================
-- USER JOB PREFERENCES
-- ====================

-- User preferences for job matching and notifications
CREATE TABLE IF NOT EXISTS user_job_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    entrant_id INTEGER UNIQUE,
    preferred_position_levels TEXT, -- JSON array: ['joint_secretary', 'director']
    preferred_domains TEXT, -- JSON array: ['finance', 'technology']
    preferred_locations TEXT, -- JSON array: ['Delhi', 'Mumbai', 'Remote']
    preferred_organization_types TEXT, -- JSON array: ['central_govt', 'psu', 'private']
    min_salary INTEGER,
    max_experience_years INTEGER,
    job_alerts_enabled BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT FALSE,
    weekly_digest BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id) ON DELETE SET NULL
);

-- User saved jobs (bookmarked for later)
CREATE TABLE IF NOT EXISTS saved_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    application_status VARCHAR(50) DEFAULT 'saved', -- 'saved', 'applied', 'interviewing', 'offered', 'rejected', 'withdrawn'
    notes TEXT,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_listings(id) ON DELETE CASCADE,
    UNIQUE(user_id, job_id)
);

-- ====================
-- MONITORING CONFIGURATION
-- ====================

-- Organizations to monitor (configured by admin)
CREATE TABLE IF NOT EXISTS monitored_organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_name VARCHAR(255) NOT NULL,
    organization_type VARCHAR(100), -- 'central_govt', 'state_govt', 'psu', 'private', etc.
    website_url TEXT,
    careers_page_url TEXT,
    monitoring_priority VARCHAR(50) DEFAULT 'medium', -- 'high', 'medium', 'low'
    monitoring_frequency VARCHAR(50) DEFAULT 'daily', -- 'hourly', 'daily', 'weekly'
    is_active BOOLEAN DEFAULT TRUE,
    last_monitored_at TIMESTAMP,
    jobs_found_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Parallel AI monitoring prompts and configuration
CREATE TABLE IF NOT EXISTS job_monitoring_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_name VARCHAR(100) UNIQUE NOT NULL,
    monitoring_prompt TEXT NOT NULL, -- The prompt sent to Parallel AI
    target_organizations TEXT, -- JSON array of organization names
    keywords TEXT, -- JSON array of keywords to search for
    position_levels TEXT, -- JSON array of position levels
    monitoring_schedule VARCHAR(50) DEFAULT 'hourly', -- 'hourly', 'daily', 'weekly'
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP,
    next_run_at TIMESTAMP,
    jobs_discovered_count INTEGER DEFAULT 0,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Job monitoring execution history
CREATE TABLE IF NOT EXISTS job_monitoring_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'running', 'completed', 'failed', 'partial'
    jobs_discovered INTEGER DEFAULT 0,
    jobs_new INTEGER DEFAULT 0,
    jobs_updated INTEGER DEFAULT 0,
    api_requests_made INTEGER DEFAULT 0,
    execution_time_ms INTEGER,
    error_message TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (config_id) REFERENCES job_monitoring_config(id) ON DELETE CASCADE
);

-- ====================
-- JOB NOTIFICATIONS
-- ====================

-- Job notifications sent to users
CREATE TABLE IF NOT EXISTS job_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    notification_type VARCHAR(50) NOT NULL, -- 'new_match', 'deadline_reminder', 'status_update'
    match_score FLOAT, -- 0-1, how well job matches user preferences
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    notification_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_listings(id) ON DELETE CASCADE
);

-- ====================
-- SOCIAL MEDIA AND NEWS FEEDS
-- ====================

-- Social media feed items (optional feature)
CREATE TABLE IF NOT EXISTS social_feed_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform VARCHAR(50) NOT NULL, -- 'twitter', 'facebook', 'linkedin'
    post_id VARCHAR(255) UNIQUE, -- External platform post ID
    author_name VARCHAR(255),
    author_handle VARCHAR(255),
    author_avatar_url TEXT,
    content TEXT,
    url TEXT,
    media_urls TEXT, -- JSON array of media URLs
    engagement_count INTEGER, -- likes + shares + comments
    posted_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_relevant BOOLEAN DEFAULT TRUE,
    relevance_score FLOAT,
    related_entrant_ids TEXT -- JSON array of entrant IDs mentioned
);

-- News articles from Parallel AI monitoring
CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    url TEXT UNIQUE,
    source_name VARCHAR(255),
    author VARCHAR(255),
    summary TEXT,
    content TEXT,
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment VARCHAR(50), -- 'positive', 'neutral', 'negative'
    relevance_score FLOAT,
    related_entrant_ids TEXT, -- JSON array of entrant IDs mentioned
    related_keywords TEXT -- JSON array of keywords
);

-- News monitoring keywords
CREATE TABLE IF NOT EXISTS news_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword VARCHAR(255) NOT NULL,
    keyword_type VARCHAR(50), -- 'entrant_name', 'ministry', 'program'
    related_entrant_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (related_entrant_id) REFERENCES lateral_entrants(id) ON DELETE SET NULL
);

-- ====================
-- INDEXES FOR PERFORMANCE
-- ====================

-- Job listings queries
CREATE INDEX IF NOT EXISTS idx_jobs_organization ON job_listings(organization_name);
CREATE INDEX IF NOT EXISTS idx_jobs_position_level ON job_listings(position_level);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON job_listings(location);
CREATE INDEX IF NOT EXISTS idx_jobs_deadline ON job_listings(application_deadline);
CREATE INDEX IF NOT EXISTS idx_jobs_active ON job_listings(is_active);
CREATE INDEX IF NOT EXISTS idx_jobs_relevance ON job_listings(relevance_score DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_discovered_at ON job_listings(discovered_at DESC);

-- User preferences and saved jobs
CREATE INDEX IF NOT EXISTS idx_user_prefs_user_id ON user_job_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_user ON saved_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_job ON saved_jobs(job_id);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_status ON saved_jobs(application_status);

-- Monitoring organization tracking
CREATE INDEX IF NOT EXISTS idx_monitored_orgs_type ON monitored_organizations(organization_type);
CREATE INDEX IF NOT EXISTS idx_monitored_orgs_active ON monitored_organizations(is_active);
CREATE INDEX IF NOT EXISTS idx_monitored_orgs_priority ON monitored_organizations(monitoring_priority);

-- Job notifications
CREATE INDEX IF NOT EXISTS idx_job_notifs_user_unread ON job_notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_job_notifs_created ON job_notifications(created_at DESC);

-- Social feeds and news
CREATE INDEX IF NOT EXISTS idx_social_platform ON social_feed_items(platform);
CREATE INDEX IF NOT EXISTS idx_social_posted_at ON social_feed_items(posted_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_published_at ON news_articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_relevance ON news_articles(relevance_score DESC);

-- ====================
-- DEFAULT JOB DOMAINS
-- ====================

-- Insert common domains for job matching
INSERT OR IGNORE INTO job_domains (domain_name, description) VALUES
    ('finance', 'Finance, banking, and economic policy'),
    ('technology', 'IT, digital transformation, and cybersecurity'),
    ('healthcare', 'Public health, medical services, and pharmaceuticals'),
    ('education', 'Education policy, skill development, and research'),
    ('infrastructure', 'Infrastructure development, urban planning, and construction'),
    ('energy', 'Energy, renewable energy, and environmental policy'),
    ('agriculture', 'Agriculture, rural development, and food security'),
    ('legal', 'Legal affairs, regulatory compliance, and justice'),
    ('human_resources', 'HR, personnel management, and organizational development'),
    ('public_policy', 'Policy formulation, governance, and administration'),
    ('defense', 'Defense, security, and strategic affairs'),
    ('foreign_affairs', 'International relations and diplomacy'),
    ('commerce', 'Trade, commerce, and industrial policy'),
    ('social_welfare', 'Social justice, welfare programs, and inclusion'),
    ('transportation', 'Transport, logistics, and connectivity');

-- ====================
-- DEFAULT MONITORING CONFIG
-- ====================

-- Create default monitoring configuration (admin can customize)
INSERT OR IGNORE INTO job_monitoring_config (
    config_name,
    monitoring_prompt,
    target_organizations,
    keywords,
    position_levels,
    monitoring_schedule,
    is_active
) VALUES (
    'central_govt_js_director',
    'Monitor vacancies for Joint Secretary and Director level positions in Central Government ministries',
    '["All Central Government Ministries", "Department of Personnel and Training", "UPSC"]',
    '["lateral entry", "joint secretary", "director", "deputy secretary", "expert appointment"]',
    '["joint_secretary", "director", "deputy_secretary"]',
    'hourly',
    TRUE
);

-- ====================
-- MIGRATION COMPLETE
-- ====================
-- Run this migration with:
-- sqlite3 database/lateral_entry.db < database/migrations/003_add_job_monitoring.sql
