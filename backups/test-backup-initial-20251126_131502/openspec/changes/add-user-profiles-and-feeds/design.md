# Design: Professional Networking Platform with Enhanced Features

**Change ID**: `add-user-profiles-and-feeds`  
**Status**: Draft  
**Last Updated**: 2025-11-26

## Executive Summary

This design document covers the transformation of the "Lateral Entry Portal" into a comprehensive professional networking platform for lateral entry officers in the Government of India. The platform includes:

1. **Project Rebranding**: Rename to accurately reflect purpose (information database, not application portal)
2. **Granular Visibility Controls**: 3-level field permissions (Public/Lateral Entrants Only/Private)
3. **LinkedIn Integration**: Optional real-time sync or manual entry with LinkedIn-style layout
4. **Comprehensive Job Monitoring**: AI-powered vacancy tracking across thousands of organizations
5. **User Authentication**: Google OAuth with admin approval workflow
6. **Profile Management**: User-controlled profiles with moderation
7. **Social Feeds & News**: Optional social media aggregation and news monitoring

## Key Architectural Decisions

### Decision 1: Three-Level Visibility Architecture

**Context**: Users need control over who sees their profile information while maintaining public transparency.

**Decision**: Implement field-level visibility with three tiers: Public (all visitors), Lateral Entrants Only (authenticated officers), and Private (owner only).

**Rationale**:
- **Granularity**: Field-level control gives maximum flexibility
- **Performance**: Database-driven filtering allows efficient queries
- **Security**: API middleware enforces visibility at response level
- **User Experience**: Simple toggle interface doesn't overwhelm users

**Implementation**:
- `field_visibility_settings` table stores visibility per field per user
- API middleware intercepts all profile responses and filters based on requester authentication
- Frontend shows appropriate UI elements (toggles for owners, indicators for viewers)
- Search and browse queries include visibility in WHERE clauses

**Trade-offs**:
- **Pro**: Maximum user control, clear security boundary
- **Con**: Additional database joins (mitigated with indexing)
- **Pro**: Scalable (visibility check is O(1) lookup)
- **Con**: More complex API logic (mitigated with middleware pattern)

**Alternatives Considered**:
- Profile-level visibility (Public/Private entire profile): Too coarse-grained
- Role-based access only: Doesn't provide per-user customization
- Client-side filtering: Security risk, not acceptable

---

### Decision 2: LinkedIn Integration with Dual Options

**Context**: Users want LinkedIn sync but API limitations and user preferences vary.

**Decision**: Offer both OAuth-based real-time sync (Option A) and manual URL entry (Option B). User chooses based on preference and LinkedIn API availability.

**Rationale**:
- **Flexibility**: Not all users have LinkedIn or want to link it
- **API Constraints**: LinkedIn API has rate limits; manual entry provides fallback
- **User Choice**: "Technical feasibility rests with the user" per requirements
- **Graceful Degradation**: Platform works regardless of LinkedIn API status

**Implementation**:
- **Option A (OAuth)**: LinkedIn OAuth → fetch profile data → user configures field mappings → sync on demand
- **Option B (Manual)**: User enters LinkedIn URL → manually copies data → profile adopts LinkedIn-style layout
- Both options result in same LinkedIn-style profile design
- Token storage uses same encryption as Google OAuth (Fernet)

**Trade-offs**:
- **Pro**: Works for all users regardless of LinkedIn access
- **Con**: Dual code paths increase complexity (mitigated with adapter pattern)
- **Pro**: No dependency on LinkedIn API availability
- **Con**: Manual entry requires more user effort

**Alternatives Considered**:
- OAuth only: Would exclude users without LinkedIn or those unwilling to link
- Manual only: Would miss opportunity for automatic sync and real-time updates
- Third-party LinkedIn scraping: Legal and ethical concerns, not pursued

---

### Decision 3: Parallel AI Monitor for Comprehensive Job Tracking

**Context**: Need to monitor job vacancies across thousands of organizations efficiently.

**Decision**: Use Parallel AI Monitor as primary job monitoring engine with customizable prompts for government, PSU, and private sector organizations.

**Rationale**:
- **Scale**: Can monitor thousands of organizations with single API call
- **Intelligence**: AI can understand job descriptions and relevance
- **Flexibility**: Prompt-based configuration allows admin to customize monitored organizations
- **Existing Infrastructure**: Parallel AI already used for news monitoring

**Implementation**:
- Background jobs trigger Parallel AI Monitor hourly (government) and daily (private sector)
- Comprehensive prompt includes: organization list, position levels, domains, keywords
- Results processed and scored for relevance (0-100)
- Jobs stored in `job_listings` table with metadata
- User preferences filter results for personalized job board

**Trade-offs**:
- **Pro**: Scales to thousands of organizations without individual API calls
- **Con**: Dependent on Parallel AI Monitor availability (mitigated with error handling)
- **Pro**: AI-powered relevance scoring improves over time
- **Con**: API costs scale with monitoring frequency (acceptable for value provided)

**Alternatives Considered**:
- Individual website scraping: Doesn't scale, legal concerns, high maintenance
- RSS feed aggregation: Not all orgs provide RSS, limited metadata
- Manual admin entry only: Doesn't scale, defeats purpose of monitoring
- Google Custom Search: Doesn't provide structured data, API limits

---

### Decision 4: Static-First with Optional Backend

**Context**: Portal currently works as static site; need to maintain this while adding dynamic features.

**Decision**: Keep static JSON export for read-only public data; add authenticated API for dynamic features (job board, profile editing, visibility controls).

**Rationale**:
- **Backward Compatibility**: Public visitors continue to access static content
- **Progressive Enhancement**: Authenticated features require API but don't break public access
- **Deployment Flexibility**: Can deploy frontend without backend for read-only mode
- **Performance**: Static content served from CDN, dynamic content from API

**Implementation**:
- Public profiles: Served from static JSON, filtered by "Public" visibility
- Authenticated features: API required (job board, profile editing, LinkedIn sync)
- Background jobs: Run on backend server, update database
- JSON export: Generates static files for public data only

**Trade-offs**:
- **Pro**: Public portal remains fast and CDN-cacheable
- **Con**: Dual data paths (static vs dynamic) add complexity
- **Pro**: Gradual rollout possible (can deploy frontend before backend)
- **Con**: Static export must respect visibility controls

---

### Decision 5: Field-Level Moderation with Admin Approval

**Context**: Users can edit any field, but changes need review before going live.

**Decision**: All field edits create edit requests in moderation queue; admin approves/rejects before changes apply to public profile.

**Rationale**:
- **Data Quality**: Prevents inappropriate or incorrect information
- **Audit Trail**: Every change is logged and reviewable
- **User Empowerment**: Users can edit anything, but with oversight
- **Flexibility**: Admin can approve in bulk or selectively

**Implementation**:
- User edits → creates `field_edit_requests` record with status='pending'
- Admin views moderation queue with diff viewer
- Approve → updates lateral_entrants table, creates audit log entry
- Reject → notifies user, edit request marked rejected
- Uploads follow same pattern (separate `uploads` table moderation)

**Trade-offs**:
- **Pro**: Maintains data quality and prevents abuse
- **Con**: Adds latency (changes not immediate)
- **Pro**: Audit trail for compliance
- **Con**: Admin workload (mitigated with bulk approval tools)

**Alternatives Considered**:
- Immediate updates: Risk of inappropriate content, no quality control
- Pre-moderation for new users only: Inconsistent experience
- Auto-moderation with AI: False positives/negatives, still needs human review

---

### Decision 6: Project Rebranding without Technical Changes

**Context**: Portal name misleading (suggests application portal); need to clarify purpose.

**Decision**: Update display name and messaging on frontend only; keep all technical infrastructure (URLs, database names, code) unchanged.

**Rationale**:
- **No Breaking Changes**: External links, bookmarks, API consumers unaffected
- **Quick Implementation**: Frontend text changes only, can deploy in days
- **Clear Communication**: Homepage clarification prevents user confusion
- **Backward Compatible**: No migration or refactoring required

**Implementation**:
- Update `index.html` and all pages: title tags, headings, meta descriptions
- Add prominent clarification: "This is an information database. To apply for lateral entry, visit UPSC."
- Update `manifest.json`, footer, documentation
- Repository, database, URLs remain unchanged

