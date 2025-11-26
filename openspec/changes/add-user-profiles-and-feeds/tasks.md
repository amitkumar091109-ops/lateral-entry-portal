# Implementation Tasks: Professional Networking Platform with Enhanced Features

**Change ID**: `add-user-profiles-and-feeds`  
**Status**: Planning  
**Last Updated**: 2025-11-26

## Overview

This document breaks down the implementation into manageable phases. Each phase is designed to deliver working functionality that can be tested and validated before moving to the next phase.

## NEW FEATURES ADDED:
- ✨ Project Rebranding (homepage title updates)
- ✨ Granular Visibility Controls (3-level permissions per field)
- ✨ LinkedIn Integration (OAuth sync + manual entry options)
- ✨ Comprehensive Job Monitoring (AI-powered with Parallel AI)

## Implementation Phases

### Phase 0: Project Rebranding (Week 1, Days 1-2)

**Goal**: Update display name and clarify portal purpose (quick wins)

#### 0.1 Update Display Strings
- [ ] Update index.html main heading and title tag
- [ ] Update all pages/*.html page titles
- [ ] Update manifest.json (name, short_name, description)
- [ ] Update constants in assets/js/main.js
- [ ] Update footer copyright text

**Files to Modify**:
- `index.html`
- `pages/*.html` (all pages)
- `manifest.json`
- `assets/js/main.js`

#### 0.2 Add Clarification Messaging
- [ ] Add info banner on homepage: "This is an information database, not an application portal"
- [ ] Update About section with clarification
- [ ] Add FAQ entry: "How do I apply for lateral entry?"
- [ ] Link to UPSC website for applications
- [ ] Update footer with clarification

**Files to Modify**:
- `index.html`
- `pages/faq.html`

#### 0.3 Update Meta Tags for SEO
- [ ] Update all title tags across pages
- [ ] Update all meta descriptions
- [ ] Update Open Graph tags
- [ ] Update Twitter Card tags
- [ ] Ensure keywords don't suggest application portal

**Files to Modify**:
- `index.html`
- `pages/*.html`

#### 0.4 Update Documentation
- [ ] Update README.md title and description
- [ ] Update PROJECT_SUMMARY.md
- [ ] Add "About the Rebranding" section
- [ ] Update deployment documentation

**Files to Modify**:
- `README.md`
- `PROJECT_SUMMARY.md`
- `DEPLOYMENT_GUIDE.md`

**Testing**:
- [ ] Verify all pages display new name
- [ ] Verify clarification message is prominent
- [ ] Check all internal links work
- [ ] Test on multiple browsers
- [ ] Validate SEO tags with tools

---

### Phase 1: Foundation & Google OAuth Authentication (Week 1-2)

**Goal**: Establish secure authentication system and admin infrastructure

#### 1.1 Database Schema Setup
- [ ] Create new database tables (users, pending_users, sessions, admin_settings, audit_log)
- [ ] Create field_visibility_settings table (for granular visibility)
- [ ] Add new columns to lateral_entrants table
- [ ] Create database indexes for performance
- [ ] Write migration script from current schema to new schema
- [ ] Test migration on backup database

**Files to Create/Modify**:
- `database/migrations/001_add_authentication.sql`
- `database/migrations/002_add_visibility_controls.sql`
- `database/lateral_entry_schema.sql` (update)

#### 1.2 Google OAuth Integration
- [ ] Install dependencies (google-auth-oauthlib, google-auth, cryptography)
- [ ] Create GoogleOAuthService class
- [ ] Implement token encryption utilities
- [ ] Create session management system
- [ ] Implement CSRF protection
- [ ] Add authentication decorators (@require_auth, @require_admin)

**Files to Create**:
- `api/auth/google_oauth.py`
- `api/auth/session_manager.py`
- `api/auth/decorators.py`
- `api/auth/__init__.py`

#### 1.3 Authentication API Endpoints
- [ ] POST /api/auth/google/login - Initiate OAuth flow
- [ ] GET /api/auth/google/callback - Handle OAuth callback
- [ ] POST /api/auth/logout - End session
- [ ] GET /api/auth/me - Get current user
- [ ] GET /api/auth/status - Check approval status

**Files to Create**:
- `api/routes/auth_routes.py`

#### 1.4 Admin Settings System
- [ ] Create AdminSettings class
- [ ] Initialize default settings in database
- [ ] Create admin settings API endpoints
- [ ] Build initialization script for first-time setup

**Files to Create**:
- `api/admin/admin_settings.py`
- `scripts/initialize_admin.py`

#### 1.5 Frontend - Authentication UI
- [ ] Create login page with "Sign in with Google" button
- [ ] Create pending approval page
- [ ] Create access requested page
- [ ] Add authentication state management
- [ ] Update navigation to show login/logout

**Files to Create**:
- `pages/login.html`
- `pages/pending-approval.html`
- `pages/access-requested.html`
- `assets/js/auth-client.js`

**Testing**:
- [ ] Test Google OAuth flow end-to-end
- [ ] Test session creation and validation
- [ ] Test CSRF protection
- [ ] Test token encryption/decryption
- [ ] Test admin settings CRUD operations

---

### Phase 2: Admin Panel & User Management (Week 3)

**Goal**: Enable admin approval workflow and user management

#### 2.1 Admin Backend
- [ ] GET /api/admin/pending-users - List pending access requests
- [ ] POST /api/admin/users/approve - Approve user and link to profile
- [ ] POST /api/admin/users/reject - Reject user request
- [ ] GET /api/admin/users - List all users
- [ ] PUT /api/admin/users/:id - Update user (activate/deactivate)
- [ ] DELETE /api/admin/users/:id - Delete user account
- [ ] GET /api/admin/audit-log - View audit log
- [ ] GET /api/admin/stats - System statistics

**Files to Create**:
- `api/routes/admin_routes.py`
- `api/admin/user_manager.py`

#### 2.2 Admin Frontend
- [ ] Create admin dashboard page
- [ ] Create pending users approval interface
- [ ] Create user management table
- [ ] Create settings configuration UI
- [ ] Create audit log viewer
- [ ] Add admin navigation

**Files to Create**:
- `pages/admin/dashboard.html`
- `pages/admin/pending-users.html`
- `pages/admin/users.html`
- `pages/admin/settings.html`
- `pages/admin/audit-log.html`
- `assets/js/admin-client.js`

#### 2.3 Email Notifications (Optional)
- [ ] Configure SMTP settings
- [ ] Create email templates
- [ ] Implement notification service
- [ ] Send notifications on user approval/rejection

**Files to Create**:
- `api/notifications/email_service.py`
- `api/notifications/templates/`

**Testing**:
- [ ] Test admin approval workflow
- [ ] Test user linking to profiles
- [ ] Test user activation/deactivation
- [ ] Test audit log tracking
- [ ] Test email notifications (if implemented)

---

### Phase 3: Granular Visibility Controls (Week 4)

**Goal**: Implement 3-level field visibility (Public/Lateral Entrants Only/Private)

#### 3.1 Visibility Control Backend
- [ ] Create VisibilityManager class
- [ ] GET /api/profile/:id/visibility - Get visibility settings
- [ ] PUT /api/profile/visibility/:field - Update single field visibility
- [ ] PUT /api/profile/visibility/bulk - Update multiple fields
- [ ] GET /api/visibility/audit-log - Get visibility change history
- [ ] Implement visibility filtering in profile API
- [ ] Add middleware to enforce visibility based on authentication

**Files to Create**:
- `api/visibility/visibility_manager.py`
- `api/visibility/visibility_middleware.py`
- `api/routes/visibility_routes.py`

#### 3.2 Update Profile API with Visibility Filtering
- [ ] Modify GET /api/profile/:id to filter by visibility
- [ ] Add logic to detect authentication status (unauthenticated, authenticated lateral entrant, owner)
- [ ] Return different fields based on viewer type
- [ ] Include visibility metadata in owner's profile response

**Files to Modify**:
- `api/routes/profile_routes.py`

#### 3.3 Frontend - Visibility Controls UI
- [ ] Create inline visibility toggles in profile editor
- [ ] Build visibility dropdown component (Public/Lateral Entrants Only/Private)
- [ ] Add visual indicators (🌐 🔒 👁️) for each visibility level
- [ ] Create bulk visibility management modal
- [ ] Add visibility preview mode ("View as Public", "View as Lateral Entrant")
- [ ] Show restricted field placeholders on public profiles

**Files to Create**:
- `assets/js/visibility-controls.js`
- `assets/css/visibility-controls.css`

**Files to Modify**:
- `pages/profile-editor.html`
- `pages/profile-detail.html`

#### 3.4 Search and Browse with Visibility
- [ ] Update search to respect visibility controls
- [ ] Update browse/listing pages to filter by visibility
- [ ] Add indicators for restricted content

**Files to Modify**:
- `assets/js/search.js`
- `pages/profiles.html`

**Testing**:
- [ ] Test visibility setting for each field
- [ ] Test public visitor sees only "Public" fields
- [ ] Test authenticated lateral entrant sees "Public" + "Lateral Entrants Only"
- [ ] Test owner sees all fields
- [ ] Test API properly filters responses
- [ ] Test audit log captures visibility changes
- [ ] Test search respects visibility
- [ ] Test no data leakage via API

---

### Phase 4: Profile Editing & Field Management (Week 5)

**Goal**: Allow authenticated users to edit their profile fields (with moderation)

#### 4.1 Profile API Backend
- [ ] GET /api/profile - Get own profile (authenticated)
- [ ] GET /api/profile/:id - Get public/visible profile
- [ ] POST /api/edit-requests - Request field edit
- [ ] GET /api/edit-requests - Get own edit requests
- [ ] DELETE /api/edit-requests/:id - Cancel edit request
- [ ] Implement field validation with word limits
- [ ] POST /api/profile/validate-field - Validate field before saving

**Files to Create**:
- `api/routes/profile_routes.py` (extend)
- `api/profile/profile_manager.py`
- `api/profile/validators.py`

#### 4.2 Moderation Queue Backend
- [ ] GET /api/admin/edit-requests - List pending edits
- [ ] POST /api/admin/edit-requests/:id/approve - Approve edit
- [ ] POST /api/admin/edit-requests/:id/reject - Reject edit
- [ ] Implement diff viewer for changes

**Files to Modify**:
- `api/routes/admin_routes.py` (extend)

#### 4.3 Profile Editor Frontend
- [ ] Create profile editor page
- [ ] Build form with editable fields
- [ ] Implement word counter components
- [ ] Add real-time validation
- [ ] Show pending edits status
- [ ] Auto-save functionality

**Files to Create**:
- `pages/profile-editor.html`
- `assets/js/profile-editor.js`
- `assets/js/word-counter.js`
- `assets/css/profile-editor.css`

#### 4.4 Admin Moderation Frontend
- [ ] Create edit requests moderation page
- [ ] Build diff viewer component
- [ ] Add approve/reject actions
- [ ] Show edit request history

**Files to Create**:
- `pages/admin/moderation.html`
- `assets/js/diff-viewer.js`

**Testing**:
- [ ] Test profile field editing
- [ ] Test word limit validation
- [ ] Test edit request workflow
- [ ] Test admin approval/rejection
- [ ] Test auto-save functionality

---

### Phase 5: File Uploads & Media Management (Week 6-7)

**Goal**: Enable photo and document uploads with moderation

#### 5.1 File Upload Backend
- [ ] POST /api/uploads/photo - Upload photo
- [ ] POST /api/uploads/document - Upload document
- [ ] DELETE /api/uploads/:id - Delete own upload
- [ ] PUT /api/uploads/:id/caption - Update caption
- [ ] GET /api/uploads/pending - Get own pending uploads
- [ ] Implement file validation (type, size, magic bytes)
- [ ] Implement image processing (resize, optimize, WebP conversion)
- [ ] Create upload storage structure

**Files to Create**:
- `api/routes/upload_routes.py`
- `api/uploads/upload_manager.py`
- `api/uploads/image_processor.py`
- `api/uploads/file_validator.py`

#### 5.2 Upload Moderation Backend
- [ ] GET /api/admin/pending-uploads - List uploads awaiting moderation
- [ ] POST /api/admin/uploads/:id/approve - Approve upload
- [ ] POST /api/admin/uploads/:id/reject - Reject upload
- [ ] Implement storage quota checking

**Files to Modify**:
- `api/routes/admin_routes.py` (extend)

#### 5.3 Photo Upload Frontend
- [ ] Create photo uploader component
- [ ] Build drag-and-drop interface
- [ ] Add upload progress indicator
- [ ] Show preview before upload
- [ ] Display uploaded photos with status
- [ ] Add caption editing

**Files to Create**:
- `assets/js/photo-uploader.js`
- `assets/css/uploader.css`

#### 5.4 Document Upload Frontend
- [ ] Create document uploader component
- [ ] Show upload status
- [ ] Display document list

**Files to Create**:
- `assets/js/document-uploader.js`

#### 5.5 Upload Moderation Frontend
- [ ] Create upload moderation page
- [ ] Build image preview gallery
- [ ] Add approve/reject actions
- [ ] Show upload metadata

**Files to Create**:
- `pages/admin/uploads.html`
- `assets/js/upload-moderator.js`

**Testing**:
- [ ] Test photo upload (various formats)
- [ ] Test document upload (PDF)
- [ ] Test file size validation
- [ ] Test file type validation
- [ ] Test image processing (resize, optimize)
- [ ] Test upload moderation workflow
- [ ] Test storage quota limits

---

### Phase 6: LinkedIn Integration (Week 8)

**Goal**: Integrate LinkedIn OAuth sync and manual entry options

#### 6.1 LinkedIn OAuth Backend
- [ ] Install linkedin-api-client library
- [ ] Create LinkedInOAuthService class
- [ ] POST /api/linkedin/connect - Initiate LinkedIn OAuth
- [ ] GET /api/linkedin/callback - Handle OAuth callback
- [ ] POST /api/linkedin/disconnect - Disconnect LinkedIn
- [ ] GET /api/linkedin/profile - Fetch LinkedIn data
- [ ] Implement token encryption for LinkedIn tokens
- [ ] Create LinkedInFieldMapper class

**Files to Create**:
- `api/linkedin/linkedin_oauth.py`
- `api/linkedin/field_mapper.py`
- `api/routes/linkedin_routes.py`

#### 6.2 LinkedIn Sync Backend
- [ ] POST /api/linkedin/sync - Sync LinkedIn data to profile
- [ ] GET /api/linkedin/mappings - Get field mappings
- [ ] PUT /api/linkedin/mappings - Update field mappings
- [ ] GET /api/linkedin/sync-history - Get sync history
- [ ] Implement rate limiting (10 syncs per hour)
- [ ] Handle LinkedIn API errors gracefully

**Files to Modify**:
- `api/routes/linkedin_routes.py` (extend)

#### 6.3 Frontend - LinkedIn Connection UI
- [ ] Add LinkedIn connection settings in profile settings
- [ ] Create "Connect LinkedIn (OAuth)" button
- [ ] Create "Add LinkedIn URL Manually" button
- [ ] Build field mapping configuration modal
- [ ] Show LinkedIn connection status
- [ ] Add "Sync Now" button
- [ ] Display last sync timestamp

**Files to Create**:
- `assets/js/linkedin-integration.js`
- `assets/css/linkedin-ui.css`

**Files to Modify**:
- `pages/profile-editor.html` (add LinkedIn section)

#### 6.4 Frontend - LinkedIn-Style Layout
- [ ] Update profile display with LinkedIn-inspired design
- [ ] Add professional header layout
- [ ] Update experience section with timeline
- [ ] Update education section styling
- [ ] Add skills section with visual display

**Files to Modify**:
- `pages/profile-detail.html`
- `assets/css/profile-layout.css`

**Testing**:
- [ ] Test LinkedIn OAuth flow
- [ ] Test field mapping configuration
- [ ] Test sync functionality
- [ ] Test manual URL entry
- [ ] Test token refresh
- [ ] Test rate limiting
- [ ] Test disconnect flow
- [ ] Test LinkedIn-style layout display

---

### Phase 7: AI Assistance Integration (Week 9)

**Goal**: Integrate custom AI model for content generation

#### 7.1 AI Service Backend
- [ ] Create AIService class
- [ ] Implement AI API client
- [ ] Add rate limiting for AI requests
- [ ] Implement fallback to templates
- [ ] Create prompt templates
- [ ] POST /api/ai/suggest-summary - Generate profile summary
- [ ] POST /api/ai/suggest-achievement - Generate achievement text
- [ ] POST /api/ai/improve-text - Improve/grammar check
- [ ] GET /api/ai/usage - Get AI usage stats

**Files to Create**:
- `api/ai/ai_service.py`
- `api/ai/rate_limiter.py`
- `api/ai/prompt_templates.py`
- `api/ai/template_fallback.py`
- `api/routes/ai_routes.py`

#### 7.2 AI Assistant Frontend
- [ ] Create AIAssistant JavaScript class
- [ ] Add AI suggestion buttons to text fields
- [ ] Build suggestion modal component
- [ ] Show AI loading states
- [ ] Display AI suggestions with edit capability
- [ ] Track AI usage stats

**Files to Create**:
- `assets/js/ai-assistant.js`
- `assets/js/suggestion-modal.js`
- `assets/css/ai-assistant.css`

**Testing**:
- [ ] Test AI API integration
- [ ] Test summary generation
- [ ] Test achievement text generation
- [ ] Test text improvement
- [ ] Test rate limiting
- [ ] Test fallback when AI unavailable
- [ ] Test AI suggestion acceptance/rejection

---

### Phase 8: Comprehensive Job Monitoring (Week 10-11)

**Goal**: AI-powered job vacancy monitoring across thousands of organizations

#### 8.1 Job Monitoring Backend
- [ ] Create JobMonitor class
- [ ] Integrate Parallel AI Monitor API
- [ ] Create job relevance scoring algorithm
- [ ] Create database tables (job_listings, user_job_preferences, etc.)
- [ ] Implement hourly monitoring job for government orgs
- [ ] Implement daily monitoring job for private sector
- [ ] GET /api/jobs - Get job listings (with filters)
- [ ] GET /api/jobs/:id - Get job details
- [ ] GET /api/jobs/search - Search jobs
- [ ] GET /api/jobs/recommended - Get personalized recommendations

**Files to Create**:
- `api/jobs/job_monitor.py`
- `api/jobs/relevance_scorer.py`
- `api/routes/job_routes.py`
- `database/migrations/003_add_job_monitoring.sql`

#### 8.2 User Job Preferences Backend
- [ ] GET /api/job-preferences - Get user preferences
- [ ] PUT /api/job-preferences - Update preferences
- [ ] Calculate match percentages for jobs based on preferences
- [ ] Implement job filtering by user preferences

**Files to Modify**:
- `api/routes/job_routes.py` (extend)

#### 8.3 Job Notifications Backend
- [ ] Create JobNotificationService class
- [ ] Detect high-relevance jobs (score ≥ 80)
- [ ] Send in-app notifications
- [ ] Send email notifications (if enabled)
- [ ] Implement weekly job digest email
- [ ] GET /api/job-notifications - Get notifications
- [ ] PUT /api/job-notifications/:id/read - Mark as read

**Files to Create**:
- `api/jobs/notification_service.py`
- `api/routes/notification_routes.py`

#### 8.4 Saved Jobs Backend
- [ ] POST /api/jobs/:id/save - Save job
- [ ] DELETE /api/jobs/:id/save - Remove saved job
- [ ] GET /api/jobs/saved - Get saved jobs
- [ ] PUT /api/jobs/:id/status - Update application status

**Files to Modify**:
- `api/routes/job_routes.py` (extend)

#### 8.5 Frontend - Job Board (Authenticated Only)
- [ ] Create job board main page
- [ ] Build job listing cards
- [ ] Add search and filter sidebar
- [ ] Implement pagination (20 per page)
- [ ] Show match percentages
- [ ] Add "View All" vs "Personalized" toggle
- [ ] Create job detail page
- [ ] Add "Save Job" functionality
- [ ] Create "My Saved Jobs" page

**Files to Create**:
- `pages/job-board.html`
- `pages/job-detail.html`
- `pages/saved-jobs.html`
- `assets/js/job-board.js`
- `assets/css/job-board.css`

#### 8.6 Frontend - Job Preferences
- [ ] Create job preferences settings page
- [ ] Build preference form (position level, domain, location)
- [ ] Add notification settings toggle
- [ ] Display match breakdown on job details

**Files to Create**:
- `pages/job-preferences.html`
- `assets/js/job-preferences.js`

#### 8.7 Admin Job Monitoring Configuration
- [ ] GET /api/admin/job-monitoring/config - Get config
- [ ] PUT /api/admin/job-monitoring/config - Update Parallel AI prompt
- [ ] POST /api/admin/job-monitoring/test - Test prompt
- [ ] GET /api/admin/job-monitoring/stats - Get statistics
- [ ] GET /api/admin/job-monitoring/history - Get monitoring history
- [ ] POST /api/admin/jobs - Manually add job
- [ ] DELETE /api/admin/jobs/:id - Remove job
- [ ] GET /api/admin/organizations - Manage monitored orgs
- [ ] POST /api/admin/organizations - Add organization

**Files to Create**:
- `pages/admin/job-monitoring.html`
- `pages/admin/job-config.html`
- `assets/js/admin-job-monitoring.js`

#### 8.8 Background Jobs Setup
- [ ] Install APScheduler
- [ ] Create job monitoring scheduler
- [ ] Add hourly job: monitor government organizations
- [ ] Add daily job: monitor private sector
- [ ] Add weekly job: send job digest emails
- [ ] Add job: cleanup old job listings (>90 days)

**Files to Create**:
- `api/jobs/scheduler.py`
- `api/jobs/monitoring_jobs.py`

**Testing**:
- [ ] Test Parallel AI Monitor integration
- [ ] Test job relevance scoring
- [ ] Test user preference matching
- [ ] Test job board display and filtering
- [ ] Test search functionality
- [ ] Test saved jobs workflow
- [ ] Test notification delivery
- [ ] Test weekly digest generation
- [ ] Test admin configuration
- [ ] Test background job execution
- [ ] Test manual job addition by admin

---

### Phase 9: Social Media Feeds (Week 12) [OPTIONAL]

**Goal**: Display social media feeds on homepage (optional feature)

#### 9.1 Social Media Integration Backend
- [ ] Create FeedAggregator class
- [ ] Implement X/Twitter API client
- [ ] Implement Facebook Graph API client
- [ ] Implement LinkedIn API client
- [ ] Build feed caching system
- [ ] Create relevance scoring algorithm
- [ ] GET /api/feeds/social - Get social feed items
- [ ] GET /api/feeds/news - Get news articles
- [ ] GET /api/feeds/combined - Get combined feed
- [ ] POST /api/feeds/refresh - Trigger manual refresh (admin)

**Files to Create**:
- `api/feeds/feed_aggregator.py`
- `api/feeds/twitter_client.py`
- `api/feeds/facebook_client.py`
- `api/feeds/linkedin_client.py`
- `api/feeds/cache_manager.py`
- `api/routes/feed_routes.py`

#### 9.2 Background Jobs Setup
- [ ] Add feed refresh job (every 15 minutes)
- [ ] Add cache cleanup job (daily)

**Files to Modify**:
- `api/jobs/scheduler.py` (extend)

#### 9.3 Social Feeds Frontend
- [ ] Create FeedManager JavaScript class
- [ ] Build feed display component
- [ ] Create feed item templates (tweet, Facebook post, LinkedIn post)
- [ ] Implement infinite scroll
- [ ] Add feed refresh button
- [ ] Display feed on homepage

**Files to Create**:
- `assets/js/feed-manager.js`
- `assets/js/feed-templates.js`
- `assets/css/social-feeds.css`

**Files to Modify**:
- `index.html` (add feed section)

**Testing**:
- [ ] Test X/Twitter API integration
- [ ] Test Facebook API integration
- [ ] Test LinkedIn API integration
- [ ] Test feed caching
- [ ] Test relevance scoring
- [ ] Test background job scheduling
- [ ] Test feed display on homepage
- [ ] Test infinite scroll

---

### Phase 10: News Monitoring (Week 13)

**Goal**: Monitor and display news articles about lateral entry

#### 10.1 News Monitoring Backend
- [ ] Create NewsMonitor class
- [ ] Integrate Parallel AI Monitor for news
- [ ] Build keyword extraction system
- [ ] Implement relevance scoring for articles
- [ ] Store news articles in database
- [ ] Add hourly monitoring job
- [ ] Send notifications for high-relevance articles

**Files to Create**:
- `api/news/news_monitor.py`
- `api/news/keyword_extractor.py`
- `api/news/article_scorer.py`

**Files to Modify**:
- `api/jobs/scheduler.py` (add news monitoring job)
- `api/routes/feed_routes.py` (already created in Phase 9)

#### 10.2 News Display Frontend
- [ ] Create news article template
- [ ] Build news section on homepage
- [ ] Add filtering by relevance
- [ ] Display article summaries

**Files to Modify**:
- `assets/js/feed-manager.js` (extend)
- `assets/js/feed-templates.js` (add news template)

#### 10.3 Admin Configuration
- [ ] GET /api/admin/news-keywords - Get monitoring keywords
- [ ] POST /api/admin/news-keywords - Add keyword
- [ ] DELETE /api/admin/news-keywords/:id - Remove keyword
- [ ] Create news monitoring configuration UI

**Files to Create**:
- `pages/admin/news-config.html`

**Testing**:
- [ ] Test Parallel AI Monitor integration
- [ ] Test keyword extraction
- [ ] Test relevance scoring
- [ ] Test news article storage
- [ ] Test hourly monitoring job
- [ ] Test news display on homepage
- [ ] Test admin keyword management

---

### Phase 11: Testing, Security & Performance (Week 14)

**Goal**: Comprehensive testing and optimization

#### 11.1 Security Hardening
- [ ] Implement rate limiting on all endpoints
- [ ] Add content security policy headers
- [ ] Configure CORS properly
- [ ] Implement virus scanning on uploads (optional: ClamAV)
- [ ] Add SQL injection protection review
- [ ] Implement XSS protection review
- [ ] Add security headers (X-Frame-Options, etc.)
- [ ] Test visibility controls for data leakage
- [ ] Test LinkedIn token encryption
- [ ] Test job board authorization

**Files to Create**:
- `api/security/rate_limiter.py`
- `api/security/content_scanner.py`

#### 11.2 Performance Optimization
- [ ] Add database indexes (especially for visibility lookups, job queries)
- [ ] Implement query optimization
- [ ] Add CDN configuration for static assets
- [ ] Optimize image loading (lazy load, WebP)
- [ ] Implement service worker for offline access
- [ ] Add compression for API responses
- [ ] Test job board performance with 10,000+ listings
- [ ] Optimize visibility filtering queries

**Files to Create**:
- `assets/js/service-worker.js`
- `api/middleware/compression.py`

#### 11.3 Testing
- [ ] Write unit tests for authentication
- [ ] Write unit tests for visibility controls
- [ ] Write unit tests for profile API
- [ ] Write unit tests for LinkedIn integration
- [ ] Write unit tests for job monitoring
- [ ] Write unit tests for uploads
- [ ] Write integration tests for AI service
- [ ] Write integration tests for social feeds
- [ ] Write end-to-end tests for user workflows
- [ ] Load testing on API endpoints
- [ ] Security testing (penetration testing)

**Files to Create**:
- `tests/test_auth.py`
- `tests/test_visibility.py`
- `tests/test_profile.py`
- `tests/test_linkedin.py`
- `tests/test_jobs.py`
- `tests/test_uploads.py`
- `tests/test_ai.py`
- `tests/test_feeds.py`
- `tests/test_integration.py`

#### 11.4 Documentation
- [ ] Create API documentation
- [ ] Write user guide for appointees
- [ ] Write admin manual
- [ ] Create deployment guide
- [ ] Document configuration options
- [ ] Document LinkedIn integration setup
- [ ] Document job monitoring configuration
- [ ] Document visibility controls usage

**Files to Create**:
- `docs/API.md`
- `docs/USER_GUIDE.md`
- `docs/ADMIN_MANUAL.md`
- `docs/DEPLOYMENT.md`
- `docs/LINKEDIN_SETUP.md`
- `docs/JOB_MONITORING_SETUP.md`

**Testing**:
- [ ] Security audit
- [ ] Performance benchmarks
- [ ] Cross-browser testing
- [ ] Mobile responsiveness testing
- [ ] Accessibility testing (WCAG 2.1 AA)

---

### Phase 12: Deployment & Launch (Week 15-16)

**Goal**: Deploy to production and launch

#### 12.1 Pre-deployment
- [ ] Set up production environment variables
- [ ] Configure Google OAuth production credentials
- [ ] Configure LinkedIn OAuth production credentials (if using)
- [ ] Configure Parallel AI Monitor for jobs AND news
- [ ] Set up production database
- [ ] Configure file storage
- [ ] Set up SSL certificates
- [ ] Configure backup system

#### 12.2 Deployment
- [ ] Run database migrations on production
- [ ] Deploy backend API
- [ ] Deploy frontend assets
- [ ] Configure web server (nginx/Apache)
- [ ] Set up background job runner (for job monitoring, news monitoring)
- [ ] Initialize admin settings
- [ ] Create default admin account
- [ ] Verify all environment variables

#### 12.3 Post-deployment
- [ ] Smoke testing on production
- [ ] Test authentication flow
- [ ] Test visibility controls
- [ ] Test LinkedIn integration
- [ ] Test job board access
- [ ] Test job monitoring runs
- [ ] Monitor logs for errors
- [ ] Set up monitoring alerts
- [ ] Create backup restoration procedure
- [ ] Document rollback procedure

#### 12.4 Launch
- [ ] Send invitations to lateral entry appointees
- [ ] Provide user onboarding materials
- [ ] Announce job board feature
- [ ] Monitor system performance
- [ ] Collect user feedback
- [ ] Address initial issues
- [ ] Monitor job monitoring effectiveness

---

## Task Dependencies

```
Phase 0 (Rebranding) → Independent (can be done first)
Phase 1 (Auth) → Phase 2 (Admin) → Phase 3 (Visibility) → Phase 4 (Profile Edit)
                                   → Phase 5 (Uploads)
                                   
Phase 6 (LinkedIn) → Requires Phase 1, 3, 4
Phase 7 (AI) → Requires Phase 4
Phase 8 (Job Monitoring) → Requires Phase 1, 3 (for authentication and visibility)
Phase 9 (Social Feeds) → Independent (optional)
Phase 10 (News) → Can run parallel to Phase 9
Phase 11 (Testing) → Requires all above phases
Phase 12 (Deployment) → Requires Phase 11
```

## Estimated Timeline

- **Phase 0**: 2 days (Project Rebranding)
- **Phase 1**: 2 weeks (Authentication)
- **Phase 2**: 1 week (Admin Panel)
- **Phase 3**: 1 week (Granular Visibility)
- **Phase 4**: 1 week (Profile Editing)
- **Phase 5**: 2 weeks (File Uploads)
- **Phase 6**: 1 week (LinkedIn Integration)
- **Phase 7**: 1 week (AI Assistance)
- **Phase 8**: 2 weeks (Job Monitoring) ⭐ NEW
- **Phase 9**: 1 week (Social Feeds - Optional)
- **Phase 10**: 1 week (News Monitoring)
- **Phase 11**: 1 week (Testing & Security)
- **Phase 12**: 1 week (Deployment)

**Total**: ~15-16 weeks (3.5-4 months)

## Prerequisites Before Starting

### Environment Setup
1. **Google OAuth Credentials**:
   - Create OAuth 2.0 Client ID in Google Cloud Console
   - Configure authorized redirect URIs
   - Obtain Client ID and Client Secret

2. **Custom AI Model**:
   - Base URL for AI API
   - API authentication key
   - Model name/version
   - Rate limit specifications

3. **Parallel AI Monitor** (Enhanced for Jobs + News):
   - Monitor API URL
   - API authentication key
   - **Job Monitoring Prompt**: Comprehensive list of organizations to monitor (user to provide)
   - **News Monitoring Prompt**: Keywords for news tracking
   - Configuration documentation

4. **LinkedIn OAuth** (Optional, for real-time sync):
   - LinkedIn App ID and App Secret
   - Configure authorized redirect URIs
   - Understand LinkedIn API rate limits

5. **Social Media APIs** (Optional, for Phase 9):
   - X/Twitter API keys
   - Facebook App ID and Secret
   - LinkedIn Client ID and Secret

6. **Email Service** (Optional):
   - SMTP server details
   - Authentication credentials

7. **Infrastructure**:
   - Production server with Python 3.13+
   - Sufficient storage for file uploads
   - SSL certificate for HTTPS
   - Domain name configured

### Dependencies to Install
```bash
pip install flask flask-cors
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install cryptography
pip install pillow  # Image processing
pip install httpx  # Async HTTP client
pip install apscheduler  # Background jobs
pip install bleach  # HTML sanitization
pip install pytest pytest-cov  # Testing
pip install linkedin-api-client  # LinkedIn integration (if using)
```

## Risk Mitigation

### Critical Risks
1. **Google OAuth Configuration**: Test thoroughly in development before production
2. **File Upload Security**: Implement all validation and scanning measures
3. **Visibility Controls**: Thoroughly test for data leakage
4. **LinkedIn API Availability**: Ensure fallback to manual entry works
5. **Job Monitoring Scale**: Test Parallel AI with large organization lists
6. **AI API Availability**: Ensure fallback mechanisms work
7. **Background Jobs**: Ensure scheduler is reliable and monitored

### Rollback Plan
- Keep database migrations reversible
- Maintain previous version deployment package
- Document rollback procedure for each phase
- Test rollback procedures before production deployment

## Success Metrics

Track these metrics throughout implementation:

- [ ] Authentication success rate > 99%
- [ ] Page load time < 3 seconds
- [ ] File upload success rate > 95%
- [ ] AI suggestion generation time < 5 seconds
- [ ] Zero SQL injection vulnerabilities
- [ ] Zero XSS vulnerabilities
- [ ] Zero visibility control bypass vulnerabilities
- [ ] 100% test coverage on critical paths
- [ ] **Visibility controls properly enforce access (0 data leakage)**
- [ ] **LinkedIn sync success rate > 90%**
- [ ] **Job board loads in < 2 seconds**
- [ ] **Job monitoring finds > 50 relevant jobs per week**
- [ ] **>50% of authenticated users visit job board**
- [ ] **>30% of users set granular visibility preferences**

## Next Steps

1. **User to provide**:
   - Final project name (e.g., "Lateral Entry Officers Database")
   - Google OAuth credentials
   - Custom AI Model configuration
   - **Parallel AI Monitor comprehensive job monitoring prompt**
   - LinkedIn OAuth credentials (if users want real-time sync)
   - Social media API access (if Phase 9 desired)
   - Default admin credentials

2. **Review and approve** this task breakdown

3. **Begin Phase 0** (Project Rebranding - quick wins in 2 days)

4. **Then proceed to Phase 1** (Authentication foundation)