**Trade-offs**:
- **Pro**: Zero technical risk, no downtime
- **Con**: Internal code still references "portal" (acceptable, user doesn't see)
- **Pro**: Fast implementation (2 days)
- **Con**: SEO takes weeks to reflect new name (expected behavior)

**Alternatives Considered**:
- Full rebrand including URLs: High risk, breaks external links
- No change: Continues user confusion about portal purpose
- Subdomain migration: Unnecessary complexity for display name change

---

## Architecture Overview

This change introduces significant new capabilities to the platform, transforming it from a static content site to an interactive professional networking platform with user authentication, granular privacy controls, LinkedIn integration, comprehensive job monitoring, and content management.

### High-Level Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Public Pages          │  Authenticated Pages  │  Admin Pages   │
│  - Homepage w/feeds    │  - Profile Editor     │  - User Mgmt   │
│  - Profile View        │  - Photo Upload       │  - Moderation  │
│  - Search/Browse       │  - AI Assistant       │  - Config      │
│                                                                   │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ REST API / JSON
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                      Backend API Layer (Flask)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Authentication   │  Profile API    │  Upload API  │  Admin API │
│  - Login/Logout   │  - CRUD Ops     │  - Files     │  - Moderate│
│  - Sessions       │  - Validation   │  - Images    │  - Users   │
│  - Permissions    │  - AI Assist    │  - Docs      │  - Config  │
│                                                                   │
└───────────┬───────────┬───────────────┬──────────────┬──────────┘
            │           │               │              │
            │           │               │              │
┌───────────▼──┐ ┌──────▼────┐ ┌───────▼──────┐ ┌────▼──────────┐
│   SQLite     │ │  File     │ │  External    │ │   Background  │
│   Database   │ │  Storage  │ │  Services    │ │   Workers     │
│              │ │           │ │              │ │               │
│ - Users      │ │ - Photos  │ │ - AI Model   │ │ - News Monitor│
│ - Profiles   │ │ - Docs    │ │ - Social APIs│ │ - Feed Refresh│
│ - Sessions   │ │ - Uploads │ │ - Parallel AI│ │ - Cache Update│
│ - Audit Log  │ │           │ │              │ │               │
└──────────────┘ └───────────┘ └──────────────┘ └───────────────┘
```

## Data Model Changes

### New Tables

#### 1. Users and Authentication

```sql
-- User accounts for appointees
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER UNIQUE, -- Links to lateral_entrants
    google_id VARCHAR(255) UNIQUE NOT NULL, -- Google account ID
    email VARCHAR(255) UNIQUE NOT NULL, -- From Google account
    name VARCHAR(255), -- From Google account
    picture_url TEXT, -- Google profile picture
    role VARCHAR(50) DEFAULT 'appointee', -- appointee, admin
    is_approved BOOLEAN DEFAULT FALSE, -- Admin approval required
    is_active BOOLEAN DEFAULT TRUE,
    approved_by INTEGER, -- Admin who approved
    approved_at TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Pending user requests (before admin approval)
CREATE TABLE pending_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    picture_url TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    request_notes TEXT -- User can explain who they are
);

-- Active sessions
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    google_access_token TEXT, -- OAuth access token (encrypted)
    google_refresh_token TEXT, -- OAuth refresh token (encrypted)
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Audit log for all profile changes
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    action VARCHAR(100) NOT NULL, -- create, update, delete, upload, approve, reject
    entity_type VARCHAR(50) NOT NULL, -- profile, photo, achievement, etc.
    entity_id INTEGER,
    old_value TEXT,
    new_value TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 2. Media and Uploads (with Moderation)

```sql
-- Photos and documents
CREATE TABLE uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL, -- user_id
    file_type VARCHAR(50) NOT NULL, -- photo, document, certificate
    original_filename VARCHAR(255),
    stored_filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    width INTEGER, -- for images
    height INTEGER, -- for images
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE, -- primary profile photo
    moderation_status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
    moderated_by INTEGER,
    moderated_at TIMESTAMP,
    moderation_notes TEXT,
    is_public BOOLEAN DEFAULT FALSE, -- Only true after approval
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (moderated_by) REFERENCES users(id)
);

-- Profile field edit requests (for admin approval)
CREATE TABLE field_edit_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    entrant_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL, -- Which field to edit
    current_value TEXT, -- Current value in database
    requested_value TEXT, -- New value requested by user
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
    reviewed_by INTEGER,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id)
);

-- Education credentials (enhanced)
CREATE TABLE education_credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    education_detail_id INTEGER NOT NULL,
    credential_type VARCHAR(100), -- degree_certificate, transcript, award
    upload_id INTEGER,
    verification_status VARCHAR(50) DEFAULT 'pending',
    verified_by INTEGER,
    verified_at TIMESTAMP,
    FOREIGN KEY (education_detail_id) REFERENCES education_details(id),
    FOREIGN KEY (upload_id) REFERENCES uploads(id),
    FOREIGN KEY (verified_by) REFERENCES users(id)
);
```

#### 3. AI Assistance

```sql
-- AI-generated content suggestions
CREATE TABLE ai_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content_type VARCHAR(100), -- summary, achievement, education
    input_data TEXT, -- User's raw input/bullet points
    generated_content TEXT, -- AI's suggestion
    was_accepted BOOLEAN,
    edited_content TEXT, -- User's final version
    model_version VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- AI API usage tracking
CREATE TABLE ai_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    request_type VARCHAR(100),
    tokens_used INTEGER,
    response_time_ms INTEGER,
    success BOOLEAN,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 4. Social Media and News

```sql
-- Social media feed items
CREATE TABLE social_feed_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform VARCHAR(50) NOT NULL, -- twitter, facebook, linkedin
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

-- News articles from monitoring
CREATE TABLE news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    url TEXT UNIQUE,
    source_name VARCHAR(255),
    author VARCHAR(255),
    summary TEXT,
    content TEXT,
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment VARCHAR(50), -- positive, neutral, negative
    relevance_score FLOAT,
    related_entrant_ids TEXT, -- JSON array of entrant IDs mentioned
    related_keywords TEXT -- JSON array of keywords
);

-- Social media monitoring configuration
CREATE TABLE social_monitoring_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform VARCHAR(50) NOT NULL,
    account_handle VARCHAR(255),
    account_type VARCHAR(50), -- ministry, appointee, media
    is_active BOOLEAN DEFAULT TRUE,
    fetch_frequency_minutes INTEGER DEFAULT 15,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- News monitoring keywords
CREATE TABLE news_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword VARCHAR(255) NOT NULL,
    keyword_type VARCHAR(50), -- entrant_name, ministry, program
    related_entrant_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (related_entrant_id) REFERENCES lateral_entrants(id)
);
```

#### 5. Content Moderation

```sql
-- Flagged content for review
CREATE TABLE flagged_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type VARCHAR(50), -- upload, profile_text, comment
    content_id INTEGER,
    flagged_by INTEGER, -- NULL for automated flags
    flag_reason VARCHAR(255),
    flag_type VARCHAR(50), -- inappropriate, inaccurate, spam
    status VARCHAR(50) DEFAULT 'pending', -- pending, reviewed, approved, removed
    reviewed_by INTEGER,
    reviewed_at TIMESTAMP,
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flagged_by) REFERENCES users(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id)
);
```

### Modified Tables

#### Extend lateral_entrants

```sql
-- Add new columns to existing lateral_entrants table
ALTER TABLE lateral_entrants ADD COLUMN is_profile_claimed BOOLEAN DEFAULT FALSE;
ALTER TABLE lateral_entrants ADD COLUMN profile_completeness INTEGER DEFAULT 0; -- 0-100%
ALTER TABLE lateral_entrants ADD COLUMN profile_views INTEGER DEFAULT 0;
ALTER TABLE lateral_entrants ADD COLUMN last_profile_update TIMESTAMP;
ALTER TABLE lateral_entrants ADD COLUMN ai_generated_summary TEXT; -- AI suggestion
ALTER TABLE lateral_entrants ADD COLUMN custom_summary TEXT; -- User override
```

## API Endpoints

### Authentication Endpoints (Google OAuth)

```
GET    /api/auth/google/login      - Redirect to Google OAuth consent
GET    /api/auth/google/callback   - Handle OAuth callback
POST   /api/auth/logout             - End session
GET    /api/auth/me                 - Get current user info
GET    /api/auth/status             - Check if user is approved
POST   /api/auth/request-access     - Submit access request (after OAuth)
```

### User Management Endpoints (Authenticated Users)

```
GET    /api/profile                 - Get own profile (authenticated)
GET    /api/profile/:id             - Get public profile (any user)
GET    /api/profile/uploads         - Get own uploads with moderation status
GET    /api/profile/edit-requests   - Get own field edit requests status
```

### Upload Endpoints (Authenticated Users)

```
POST   /api/uploads/photo           - Upload profile photo (goes to moderation)
POST   /api/uploads/document        - Upload document (goes to moderation)
DELETE /api/uploads/:id             - Delete own pending upload
PUT    /api/uploads/:id/caption     - Update caption of own upload
GET    /api/uploads/pending         - Get own pending uploads
```

### Field Edit Request Endpoints (Authenticated Users)

```
POST   /api/edit-requests           - Request to edit a profile field
GET    /api/edit-requests           - Get status of own edit requests
DELETE /api/edit-requests/:id       - Cancel pending edit request
```

### AI Assistant Endpoints

```
POST   /api/ai/suggest-summary     - Generate profile summary
POST   /api/ai/suggest-achievement - Suggest achievement description
POST   /api/ai/improve-text        - Improve/grammar-check text
POST   /api/ai/translate           - Translate text (future)
GET    /api/ai/usage               - Get AI usage stats (authenticated)
```

### Social Media Feed Endpoints

```
GET    /api/feeds/social           - Get social media feed items
GET    /api/feeds/news             - Get news articles
GET    /api/feeds/combined         - Get combined feed (social + news)
POST   /api/feeds/refresh          - Trigger manual refresh (admin)
GET    /api/feeds/config           - Get monitoring configuration (admin)
PUT    /api/feeds/config           - Update monitoring config (admin)
```

### Admin Endpoints

```
GET    /api/admin/users            - List all users
POST   /api/admin/users/approve    - Approve pending user
POST   /api/admin/users/reject     - Reject pending user
POST   /api/admin/users/link       - Link user to entrant profile
PUT    /api/admin/users/:id        - Update user (activate/deactivate)
DELETE /api/admin/users/:id        - Delete user account

GET    /api/admin/pending-users    - List pending access requests
GET    /api/admin/pending-uploads  - List uploads awaiting moderation
POST   /api/admin/uploads/:id/approve - Approve upload
POST   /api/admin/uploads/:id/reject  - Reject upload

GET    /api/admin/edit-requests    - List field edit requests
POST   /api/admin/edit-requests/:id/approve - Approve field edit
POST   /api/admin/edit-requests/:id/reject  - Reject field edit

GET    /api/admin/flagged          - Get flagged content
PUT    /api/admin/flagged/:id      - Review flagged content
GET    /api/admin/audit-log        - View audit log
GET    /api/admin/stats            - System statistics
```

## File Upload Architecture

### Storage Strategy

```
uploads/
├── photos/
│   ├── original/        # Original uploads
│   │   └── {entrant_id}/
│   │       └── {uuid}.jpg
│   ├── large/           # 1200px max
│   │   └── {entrant_id}/
│   │       └── {uuid}.jpg
│   ├── medium/          # 600px max
│   │   └── {entrant_id}/
│   │       └── {uuid}.jpg
│   └── thumbnail/       # 200px max
│       └── {entrant_id}/
│           └── {uuid}.jpg
├── documents/
│   └── {entrant_id}/
│       └── {uuid}.pdf
└── temp/                # Temporary upload location
    └── {session_id}/
        └── {filename}
```

### Upload Flow

```
1. Client uploads file via POST /api/profile/photo
2. Server validates:
   - File type (whitelist: JPEG, PNG, WebP, PDF)
   - File size (< 5MB for images, < 10MB for docs)
   - User authentication and permissions
   - File content (magic bytes check)
   - Virus scan (optional, using ClamAV)
3. Server generates UUID filename
4. Server stores in temp/ directory
5. For images:
   - Generate multiple sizes (large, medium, thumbnail)
   - Optimize (reduce quality to 85%, strip EXIF)
   - Convert to WebP for modern browsers
6. Move from temp/ to permanent storage
7. Create database record in uploads table
8. Return upload ID and URLs to client
9. Clean up temp files older than 1 hour (background job)
```

### Security Measures

- MIME type validation
- Magic bytes checking
- File extension whitelist
- Random UUID filenames (prevent path traversal)
- Separate directory per user
- No execution permissions on upload directories
- Rate limiting (5 uploads per minute per user)
- Total storage quota per user (100MB)
- Virus scanning on upload
- Content moderation via AI (detect inappropriate content)

## AI Integration Architecture

### AI Model Configuration

```python
# config.py
AI_CONFIG = {
    'base_url': os.getenv('CUSTOM_AI_BASE_URL'),  # User provides
    'api_key': os.getenv('CUSTOM_AI_API_KEY'),    # User provides
    'model_name': os.getenv('CUSTOM_AI_MODEL', 'default'),
    'timeout': 10,  # seconds
    'max_tokens': 500,
    'temperature': 0.7,
    'rate_limit': {
        'requests_per_minute': 10,
        'requests_per_hour': 50,
        'requests_per_day': 200
    }
}
```

### AI Service Layer

```python
# ai_service.py
class AIService:
    def __init__(self, config):
        self.base_url = config['base_url']
        self.api_key = config['api_key']
        self.rate_limiter = RateLimiter(config['rate_limit'])
    
    async def suggest_summary(self, user_data):
        """Generate profile summary from structured data"""
        prompt = self._build_summary_prompt(user_data)
        response = await self._call_ai_api(prompt, 'summary')
        return self._parse_response(response)
    
    async def suggest_achievement(self, achievement_data):
        """Generate achievement description from bullet points"""
        prompt = self._build_achievement_prompt(achievement_data)
        response = await self._call_ai_api(prompt, 'achievement')
        return self._parse_response(response)
    
    async def improve_text(self, text):
        """Grammar check and improve text"""
        prompt = self._build_improvement_prompt(text)
        response = await self._call_ai_api(prompt, 'improve')
        return self._parse_response(response)
    
    async def _call_ai_api(self, prompt, request_type):
        """Make API call with error handling and retry logic"""
        # Check rate limit
        if not self.rate_limiter.allow_request():
            raise RateLimitExceeded()
        
        # Make request with timeout and retry
        try:
            response = await self._make_request(prompt)
            # Log usage
            await self._log_usage(request_type, response)
            return response
        except Exception as e:
            # Log error
            await self._log_error(request_type, str(e))
            raise
```

### AI Prompt Templates

```python
SUMMARY_PROMPT = """
Generate a professional 2-3 paragraph summary for a government lateral entry appointee profile.

Name: {name}
Position: {position}
Ministry: {ministry}
Education: {education}
Previous Experience: {experience}
Key Achievements: {achievements}

Requirements:
- Professional tone appropriate for government website
- Highlight relevant expertise and accomplishments
- 150-200 words
- Focus on impact and contributions
- Avoid jargon and overly technical language
"""

ACHIEVEMENT_PROMPT = """
Convert these achievement bullet points into a professional paragraph description:

{bullet_points}

Requirements:
- Start with the achievement's impact
- Include measurable results if available
- Professional government tone
- 75-100 words
- Highlight stakeholder benefits
"""
```

### Fallback Strategy

```python
def get_ai_suggestion_with_fallback(user_data, content_type):
    """Try AI, fall back to templates if AI fails"""
    try:
        # Try AI service
        suggestion = ai_service.suggest_summary(user_data)
        return {
            'source': 'ai',
            'content': suggestion,
            'confidence': 0.9
        }
    except AIServiceUnavailable:
        # Fall back to template-based suggestion
        suggestion = template_service.generate_from_template(
            user_data, 
            content_type
        )
        return {
            'source': 'template',
            'content': suggestion,
            'confidence': 0.6
        }
    except RateLimitExceeded:
        # User exceeded rate limit, show message
        return {
            'source': 'none',
            'error': 'Rate limit exceeded. Please try again later.',
            'suggestion': 'Consider these guidelines: ...'
        }
```

## Social Media Feed Architecture

### Feed Aggregation Service

```python
# feed_aggregator.py
class FeedAggregator:
    def __init__(self):
        self.twitter_client = TwitterAPIClient()
        self.facebook_client = FacebookGraphClient()
        self.linkedin_client = LinkedInAPIClient()
        self.cache = RedisCache() if REDIS_AVAILABLE else InMemoryCache()
    
    async def fetch_all_feeds(self):
        """Fetch from all platforms in parallel"""
        tasks = [
            self.fetch_twitter_feed(),
            self.fetch_facebook_feed(),
            self.fetch_linkedin_feed()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return self._combine_feeds(results)
    
    async def fetch_twitter_feed(self):
        """Fetch tweets about lateral entry"""
        cache_key = 'twitter_feed'
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Fetch from Twitter API
        queries = self._build_twitter_queries()
        tweets = []
        for query in queries:
            results = await self.twitter_client.search(query, max_results=100)
            tweets.extend(results)
        
        # Filter and score relevance
        relevant_tweets = self._filter_relevant(tweets)
        
        # Cache for 15 minutes
        self.cache.set(cache_key, relevant_tweets, ttl=900)
        
        # Store in database
        await self._store_feed_items(relevant_tweets, 'twitter')
        
        return relevant_tweets
    
    def _build_twitter_queries(self):
        """Build search queries from keywords"""
        entrants = get_all_entrant_names()
        ministries = get_all_ministries()
        
        queries = [
            'lateral entry government india',
            'UPSC lateral entry',
        ]
        
        # Add queries for each appointee
        for entrant in entrants:
            queries.append(f'"{entrant}" joint secretary OR director')
        
        return queries
```

### Feed Display Strategy

```javascript
// Frontend feed loading
class FeedManager {
    constructor() {
        this.feeds = {
            twitter: [],
            facebook: [],
            linkedin: [],
            news: []
        };
        this.isLoading = false;
        this.lastUpdate = null;
    }
    
    async loadFeeds() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoadingState();
        
        try {
            // Load feeds with timeout
            const response = await fetch('/api/feeds/combined', {
                timeout: 5000
            });
            
            if (!response.ok) {
                throw new Error('Failed to load feeds');
            }
            
            const data = await response.json();
            this.feeds = data.feeds;
            this.lastUpdate = new Date();
            
            this.renderFeeds();
            this.startAutoRefresh();
            
        } catch (error) {
            console.error('Feed load failed:', error);
            this.showErrorState();
            // Show cached feeds if available
            this.loadCachedFeeds();
        } finally {
            this.isLoading = false;
        }
    }
    
    startAutoRefresh() {
        // Refresh every 15 minutes
        setInterval(() => this.loadFeeds(), 15 * 60 * 1000);
    }
    
    renderFeeds() {
        const container = document.getElementById('social-feed');
        
        // Combine and sort all feeds by timestamp
        const allItems = this._combineFeeds();
        const sortedItems = allItems.sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
        );
        
        // Render top 20 items
        const itemsToShow = sortedItems.slice(0, 20);
        container.innerHTML = itemsToShow.map(item => 
            this.renderFeedItem(item)
        ).join('');
        
        // Add lazy loading for more items
        this.setupInfiniteScroll();
    }
    
    renderFeedItem(item) {
        const templates = {
            twitter: this.renderTweet,
            facebook: this.renderFacebookPost,
            linkedin: this.renderLinkedInPost,
            news: this.renderNewsArticle
        };
        
        const renderer = templates[item.platform];
        return renderer ? renderer(item) : '';
    }
}
```

## News Monitoring Architecture

### Parallel AI Monitor Integration

```python
# news_monitor.py
class NewsMonitor:
    def __init__(self, parallel_config):
        self.parallel_url = parallel_config['monitor_url']
        self.parallel_api_key = parallel_config['api_key']
        self.keywords = self._load_keywords()
    
    async def monitor_news(self):
        """Run news monitoring check"""
        # Build monitoring request for Parallel AI
        monitor_request = {
            'sources': [
                'timesofindia.com',
                'economictimes.com',
                'thehindu.com',
                'businessstandard.com',
                'indianexpress.com',
                'hindustantimes.com'
            ],
            'keywords': self.keywords,
            'time_range': '24h',  # Last 24 hours
            'max_results': 100
        }
        
        # Call Parallel AI Monitor
        response = await self._call_parallel_monitor(monitor_request)
        
        # Process results
        articles = self._process_monitor_response(response)
        
        # Filter and score relevance
        relevant_articles = self._filter_relevant_articles(articles)
        
        # Store in database
        await self._store_articles(relevant_articles)
        
        # Notify if high-relevance articles found
        high_relevance = [a for a in relevant_articles if a['relevance_score'] > 0.8]
        if high_relevance:
            await self._notify_admins(high_relevance)
        
        return relevant_articles
    
    async def _call_parallel_monitor(self, request):
        """Call Parallel AI Monitor API"""
        headers = {
            'Authorization': f'Bearer {self.parallel_api_key}',
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.parallel_url,
                json=request,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
    
    def _filter_relevant_articles(self, articles):
        """Score and filter articles by relevance"""
        scored_articles = []
        
        for article in articles:
            score = self._calculate_relevance_score(article)
            if score > 0.5:  # Threshold
                article['relevance_score'] = score
                article['related_entrant_ids'] = self._extract_entrant_mentions(
                    article['content']
                )
                scored_articles.append(article)
        
        return sorted(scored_articles, key=lambda x: x['relevance_score'], reverse=True)
    
    def _calculate_relevance_score(self, article):
        """Calculate how relevant article is to lateral entry program"""
        score = 0.0
        text = f"{article['title']} {article['content']}".lower()
        
        # Check for program keywords
        program_keywords = ['lateral entry', 'joint secretary', 'private sector']
        for keyword in program_keywords:
            if keyword in text:
                score += 0.3
        
        # Check for appointee names
        for entrant in get_all_entrant_names():
            if entrant.lower() in text:
                score += 0.5
        
        # Check for ministry mentions
        for ministry in get_all_ministries():
            if ministry.lower() in text:
                score += 0.2
        
        # Bonus for major publications
        if article['source'] in ['The Hindu', 'Times of India', 'Economic Times']:
            score += 0.1
        
        return min(score, 1.0)
```

### Background Job Scheduler

```python
# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler

def setup_background_jobs():
    """Configure background jobs for monitoring and caching"""
    scheduler = BackgroundScheduler()
    
    # News monitoring - every hour
    scheduler.add_job(
        func=run_news_monitoring,
        trigger='interval',
        hours=1,
        id='news_monitor',
        name='Monitor news articles'
    )
    
    # Social media feeds - every 15 minutes
    scheduler.add_job(
        func=refresh_social_feeds,
        trigger='interval',
        minutes=15,
        id='social_feeds',
        name='Refresh social media feeds'
    )
    
    # Cache cleanup - daily at 2 AM
    scheduler.add_job(
        func=cleanup_old_cache,
        trigger='cron',
        hour=2,
        minute=0,
        id='cache_cleanup',
        name='Clean up old cached data'
    )
    
    # Generate analytics - daily at 1 AM
    scheduler.add_job(
        func=generate_daily_analytics,
        trigger='cron',
        hour=1,
        minute=0,
        id='analytics',
        name='Generate analytics reports'
    )
    
    scheduler.start()
    return scheduler

async def run_news_monitoring():
    """Background job to monitor news"""
    try:
        monitor = NewsMonitor(config.PARALLEL_AI_CONFIG)
        articles = await monitor.monitor_news()
        logger.info(f"Found {len(articles)} relevant news articles")
    except Exception as e:
        logger.error(f"News monitoring failed: {e}")

async def refresh_social_feeds():
    """Background job to refresh social media feeds"""
    try:
        aggregator = FeedAggregator()
        feeds = await aggregator.fetch_all_feeds()
        logger.info(f"Refreshed {len(feeds)} social feed items")
    except Exception as e:
        logger.error(f"Feed refresh failed: {e}")
```

## Authentication Flow

### Google OAuth Login Flow

```
1. User clicks "Sign in with Google" button
2. Frontend redirects to: GET /api/auth/google/login
3. Backend redirects to Google OAuth consent page with:
   - client_id (from config)
   - redirect_uri: {BASE_URL}/api/auth/google/callback
   - scope: email, profile
   - state: random token (CSRF protection)
4. User approves on Google's consent page
5. Google redirects back to: /api/auth/google/callback?code=...&state=...
6. Backend validates state token (CSRF check)
7. Backend exchanges code for access token with Google
8. Backend fetches user info from Google (email, name, picture)
9. Backend checks if user exists in users table:
   
   IF user exists AND is_approved = TRUE:
     - Create session
     - Set secure HTTP-only cookie
     - Redirect to /profile page
   
   IF user exists AND is_approved = FALSE:
     - Show "Awaiting admin approval" message
     - Redirect to /pending-approval page
   
   IF user does NOT exist:
     - Create entry in pending_users table
     - Show "Access request submitted" message
     - Redirect to /access-requested page
     - Notify admins via email (optional)

10. Approved users can now access their profile editing features
```

### Admin Approval Workflow

```
1. Admin logs in (admin user with is_approved=TRUE and role='admin')
2. Admin visits /admin/pending-users
3. Admin sees list of pending access requests with:
   - Google profile info (name, email, picture)
   - Request timestamp
   - Optional: user's self-description
4. Admin reviews each request:
   
   TO APPROVE:
   - Select which entrant profile this user should edit
   - Click "Approve and Link to Profile"
   - Backend creates user record with:
     * google_id, email, name from pending_users
     * entrant_id = selected profile
     * is_approved = TRUE
     * approved_by = admin_id
     * approved_at = now
   - Delete from pending_users
   - User gets email notification (optional)
   
   TO REJECT:
   - Add rejection reason (optional)
   - Click "Reject"
   - Delete from pending_users
   - User gets rejection email (optional)

5. Approved user can now log in and access editing features
```

### Session Management

```python
# session_manager.py
class SessionManager:
    def create_session(self, user_id, ip_address, user_agent, google_tokens):
        """Create new session"""
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        
        # Encrypt Google tokens before storing
        encrypted_access = encrypt_token(google_tokens['access_token'])
        encrypted_refresh = encrypt_token(google_tokens['refresh_token'])
        
        db.execute("""
            INSERT INTO sessions (id, user_id, google_access_token, 
                                google_refresh_token, ip_address, 
                                user_agent, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, user_id, encrypted_access, encrypted_refresh,
              ip_address, user_agent, expires_at))
        
        return session_id
    
    def validate_session(self, session_id):
        """Check if session is valid"""
        session = db.execute("""
            SELECT s.*, u.is_approved, u.is_active 
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.id = ? AND s.expires_at > ?
        """, (session_id, datetime.now())).fetchone()
        
        if not session:
            return None
        
        # Check if user is still approved and active
        if not session['is_approved'] or not session['is_active']:
            # Admin revoked access, delete session
            self.delete_session(session_id)
            return None
        
        return session
    
    def refresh_google_token(self, session_id):
        """Refresh Google access token if expired"""
        session = db.execute("""
            SELECT google_refresh_token FROM sessions WHERE id = ?
        """, (session_id,)).fetchone()
        
        if not session:
            return None
        
        # Decrypt refresh token
        refresh_token = decrypt_token(session['google_refresh_token'])
        
        # Call Google to refresh
        new_tokens = google_oauth.refresh_token(refresh_token)
        
        # Update session with new tokens
        encrypted_access = encrypt_token(new_tokens['access_token'])
        db.execute("""
            UPDATE sessions 
            SET google_access_token = ?
            WHERE id = ?
        """, (encrypted_access, session_id))
        
        return new_tokens
    
    def delete_session(self, session_id):
        """Logout - delete session"""
        db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions (run daily)"""
        db.execute("""
            DELETE FROM sessions WHERE expires_at < ?
        """, (datetime.now(),))
```

### Google OAuth Implementation

```python
# google_oauth.py
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import os

class GoogleOAuthService:
    def __init__(self, config):
        self.client_id = config['GOOGLE_CLIENT_ID']
        self.client_secret = config['GOOGLE_CLIENT_SECRET']
        self.redirect_uri = config['BASE_URL'] + '/api/auth/google/callback'
        self.scopes = ['openid', 'email', 'profile']
    
    def get_authorization_url(self, state):
        """Generate Google OAuth authorization URL"""
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent'
        )
        
        return authorization_url
    
    def exchange_code_for_tokens(self, code, state):
        """Exchange authorization code for access and refresh tokens"""
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            state=state
        )
        flow.redirect_uri = self.redirect_uri
        
        # Fetch tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return {
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'id_token': credentials.id_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
    
    def get_user_info(self, id_token_str):
        """Extract user info from ID token"""
        try:
            # Verify the token
            id_info = id_token.verify_oauth2_token(
                id_token_str,
                requests.Request(),
                self.client_id
            )
            
            # Extract user information
            return {
                'google_id': id_info['sub'],
                'email': id_info['email'],
                'name': id_info.get('name', ''),
                'picture_url': id_info.get('picture', ''),
                'email_verified': id_info.get('email_verified', False)
            }
        except ValueError as e:
            raise InvalidTokenError(f"Invalid ID token: {e}")
    
    def refresh_access_token(self, refresh_token):
        """Refresh access token using refresh token"""
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        # Refresh the credentials
        credentials.refresh(Request())
        
        return {
            'access_token': credentials.token,
            'expires_at': credentials.expiry
        }

# auth_routes.py
from flask import Blueprint, request, redirect, session, jsonify, url_for
import secrets

auth_bp = Blueprint('auth', __name__)
google_oauth = GoogleOAuthService(app.config)

@auth_bp.route('/api/auth/google/login')
def google_login():
    """Initiate Google OAuth flow"""
    # Generate CSRF token
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Generate authorization URL
    auth_url = google_oauth.get_authorization_url(state)
    
    return redirect(auth_url)

@auth_bp.route('/api/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    # Verify state token (CSRF protection)
    state = request.args.get('state')
    if not state or state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    # Clear state from session
    session.pop('oauth_state', None)
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No authorization code received'}), 400
    
    try:
        # Exchange code for tokens
        tokens = google_oauth.exchange_code_for_tokens(code, state)
        
        # Get user info from ID token
        user_info = google_oauth.get_user_info(tokens['id_token'])
        
        # Check if user exists
        user = db.execute("""
            SELECT * FROM users WHERE google_id = ?
        """, (user_info['google_id'],)).fetchone()
        
        if user:
            # User exists
            if not user['is_approved']:
                # User not yet approved by admin
                return redirect(url_for('pending_approval'))
            
            if not user['is_active']:
                # User account deactivated
                return jsonify({'error': 'Account deactivated'}), 403
            
            # Create session
            session_id = session_manager.create_session(
                user_id=user['id'],
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                google_tokens=tokens
            )
            
            # Update last login
            db.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            """, (user['id'],))
            db.commit()
            
            # Set secure cookie
            response = redirect(url_for('profile_editor'))
            response.set_cookie(
                'session_id',
                session_id,
                httponly=True,
                secure=app.config['SESSION_COOKIE_SECURE'],
                samesite='Lax',
                max_age=604800  # 7 days
            )
            
            return response
        
        else:
            # User doesn't exist - check if pending
            pending = db.execute("""
                SELECT * FROM pending_users WHERE google_id = ?
            """, (user_info['google_id'],)).fetchone()
            
            if pending:
                # Already requested access
                return redirect(url_for('pending_approval'))
            
            # Create pending user request
            db.execute("""
                INSERT INTO pending_users (google_id, email, name, picture_url)
                VALUES (?, ?, ?, ?)
            """, (user_info['google_id'], user_info['email'], 
                  user_info['name'], user_info['picture_url']))
            db.commit()
            
            # Notify admins (optional)
            notify_admins_new_user_request(user_info)
            
            return redirect(url_for('access_requested'))
    
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        return jsonify({'error': 'Authentication failed'}), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log out user and delete session"""
    session_id = request.cookies.get('session_id')
    if session_id:
        session_manager.delete_session(session_id)
    
    response = jsonify({'success': True})
    response.delete_cookie('session_id')
    return response

@auth_bp.route('/api/auth/me')
def get_current_user():
    """Get current authenticated user info"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'authenticated': False}), 401
    
    session_data = session_manager.validate_session(session_id)
    if not session_data:
        return jsonify({'authenticated': False}), 401
    
    user = get_user_by_id(session_data['user_id'])
    return jsonify({
        'authenticated': True,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'entrant_id': user['entrant_id'],
            'picture_url': user['picture_url']
        }
    })

@auth_bp.route('/api/auth/status')
def check_status():
    """Check approval status for pending users"""
    # This endpoint can be called without authentication
    # to check if a Google user has been approved
    google_id = request.args.get('google_id')
    if not google_id:
        return jsonify({'error': 'Missing google_id'}), 400
    
    # Check if user is approved
    user = db.execute("""
        SELECT is_approved, is_active FROM users WHERE google_id = ?
    """, (google_id,)).fetchone()
    
    if user:
        return jsonify({
            'status': 'approved' if user['is_approved'] else 'pending',
            'active': user['is_active']
        })
    
    # Check if pending
    pending = db.execute("""
        SELECT * FROM pending_users WHERE google_id = ?
    """, (google_id,)).fetchone()
    
    if pending:
        return jsonify({'status': 'pending'})
    
    return jsonify({'status': 'not_found'})

# Token encryption utilities
from cryptography.fernet import Fernet
import base64

def get_encryption_key():
    """Get or generate encryption key for tokens"""
    key = os.getenv('TOKEN_ENCRYPTION_KEY')
    if not key:
        # Generate new key (should be done once and stored in .env)
        key = Fernet.generate_key().decode()
        logger.warning("Generated new encryption key. Store this in TOKEN_ENCRYPTION_KEY env var!")
    return key.encode() if isinstance(key, str) else key

def encrypt_token(token):
    """Encrypt OAuth token before storing"""
    f = Fernet(get_encryption_key())
    return f.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token):
    """Decrypt OAuth token when retrieving"""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_token.encode()).decode()
```

### Permission Checks

```python
# decorators.py
from functools import wraps
from flask import request, jsonify

def require_auth(f):
    """Require authentication and approval"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        session = session_manager.validate_session(session_id)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        # Attach user to request
        user = get_user_by_id(session['user_id'])
        if not user['is_approved']:
            return jsonify({'error': 'Account pending approval'}), 403
        
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    """Require admin role"""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    
    return decorated_function

def require_own_profile(f):
    """Require user to be editing their own profile"""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        profile_id = kwargs.get('id')
        if str(request.current_user['entrant_id']) != str(profile_id):
            return jsonify({'error': 'Cannot edit other profiles'}), 403
        return f(*args, **kwargs)
    
    return decorated_function

def check_editable_field(field_name):
    """Check if user can edit this field"""
    # Define which fields are editable by users
    EDITABLE_FIELDS = [
        'profile_summary',
        'contact_info',
        'social_media_links',
        # Add more fields as defined by admin
    ]
    
    READONLY_FIELDS = [
        'name',
        'position',
        'ministry',
        'department',
        'batch_year',
        'date_of_appointment',
        # Critical fields that only admin can edit
    ]
    
    if field_name in READONLY_FIELDS:
        return False, 'This field cannot be edited by users'
    
    if field_name not in EDITABLE_FIELDS:
        return False, 'Unknown or restricted field'
    
    return True, None
```

## Frontend Architecture

### Profile Editor Component

```javascript
// profile-editor.js
class ProfileEditor {
    constructor(entrantId) {
        this.entrantId = entrantId;
        this.profileData = null;
        this.isDirty = false;
        this.autoSaveTimer = null;
        this.aiService = new AIAssistant();
    }
    
    async load() {
        try {
            const response = await fetch('/api/profile');
            this.profileData = await response.json();
            this.render();
            this.setupAutoSave();
            this.setupAIAssistant();
        } catch (error) {
            this.showError('Failed to load profile');
        }
    }
    
    setupAutoSave() {
        // Auto-save every 30 seconds if changes detected
        this.autoSaveTimer = setInterval(() => {
            if (this.isDirty) {
                this.save();
            }
        }, 30000);
    }
    
    setupAIAssistant() {
        // Add AI suggestion buttons to text fields
        document.querySelectorAll('[data-ai-assist]').forEach(field => {
            this.addAIButton(field);
        });
    }
    
    addAIButton(field) {
        const button = document.createElement('button');
        button.className = 'ai-assist-btn';
        button.innerHTML = '<i class="fas fa-magic"></i> AI Assist';
        button.onclick = () => this.showAISuggestion(field);
        field.parentElement.appendChild(button);
    }
    
    async showAISuggestion(field) {
        const fieldName = field.getAttribute('data-ai-assist');
        const currentValue = field.value;
        
        // Show loading state
        this.showAILoading(field);
        
        try {
            // Get AI suggestion
            const suggestion = await this.aiService.getSuggestion(
                fieldName, 
                this.profileData
            );
            
            // Show suggestion modal
            this.showSuggestionModal(field, currentValue, suggestion);
            
        } catch (error) {
            this.showAIError('AI assistant unavailable. Try again later.');
        }
    }
    
    showSuggestionModal(field, currentValue, suggestion) {
        const modal = new Modal({
            title: 'AI Suggestion',
            content: `
                <div class="ai-suggestion">
                    <div class="current-value">
                        <h4>Current:</h4>
                        <p>${currentValue || '<em>Empty</em>'}</p>
                    </div>
                    <div class="suggested-value">
                        <h4>Suggested:</h4>
                        <p contenteditable="true" id="ai-suggestion-text">
                            ${suggestion}
                        </p>
                    </div>
                </div>
            `,
            buttons: [
                {
                    text: 'Use Suggestion',
                    className: 'btn-primary',
                    onClick: () => {
                        const edited = document.getElementById('ai-suggestion-text').innerText;
                        field.value = edited;
                        this.markDirty();
                        modal.close();
                    }
                },
                {
                    text: 'Keep Current',
                    onClick: () => modal.close()
                }
            ]
        });
        modal.show();
    }
    
    async save() {
        try {
            const response = await fetch('/api/profile', {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(this.profileData)
            });
            
            if (!response.ok) throw new Error('Save failed');
            
            this.isDirty = false;
            this.showSuccessMessage('Profile saved');
            
        } catch (error) {
            this.showError('Failed to save profile');
        }
    }
}
```

### Photo Upload Component

```javascript
// photo-uploader.js
class PhotoUploader {
    constructor(entrantId) {
        this.entrantId = entrantId;
        this.maxFiles = 10;
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    }
    
    async upload(file) {
        // Validate file
        if (!this.validate(file)) {
            return;
        }
        
        // Show preview
        const preview = this.createPreview(file);
        this.showUploadProgress(preview);
        
        // Create form data
        const formData = new FormData();
        formData.append('photo', file);
        formData.append('caption', '');
        
        try {
            // Upload with progress tracking
            const response = await this.uploadWithProgress(formData, (progress) => {
                this.updateProgress(preview, progress);
            });
            
            const result = await response.json();
            
            // Update UI with uploaded photo
            this.showUploadedPhoto(result);
            
        } catch (error) {
            this.showUploadError(preview, error.message);
        }
    }
    
    validate(file) {
        if (!this.allowedTypes.includes(file.type)) {
            this.showError('Only JPEG, PNG, and WebP images are allowed');
            return false;
        }
        
        if (file.size > this.maxFileSize) {
            this.showError('File size must be less than 5MB');
            return false;
        }
        
        return true;
    }
    
    async uploadWithProgress(formData, onProgress) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const progress = (e.loaded / e.total) * 100;
                    onProgress(progress);
                }
            });
            
            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve(xhr.response);
                } else {
                    reject(new Error('Upload failed'));
                }
            });
            
            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });
            
            xhr.responseType = 'json';
            xhr.open('POST', '/api/profile/photo');
            xhr.send(formData);
        });
    }
    
    createPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.createElement('img');
            img.src = e.target.result;
            // Add to preview area
        };
        reader.readAsDataURL(file);
    }
}
```

## Performance Considerations

### Caching Strategy

```python
# cache_strategy.py

# In-memory cache for frequently accessed data
CACHE_CONFIG = {
    'profile_views': 3600,      # 1 hour
    'social_feeds': 900,        # 15 minutes
    'news_articles': 900,       # 15 minutes
    'user_sessions': 1800,      # 30 minutes
    'ai_responses': 86400,      # 24 hours (keyed by input hash)
    'public_profiles': 300,     # 5 minutes
}

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.expiry = {}
    
    def get(self, key):
        if key in self.cache:
            if datetime.now() < self.expiry[key]:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.expiry[key]
        return None
    
    def set(self, key, value, ttl):
        self.cache[key] = value
        self.expiry[key] = datetime.now() + timedelta(seconds=ttl)
    
    def invalidate(self, pattern):
        """Invalidate cache entries matching pattern"""
        keys_to_delete = [k for k in self.cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self.cache[key]
            del self.expiry[key]
```

### Database Optimization

- Indexes on frequently queried columns (user_id, entrant_id, created_at)
- Pagination for list endpoints (limit 20 items per page)
- Lazy loading of related data (don't fetch uploads unless needed)
- Connection pooling for database
- Read replicas for public profile views (future)
- Archive old audit log entries (> 1 year)

### Frontend Optimization

- Lazy load images with IntersectionObserver
- Debounce search inputs (300ms delay)
- Virtual scrolling for long lists
- Code splitting (separate bundles for authenticated vs public pages)
- Service worker for offline access to viewed profiles
- Progressive image loading (show thumbnail, then full size)
- Minify and compress JavaScript/CSS

## Security Considerations

### Input Validation

```python
# validators.py
from typing import Optional
import re

class ProfileValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_text_field(text: str, min_length: int, max_length: int) -> tuple[bool, Optional[str]]:
        if not text or len(text.strip()) < min_length:
            return False, f'Must be at least {min_length} characters'
        if len(text) > max_length:
            return False, f'Must be less than {max_length} characters'
        # Check for SQL injection patterns
        if any(pattern in text.lower() for pattern in ['<script', 'javascript:', 'onerror=']):
            return False, 'Invalid content detected'
        return True, None
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove potentially dangerous HTML"""
        import bleach
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li']
        return bleach.clean(text, tags=allowed_tags, strip=True)
```

### Rate Limiting

```python
# rate_limiter.py
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def allow_request(self, key: str, limit: int, window: int) -> bool:
        """
        Check if request is allowed
        key: identifier (e.g., user_id or IP address)
        limit: max requests in window
        window: time window in seconds
        """
        now = datetime.now()
        cutoff = now - timedelta(seconds=window)
        
        # Remove old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > cutoff
        ]
        
        # Check limit
        if len(self.requests[key]) >= limit:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True

# Usage in Flask
@app.before_request
def check_rate_limit():
    if request.endpoint in ['auth.login', 'profile.upload']:
        identifier = get_user_identifier()  # User ID or IP
        limits = {
            'auth.login': (5, 300),  # 5 requests per 5 minutes
            'profile.upload': (10, 3600)  # 10 uploads per hour
        }
        limit, window = limits.get(request.endpoint, (100, 60))
        
        if not rate_limiter.allow_request(identifier, limit, window):
            return jsonify({'error': 'Rate limit exceeded'}), 429
```

### CSRF Protection

```python
# csrf.py
import secrets
from flask import session

def generate_csrf_token():
    """Generate CSRF token for form"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def validate_csrf_token(token):
    """Validate CSRF token"""
    return token == session.get('csrf_token')

# Decorator for endpoints
def csrf_protect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
            if not validate_csrf_token(token):
                return jsonify({'error': 'Invalid CSRF token'}), 403
        return f(*args, **kwargs)
    return decorated_function
```

## Monitoring and Logging

### Application Logging

```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger('lateral_entry')
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler (rotating)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage
logger = setup_logging()
logger.info('User logged in', extra={'user_id': user_id})
logger.error('AI service failed', extra={'error': str(e)})
```

### Metrics Collection

```python
# metrics.py
from collections import defaultdict
from datetime import datetime

class MetricsCollector:
    def __init__(self):
        self.counters = defaultdict(int)
        self.timings = defaultdict(list)
    
    def increment(self, metric_name):
        """Increment a counter"""
        self.counters[metric_name] += 1
    
    def timing(self, metric_name, duration_ms):
        """Record a timing"""
        self.timings[metric_name].append(duration_ms)
    
    def get_stats(self):
        """Get current statistics"""
        stats = {
            'counters': dict(self.counters),
            'timings': {}
        }
        
        for metric, times in self.timings.items():
            if times:
                stats['timings'][metric] = {
                    'count': len(times),
                    'avg': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times)
                }
        
        return stats

metrics = MetricsCollector()

# Usage
@app.route('/api/profile')
def get_profile():
    start = time.time()
    try:
        # ... handle request
        metrics.increment('profile_views')
        return result
    finally:
        duration = (time.time() - start) * 1000
        metrics.timing('profile_load_time', duration)
```

## Testing Strategy

### Unit Tests

```python
# tests/test_profile_api.py
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Authenticated client"""
    # Create test user
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    return client

def test_get_profile_unauthenticated(client):
    """Should require authentication"""
    response = client.get('/api/profile')
    assert response.status_code == 401

def test_get_profile_authenticated(auth_client):
    """Should return profile data"""
    response = auth_client.get('/api/profile')
    assert response.status_code == 200
    data = response.get_json()
    assert 'name' in data
    assert 'email' in data

def test_update_profile(auth_client):
    """Should update profile fields"""
    response = auth_client.put('/api/profile', json={
        'profile_summary': 'New summary text'
    })
    assert response.status_code == 200
    
    # Verify update
    response = auth_client.get('/api/profile')
    data = response.get_json()
    assert data['profile_summary'] == 'New summary text'
```

### Integration Tests

```python
# tests/test_ai_integration.py
import pytest
from unittest.mock import Mock, patch

def test_ai_suggestion_success(auth_client):
    """Test successful AI suggestion"""
    with patch('ai_service.AIService.suggest_summary') as mock_ai:
        mock_ai.return_value = 'AI generated summary'
        
        response = auth_client.post('/api/ai/suggest-summary', json={
            'name': 'John Doe',
            'position': 'Joint Secretary',
            'experience': 'Banking expert'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['suggestion'] == 'AI generated summary'

def test_ai_suggestion_fallback(auth_client):
    """Test fallback when AI fails"""
    with patch('ai_service.AIService.suggest_summary') as mock_ai:
        mock_ai.side_effect = Exception('AI unavailable')
        
        response = auth_client.post('/api/ai/suggest-summary', json={
            'name': 'John Doe',
            'position': 'Joint Secretary'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['source'] == 'template'
        assert 'suggestion' in data
```

## Deployment Considerations

### Environment Variables

```bash
# .env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
DATABASE_URL=sqlite:///lateral_entry.db

# Authentication
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax

# File Upload
UPLOAD_FOLDER=/var/www/lateral-entry/uploads
MAX_CONTENT_LENGTH=10485760  # 10MB

# Custom AI Model
CUSTOM_AI_BASE_URL=<user-provides>
CUSTOM_AI_API_KEY=<user-provides>
CUSTOM_AI_MODEL=<user-provides>

# Parallel AI Monitor
PARALLEL_MONITOR_URL=<user-provides>
PARALLEL_MONITOR_API_KEY=<user-provides>

# Social Media APIs
TWITTER_API_KEY=<optional>
TWITTER_API_SECRET=<optional>
FACEBOOK_APP_ID=<optional>
FACEBOOK_APP_SECRET=<optional>
LINKEDIN_CLIENT_ID=<optional>
LINKEDIN_CLIENT_SECRET=<optional>

# Email (for password resets)
SMTP_HOST=<optional>
SMTP_PORT=587
SMTP_USER=<optional>
SMTP_PASSWORD=<optional>
SMTP_FROM_EMAIL=noreply@lateral-entry.gov.in

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/lateral-entry/app.log
```

### Database Migrations

```python
# migration_001_add_user_tables.py
def upgrade(db):
    """Add user authentication tables"""
    db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entrant_id INTEGER UNIQUE,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'appointee',
            is_verified BOOLEAN DEFAULT FALSE,
            is_active BOOLEAN DEFAULT TRUE,
            verification_token VARCHAR(255),
            reset_token VARCHAR(255),
            reset_token_expires TIMESTAMP,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id)
        )
    """)
    
    # Create indexes
    db.execute("CREATE INDEX idx_users_email ON users(email)")
    db.execute("CREATE INDEX idx_users_entrant_id ON users(entrant_id)")

def downgrade(db):
    """Remove user authentication tables"""
    db.execute("DROP TABLE IF EXISTS users")
```

## Admin Settings Configuration

### Configurable Settings System

The admin panel includes a comprehensive settings system that allows administrators to configure word limits, moderation workflows, and system behavior without code changes.

```python
# admin_settings.py
class AdminSettings:
    """Centralized configuration management"""
    
    # Default word limits for text fields
    DEFAULT_WORD_LIMITS = {
        'profile_summary': 200,
        'professional_experience': 150,
        'achievement_description': 100,
        'education_description': 75,
        'contact_info_note': 50,
        'social_media_bio': 30
    }
    
    # Moderation settings
    DEFAULT_MODERATION_CONFIG = {
        'require_upload_approval': True,
        'require_text_approval': True,
        'auto_approve_minor_edits': False,
        'flag_threshold_score': 0.7,  # AI flagging threshold
        'admin_notification_email': True,
        'daily_digest_enabled': True
    }
    
    # File upload limits
    DEFAULT_FILE_LIMITS = {
        'max_photo_size_mb': 5,
        'max_document_size_mb': 10,
        'max_photos_per_profile': 10,
        'max_documents_per_profile': 5,
        'total_storage_per_user_mb': 100
    }
    
    # AI assistance settings
    DEFAULT_AI_CONFIG = {
        'ai_enabled': True,
        'requests_per_user_per_hour': 10,
        'requests_per_user_per_day': 50,
        'show_ai_attribution': True,
        'log_ai_suggestions': True
    }
    
    def __init__(self, db_connection):
        self.db = db_connection
        self._load_settings()
    
    def _load_settings(self):
        """Load settings from database"""
        self.settings = {}
        rows = self.db.execute("SELECT key, value, value_type FROM admin_settings").fetchall()
        
        for row in rows:
            key = row['key']
            value = row['value']
            value_type = row['value_type']
            
            # Convert value to appropriate type
            if value_type == 'int':
                self.settings[key] = int(value)
            elif value_type == 'float':
                self.settings[key] = float(value)
            elif value_type == 'bool':
                self.settings[key] = value.lower() == 'true'
            else:
                self.settings[key] = value
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value, value_type='string'):
        """Update setting value"""
        # Update in database
        self.db.execute("""
            INSERT OR REPLACE INTO admin_settings (key, value, value_type, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, str(value), value_type))
        self.db.commit()
        
        # Update in memory
        if value_type == 'int':
            self.settings[key] = int(value)
        elif value_type == 'float':
            self.settings[key] = float(value)
        elif value_type == 'bool':
            self.settings[key] = value if isinstance(value, bool) else value.lower() == 'true'
        else:
            self.settings[key] = value
    
    def get_word_limit(self, field_name):
        """Get word limit for a specific field"""
        key = f'word_limit_{field_name}'
        return self.get(key, self.DEFAULT_WORD_LIMITS.get(field_name, 100))
    
    def set_word_limit(self, field_name, limit):
        """Set word limit for a specific field"""
        key = f'word_limit_{field_name}'
        self.set(key, limit, 'int')

# Database table for settings
CREATE TABLE admin_settings (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT NOT NULL,
    value_type VARCHAR(50) DEFAULT 'string', -- string, int, float, bool, json
    description TEXT,
    updated_by INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);
```

### Admin Settings API Endpoints

```python
# admin_routes.py

@admin_bp.route('/api/admin/settings', methods=['GET'])
@require_admin
def get_settings():
    """Get all configurable settings"""
    settings = admin_settings.settings
    
    return jsonify({
        'word_limits': {
            field: admin_settings.get_word_limit(field)
            for field in AdminSettings.DEFAULT_WORD_LIMITS.keys()
        },
        'moderation': {
            key: admin_settings.get(f'moderation_{key}')
            for key in AdminSettings.DEFAULT_MODERATION_CONFIG.keys()
        },
        'file_limits': {
            key: admin_settings.get(f'file_{key}')
            for key in AdminSettings.DEFAULT_FILE_LIMITS.keys()
        },
        'ai_config': {
            key: admin_settings.get(f'ai_{key}')
            for key in AdminSettings.DEFAULT_AI_CONFIG.keys()
        }
    })

@admin_bp.route('/api/admin/settings/word-limits', methods=['PUT'])
@require_admin
def update_word_limits():
    """Update word limits for fields"""
    data = request.json
    
    for field_name, limit in data.items():
        if not isinstance(limit, int) or limit < 10 or limit > 1000:
            return jsonify({'error': f'Invalid limit for {field_name}'}), 400
        
        admin_settings.set_word_limit(field_name, limit)
    
    # Log change
    audit_log.log(
        user_id=request.current_user['id'],
        action='update_word_limits',
        entity_type='admin_settings',
        new_value=json.dumps(data)
    )
    
    return jsonify({'success': True})

@admin_bp.route('/api/admin/settings/moderation', methods=['PUT'])
@require_admin
def update_moderation_settings():
    """Update moderation workflow settings"""
    data = request.json
    
    valid_keys = AdminSettings.DEFAULT_MODERATION_CONFIG.keys()
    for key, value in data.items():
        if key not in valid_keys:
            return jsonify({'error': f'Invalid setting: {key}'}), 400
        
        admin_settings.set(f'moderation_{key}', value, 'bool' if isinstance(value, bool) else 'string')
    
    audit_log.log(
        user_id=request.current_user['id'],
        action='update_moderation_settings',
        entity_type='admin_settings',
        new_value=json.dumps(data)
    )
    
    return jsonify({'success': True})

@admin_bp.route('/api/admin/settings/default-admin', methods=['POST'])
@require_admin
def create_default_admin():
    """Create the default admin user (can only be done once)"""
    # Check if default admin already exists
    existing_admin = db.execute("""
        SELECT id FROM users WHERE role = 'admin' AND email = ?
    """, (app.config['DEFAULT_ADMIN_EMAIL'],)).fetchone()
    
    if existing_admin:
        return jsonify({'error': 'Default admin already exists'}), 400
    
    # Create default admin with pre-approved status
    admin_data = {
        'google_id': f"default_admin_{secrets.token_hex(8)}",
        'email': app.config['DEFAULT_ADMIN_EMAIL'],
        'name': app.config['DEFAULT_ADMIN_NAME'],
        'role': 'admin',
        'is_approved': True,
        'is_active': True
    }
    
    db.execute("""
        INSERT INTO users (google_id, email, name, role, is_approved, is_active)
        VALUES (:google_id, :email, :name, :role, :is_approved, :is_active)
    """, admin_data)
    db.commit()
    
    return jsonify({'success': True, 'message': 'Default admin created'})
```

### Admin Settings UI

The admin panel includes a settings page where administrators can configure:

1. **Word Limits Tab**:
   - Profile summary: `200` words (default)
   - Professional experience: `150` words
   - Achievement description: `100` words
   - Education description: `75` words
   - Contact info note: `50` words
   - Social media bio: `30` words

2. **Moderation Tab**:
   - ☑ Require admin approval for uploads
   - ☑ Require admin approval for text edits
   - ☐ Auto-approve minor edits (typo fixes)
   - AI flagging threshold: `0.7` (0-1 scale)
   - ☑ Email notifications for new uploads
   - ☑ Daily digest of pending items

3. **File Limits Tab**:
   - Max photo size: `5` MB
   - Max document size: `10` MB
   - Max photos per profile: `10`
   - Max documents per profile: `5`
   - Total storage per user: `100` MB

4. **AI Configuration Tab**:
   - ☑ AI assistance enabled
   - Requests per hour: `10`
   - Requests per day: `50`
   - ☑ Show AI attribution
   - ☑ Log suggestions for training

5. **User Management Tab**:
   - Create default admin account
   - Configure admin email addresses
   - Set notification preferences

### Initial Setup Script

```python
# scripts/initialize_admin.py
"""
Initial setup script to create admin user and default settings
"""

def initialize_admin_system(db_connection):
    """Initialize admin system with default settings"""
    
    # Create default settings
    default_settings = []
    
    # Word limits
    for field, limit in AdminSettings.DEFAULT_WORD_LIMITS.items():
        default_settings.append((f'word_limit_{field}', str(limit), 'int'))
    
    # Moderation config
    for key, value in AdminSettings.DEFAULT_MODERATION_CONFIG.items():
        default_settings.append((f'moderation_{key}', str(value), 'bool' if isinstance(value, bool) else 'string'))
    
    # File limits
    for key, value in AdminSettings.DEFAULT_FILE_LIMITS.items():
        default_settings.append((f'file_{key}', str(value), 'int'))
    
    # AI config
    for key, value in AdminSettings.DEFAULT_AI_CONFIG.items():
        default_settings.append((f'ai_{key}', str(value), 'bool' if isinstance(value, bool) else 'int'))
    
    # Insert default settings
    db_connection.executemany("""
        INSERT OR IGNORE INTO admin_settings (key, value, value_type)
        VALUES (?, ?, ?)
    """, default_settings)
    
    db_connection.commit()
    print("✓ Default settings initialized")

if __name__ == '__main__':
    import sqlite3
    db = sqlite3.connect('database/lateral_entry.db')
    db.row_factory = sqlite3.Row
    
    initialize_admin_system(db)
    
    print("\nAdmin system initialized!")
    print("\nNext steps:")
    print("1. Set environment variables in .env:")
    print("   - DEFAULT_ADMIN_EMAIL=your-email@example.com")
    print("   - DEFAULT_ADMIN_NAME=Your Name")
    print("2. Run the application and visit /admin/setup")
    print("3. Complete Google OAuth setup")
```

### Word Limit Validation

```python
# validators.py (extended)

class WordLimitValidator:
    """Validate text against configurable word limits"""
    
    def __init__(self, admin_settings):
        self.settings = admin_settings
    
    def validate_field(self, field_name, text):
        """
        Validate that text meets word limit for field
        Returns: (is_valid, error_message, word_count, limit)
        """
        if not text:
            return True, None, 0, 0
        
        # Count words
        word_count = len(text.split())
        
        # Get limit for this field
        limit = self.settings.get_word_limit(field_name)
        
        if word_count > limit:
            return False, f"Text exceeds {limit} word limit ({word_count} words)", word_count, limit
        
        return True, None, word_count, limit
    
    def get_remaining_words(self, field_name, text):
        """Get remaining words for a field"""
        word_count = len(text.split()) if text else 0
        limit = self.settings.get_word_limit(field_name)
        return max(0, limit - word_count)

# Usage in API endpoint
@app.route('/api/profile/validate-field', methods=['POST'])
@require_auth
def validate_field():
    """Validate field content before saving"""
    data = request.json
    field_name = data.get('field_name')
    text = data.get('text')
    
    validator = WordLimitValidator(admin_settings)
    is_valid, error, word_count, limit = validator.validate_field(field_name, text)
    
    return jsonify({
        'valid': is_valid,
        'error': error,
        'word_count': word_count,
        'limit': limit,
        'remaining': limit - word_count if is_valid else 0
    })
```

### Frontend Word Counter

```javascript
// word-counter.js
class WordCounter {
    constructor(textarea, fieldName) {
        this.textarea = textarea;
        this.fieldName = fieldName;
        this.limit = null;
        this.counter = this.createCounter();
        this.init();
    }
    
    createCounter() {
        const counter = document.createElement('div');
        counter.className = 'word-counter';
        this.textarea.parentElement.appendChild(counter);
        return counter;
    }
    
    async init() {
        // Fetch word limit from API
        const response = await fetch('/api/admin/settings');
        const settings = await response.json();
        this.limit = settings.word_limits[this.fieldName];
        
        // Set up event listeners
        this.textarea.addEventListener('input', () => this.update());
        this.update();
    }
    
    update() {
        const text = this.textarea.value;
        const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
        const remaining = this.limit - wordCount;
        
        // Update counter display
        this.counter.textContent = `${wordCount} / ${this.limit} words`;
        
        // Color code based on remaining words
        if (remaining < 0) {
            this.counter.className = 'word-counter exceeded';
            this.textarea.classList.add('invalid');
        } else if (remaining < 10) {
            this.counter.className = 'word-counter warning';
            this.textarea.classList.remove('invalid');
        } else {
            this.counter.className = 'word-counter';
            this.textarea.classList.remove('invalid');
        }
    }
}

// Auto-initialize word counters
document.querySelectorAll('textarea[data-word-limit]').forEach(textarea => {
    const fieldName = textarea.getAttribute('data-word-limit');
    new WordCounter(textarea, fieldName);
});
```

## Trade-offs and Decisions

### Static vs Dynamic Deployment

**Decision**: Keep static JSON fallback, add optional API server

**Rationale**:
- Maintains current deployment simplicity
- Public viewing doesn't require backend
- Authentication and editing require backend
- Best of both worlds

### File Storage: Local vs Object Storage

**Decision**: Start with local filesystem, plan for S3-compatible storage later

**Rationale**:
- Simpler initial implementation
- No additional service dependencies
- Can migrate to S3/MinIO later without API changes
- Current traffic volume doesn't justify object storage yet

### Authentication: JWT vs Sessions

**Decision**: Server-side sessions with database storage

**Rationale**:
- Better security (can revoke sessions)
- Simpler logout implementation
- No token refresh complexity
- Audit trail of active sessions
- SQLite can handle session queries efficiently

### AI Integration: Synchronous vs Asynchronous

**Decision**: Synchronous API calls with timeout

**Rationale**:
- User expects immediate feedback for AI suggestions
- Timeout prevents hanging requests
- Simpler error handling
- Can add async/background generation later if needed

### Social Media: Real-time vs Cached

**Decision**: Cached feeds with 15-minute refresh

**Rationale**:
- Social media APIs have rate limits
- Real-time not necessary for this use case
- Better performance for users
- Reduces API costs
- Fallback to stale cache if API fails

## Open Issues for User Clarification

1. **AI Model Details**: Need exact API specifications
2. **Parallel AI Monitor**: Need configuration and API docs
3. **Social Media Access**: Need to confirm API access and costs
4. **Admin Approval**: Should content auto-publish or require review?
5. **Storage Limits**: What are total storage capacity constraints?
6. **Email Service**: Do we have SMTP server for password resets?
7. **Hosting**: Will backend run on same server or separate?
8. **SSL**: Is HTTPS already configured for prabhu.app?
9. **Backup**: What's the backup strategy for user-generated content?
10. **Timeline**: What's the desired launch date?
