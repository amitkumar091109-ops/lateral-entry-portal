# Proposal: Transform Portal into Professional Networking Platform

**Change ID**: `add-user-profiles-and-feeds`  
**Status**: Draft  
**Created**: 2025-11-25  
**Last Updated**: 2025-11-26  
**Author**: System (based on user requirements)

## Summary

Transform the "Lateral Entry Portal" into a comprehensive professional networking and information platform for lateral entry officers in the Government of India. This change introduces:

1. **Project Rebranding**: Rename from "Lateral Entry Portal" to better reflect its purpose as an officers' database and professional network
2. **User-Controlled Profiles**: Each lateral entrant manages their own profile with granular visibility controls (Public, Lateral Entrants Only, Private)
3. **LinkedIn Integration**: Optional real-time LinkedIn profile sync to auto-populate profile fields
4. **Comprehensive Job Monitoring**: AI-powered job vacancy tracking across thousands of public and private sector organizations
5. **Enhanced Content Platform**: Moderated space for news, updates, and professional networking among lateral entrants

## Motivation

### Current State
- Portal name "Lateral Entry Portal" suggests it facilitates lateral entry applications, which is misleading
- Portal displays static, read-only profiles managed by portal administrators
- No way for appointees to update their own information or control what's visible to public vs authenticated users
- No professional networking features or LinkedIn integration
- No comprehensive job vacancy monitoring for lateral entry opportunities
- Profile content is manually curated with limited detail
- No moderated content management system for appointees

### Desired State
- **Project Rebranding**: Rename to "Lateral Entry Officers Database" or similar to accurately reflect purpose as an information repository, not an application portal
- **Granular Privacy Controls**: Each profile field has three visibility options:
  1. **Public** - Visible to all visitors without login
  2. **Lateral Entrants Only** - Visible only to authenticated lateral entry officers
  3. **Private** - Visible only to the profile owner
- **LinkedIn Integration Options**:
  - **Option 1 (User Choice)**: Lateral entrant can link their LinkedIn account via OAuth and sync profile data in real-time
  - **Option 2 (Manual)**: Lateral entrant can manually add LinkedIn profile URL and copy specific fields they choose
  - Profile layout adopts LinkedIn-style professional design
- **Comprehensive Job Monitoring**: 
  - AI-powered monitoring (Parallel AI) searches thousands of organizations (public & private sector)
  - Customized by position level (JS/DS/Director), domain expertise, and location preferences
  - Vacancy notifications and curated job board for authenticated users
- **Professional Networking Hub**: Single place for all news, updates, and resources relevant to lateral entrants
- **User-Controlled Content**: Each appointee manages their profile through moderated approval workflow

## Problems Solved

1. **Misleading Branding**: Portal name no longer suggests it's for applying to lateral entry (it's an information database)
2. **Privacy & Control**: Appointees control exactly what information is public vs private vs lateral-entrants-only
3. **LinkedIn Integration**: Seamless sync with LinkedIn profiles (optional, user's choice) for up-to-date professional information
4. **Job Discovery**: Comprehensive AI-powered monitoring finds relevant vacancies across thousands of organizations
5. **Data Currency**: Appointees keep profiles updated without administrator bottleneck
6. **Professional Networking**: Creates a community platform for lateral entrants to connect and share opportunities
7. **Customized Job Alerts**: Position-level and domain-specific vacancy notifications
8. **Transparency with Privacy**: Public transparency while respecting individual privacy preferences

## User Impact

### Lateral Entry Appointees (New User Type - Authenticated)
- **Profile Management**: Log in to edit profiles with LinkedIn sync option
- **Granular Privacy**: Set visibility for each field (Public/Lateral Entrants Only/Private)
- **LinkedIn Integration**: Choose to link LinkedIn account and auto-sync data, or manually enter information
- **Job Opportunities**: Access curated job board with AI-monitored vacancies matching their expertise
- **Professional Network**: Connect with other lateral entrants (authenticated-only features)
- **Content Uploads**: Upload photos and documents (admin moderated)
- **AI Assistance**: Get help writing professional content
- **Analytics**: See profile views and engagement metrics

### Public Visitors (Unauthenticated)
- **Public Profiles**: View only fields marked as "Public" by appointees
- **Clear Branding**: Portal name accurately reflects it's an information database, not application portal
- **Social Feeds**: See news and updates on homepage
- **Search & Browse**: Find appointees by ministry, expertise, batch

### Authenticated Lateral Entrants (Peer Network)
- **Enhanced Profiles**: See fields marked as "Lateral Entrants Only" in addition to public fields
- **Job Board**: Access comprehensive vacancy listings monitored by AI
- **Professional Networking**: Community features for connecting with peers
- **Resource Hub**: Access exclusive resources, news, and updates

### Portal Administrators
- **User Approval**: Approve/link Google accounts to profiles
- **Content Moderation**: Review uploads and profile edits
- **Job Monitoring Config**: Configure AI monitoring prompts for vacancy tracking
- **Privacy Oversight**: Ensure appropriate use of visibility controls
- **Reduced Manual Work**: Less profile updates after initial setup

## Risks and Mitigations

### Security Risks
**Risk**: User-generated content opens attack vectors (XSS, SQL injection, file upload vulnerabilities)  
**Mitigation**: 
- Implement robust input sanitization
- Use parameterized queries (already in place)
- Validate and scan all file uploads
- Set strict file size and type limits
- Implement rate limiting on uploads

### Data Quality Risks
**Risk**: Appointees might add inaccurate or inappropriate content  
**Mitigation**:
- Optional admin review/approval workflow
- AI content moderation
- Clear guidelines and terms of use
- Ability to flag/report inappropriate content
- Revert capabilities for administrators

### Privacy Risks
**Risk**: Appointees might inadvertently share sensitive information  
**Mitigation**:
- Clear privacy notices and warnings
- Optional fields (nothing required beyond basics)
- Appointees control what is public vs private
- Audit log of all changes

### Performance Risks
**Risk**: Social media feeds and news monitoring could slow down homepage  
**Mitigation**:
- Asynchronous loading of feeds
- Caching layer for external API calls
- Background jobs for news monitoring
- Fallback to cached content if APIs fail
- Pagination and lazy loading

### AI Integration Risks
**Risk**: Custom AI model might be unavailable or produce inappropriate content  
**Mitigation**:
- Graceful degradation if AI unavailable
- AI suggestions require user approval
- Content moderation on AI-generated text
- Fallback to template-based suggestions
- Rate limiting on AI requests

## Dependencies

### External Services
- **Google OAuth**: Client ID and Client Secret (to be provided by user)
- **Custom AI Model**: Base URL and configuration (to be provided by user)
- **Parallel AI Monitor**: For news monitoring AND comprehensive job monitoring (configuration to be provided)
- **LinkedIn OAuth** (Optional): For users who want real-time LinkedIn sync
  - LinkedIn API credentials (App ID, App Secret)
  - Rate limits: TBD based on LinkedIn API tier
  - Fallback: Manual entry if user doesn't link LinkedIn
- **Social Media APIs** (Optional for homepage feeds):
  - X API, Facebook Graph API, LinkedIn API for social feeds
- **File Storage**: Local filesystem or object storage for uploads

### Technical Dependencies
- Google OAuth2 library (python-google-auth, google-auth-oauthlib)
- LinkedIn OAuth library (optional, if user wants real-time sync)
- Session management with secure cookies
- File upload handling with validation
- Background job processing for news and job monitoring
- API rate limiting
- Image processing libraries (Pillow for resize, optimize)
- Admin moderation queue system
- Granular permission system for field-level visibility controls

### Data Dependencies
- New database tables:
  - Field visibility settings (per-user, per-field)
  - LinkedIn sync configuration (per-user)
  - Job listings and monitoring configuration
  - User job preferences (position level, domain, location)
- Migration scripts for existing data
- Backup strategy for user-generated content

## Success Criteria

### Functional Success
- [ ] Project successfully rebranded (homepage title updated)
- [ ] Appointees can successfully register and log in
- [ ] Appointees can set granular visibility controls (Public/Lateral Entrants Only/Private) on each field
- [ ] Public visitors see only "Public" fields
- [ ] Authenticated lateral entrants see "Public" + "Lateral Entrants Only" fields
- [ ] LinkedIn integration works (optional, user's choice):
  - [ ] Option A: Users can link LinkedIn via OAuth and sync fields
  - [ ] Option B: Users can manually enter data with LinkedIn-style layout
- [ ] Appointees can edit all profile fields (with admin approval)
- [ ] Appointees can upload at least 10 photos per profile
- [ ] AI assistant generates helpful content suggestions
- [ ] Homepage displays social media feeds without performance issues
- [ ] News monitoring system finds and displays relevant articles
- [ ] **Job monitoring system tracks vacancies across configured organizations**
- [ ] **Authenticated users can access job board with curated listings**
- [ ] **Job listings are customized by position level and domain expertise**
- [ ] Admin panel allows content moderation
- [ ] Admin can configure job monitoring prompts

### Performance Success
- [ ] Homepage loads in < 3 seconds with feeds
- [ ] Profile editing interface responds in < 500ms
- [ ] File uploads complete in < 10 seconds for 5MB images
- [ ] AI content generation responds in < 5 seconds
- [ ] Social media feeds refresh every 15 minutes
- [ ] LinkedIn sync completes in < 10 seconds
- [ ] Job board loads in < 2 seconds
- [ ] Job monitoring completes hourly without impacting site performance

### Security & Privacy Success
- [ ] All user input is sanitized
- [ ] File uploads are validated and scanned
- [ ] Authentication prevents unauthorized access
- [ ] Rate limiting prevents abuse
- [ ] No security vulnerabilities in third-party code
- [ ] **Granular visibility controls properly enforce access restrictions**
- [ ] **Private fields are never exposed to unauthorized users**
- [ ] **LinkedIn OAuth tokens stored encrypted**

### User Success
- [ ] 80% of appointees update their profiles within 3 months of launch
- [ ] Average profile completeness > 70%
- [ ] < 5% inappropriate content flagged
- [ ] Positive user feedback on AI assistance
- [ ] **At least 30% of users utilize granular visibility controls**
- [ ] **At least 20% of users link their LinkedIn profiles**
- [ ] **Authenticated users engage with job board (>50% visit within first month)**
- [ ] Increased visitor engagement (time on site, page views)

## Alternatives Considered

### Alternative 1: Admin-Only Updates with Forms
Keep profiles admin-managed but add submission forms for appointees.
- **Pros**: Simpler security model, guaranteed quality control
- **Cons**: Admin bottleneck, slower updates, less engagement
- **Rejected**: Doesn't meet requirement for appointee autonomy

### Alternative 2: Third-Party Profile Hosting
Use LinkedIn or similar for profiles, embed on portal.
- **Pros**: No authentication needed, maintained by others
- **Cons**: No control over format, requires external accounts, inconsistent
- **Rejected**: Doesn't meet requirement for standardized format

### Alternative 3: Static Site Generator with Git-based CMS
Use Netlify CMS or similar for content management.
- **Pros**: Version control, no backend database needed
- **Cons**: Technical barrier for users, complex setup, not real-time
- **Rejected**: Too complex for non-technical users

### Alternative 4: WordPress or CMS Platform
Migrate to WordPress with member plugin.
- **Pros**: Mature ecosystem, many plugins available
- **Cons**: Complete rewrite, loss of custom features, heavier system
- **Rejected**: Prefer lightweight custom solution aligned with current tech stack

## Open Questions

### Authentication & Identity
1. **How should appointees register?**
   - ✅ **ANSWERED**: Google OAuth-based authentication
   - User provides: Google OAuth Client ID and Client Secret
   - Users sign in with their Google accounts
   - Admin moderates and approves authenticated users before they can access editing features

2. **What identification is required?**
   - ✅ **ANSWERED**: Google account email
   - No additional verification needed (Google handles email verification)
   - Admin links Google account to specific entrant profile

3. **What can users edit after authentication?**
   - ✅ **ANSWERED**: Users can edit all profile fields with moderation:
   - Users can upload files (photos, documents) - requires admin approval
   - Users can edit ALL information fields - requires admin approval before going live
   - Users CANNOT directly edit critical fields (name, position, ministry, batch) - must request edit
   - Users CAN set visibility controls on each field (Public/Lateral Entrants Only/Private)

### Content Management
4. **What file types should be allowed?**
   - ✅ **ANSWERED**: Images: JPEG, PNG, WebP for photos (max 5MB each, 25MB total per user)
   - Documents: PDF for certificates/credentials (max 10MB each)
   - All uploads go through admin moderation queue

5. **Should content require approval?**
   - ✅ **ANSWERED**: Yes, all uploads and edits require admin moderation
   - Users upload files → goes to moderation queue
   - Users edit fields → goes to moderation queue  
   - Admin reviews and approves/rejects before public display
   - Users can see their pending changes with moderation status
   - Rejected changes can be re-submitted after correction

6. **What happens to old data?**
   - ✅ **RECOMMENDATION**: Create accounts for all current appointees
   - Admin maintains unclaimed profiles
   - Notify appointees via email/LinkedIn about platform
   - Profiles remain public (read-only) until claimed

### Project Rebranding
7. **Should the project be renamed?**
   - ✅ **ANSWERED**: Yes, rename from "Lateral Entry Portal" to better reflect purpose
   - **Suggested Name**: "Lateral Entry Officers Database" or similar
   - Change homepage title and branding (not URL paths or repository name)
   - Update meta descriptions and page titles
   - **SCOPE**: Only frontend title/branding changes, no database/code refactoring required

### Privacy & Visibility Controls
8. **How should granular visibility work?**
   - ✅ **ANSWERED**: Three-level visibility per field:
   - **Public**: Anyone can view without login
   - **Lateral Entrants Only**: Only authenticated lateral entry officers can view
   - **Private**: Only the profile owner can view
   - Each field has a small toggle/dropdown to select visibility
   - Public page shows only "Public" fields
   - Authenticated lateral entrants see "Public" + "Lateral Entrants Only" fields
   - Profile owner sees all fields including "Private"

### LinkedIn Integration
9. **How should LinkedIn integration work?**
   - ✅ **ANSWERED**: Optional, user's choice with multiple approaches:
   
   **Option A (Real-time sync via LinkedIn OAuth)**:
   - User links their LinkedIn account via LinkedIn OAuth
   - System pulls profile data from LinkedIn API in real-time
   - User selects which LinkedIn fields to sync to which portal fields
   - Sync happens with a button click ("Sync from LinkedIn")
   - **Limitation**: LinkedIn API rate limits and permissions apply
   - **Technical**: Requires LinkedIn OAuth per user
   
   **Option B (Manual entry with LinkedIn-style layout)**:
   - User manually enters LinkedIn profile URL
   - Profile adopts LinkedIn-style layout/design
   - User manually copies fields from LinkedIn or enters data
   - No API integration needed
   
   **Option C (Hybrid - User's choice)**:
   - User can choose either Option A or B
   - If user doesn't have LinkedIn or doesn't want to link it, use Option B
   - LinkedIn sync is completely optional
   - **Technical feasibility rests with the user** - if they grant LinkedIn access, we can sync

10. **Which profile fields sync from LinkedIn?**
    - ✅ **RECOMMENDATION**: Allow user to map any LinkedIn field to portal field
    - Common mappings: Headline, Summary, Experience, Education, Skills, Certifications
    - User can choose to sync some fields and manually enter others
    - Respects visibility controls (user sets public/private per field after sync)

### Job Monitoring
11. **How should comprehensive job monitoring work?**
    - ✅ **ANSWERED**: AI-powered monitoring using Parallel AI Monitor
    - **Authenticated users only** can access job board
    - Comprehensive prompt monitors thousands of organizations (public + private sector)
    - Customized by:
      - Position level (Joint Secretary, Director, Deputy Secretary)
      - Domain expertise (Finance, Technology, Healthcare, etc.)
      - Location preferences (optional)
      - Seniority requirements
    - Parallel AI Monitor runs searches periodically
    - Results curated and displayed on job board page (authenticated only)
    - Push notifications for highly relevant vacancies (optional)

12. **What organizations should be monitored?**
    - ✅ **TO BE CONFIGURED**: Create comprehensive list of:
    - Central Government ministries and departments
    - State government organizations
    - Public sector undertakings (PSUs)
    - Autonomous bodies and regulatory agencies
    - International organizations in India
    - Think tanks and research institutions
    - Private sector companies known for hiring senior government professionals
    - **Action**: User will provide comprehensive prompt for Parallel AI Monitor

13. **How often should job monitoring run?**
    - ✅ **RECOMMENDATION**: 
    - Hourly monitoring for high-priority organizations (central govt)
    - Daily monitoring for other organizations
    - Weekly digest emails to interested lateral entrants
    - Real-time notifications for urgent/high-match vacancies

### AI Integration
7. **What AI capabilities are needed?**
   - Generate profile summaries from bullet points?
   - Suggest achievement descriptions?
   - Grammar checking and improvement?
   - Translation to multiple languages?
   - **Recommendation**: Start with summary generation and achievement descriptions

8. **How to handle AI failures?**
   - Graceful degradation to manual entry?
   - Cache successful results?
   - Retry logic?
   - **Recommendation**: Always allow manual override, show helpful templates if AI fails

9. **What's the AI model's rate limit?**
   - Requests per user per day?
   - Concurrent requests?
   - Cost per request?
   - **Recommendation**: Need user to provide these details

### Social Media Integration
10. **Which platforms are priority?**
    - X (Twitter), LinkedIn, Facebook?
    - Instagram, YouTube?
    - WhatsApp status, Telegram?
    - **Recommendation**: Start with X, LinkedIn, Facebook (most professional)

11. **What content should be shown?**
    - Only posts mentioning appointees or lateral entry?
    - Official ministry accounts?
    - Personal accounts of appointees?
    - News media accounts?
    - **Recommendation**: All of the above with filters, user can configure

12. **How to handle API rate limits?**
    - Cache duration for feeds?
    - Fallback when limits reached?
    - Cost considerations?
    - **Recommendation**: 15-minute cache, show "unavailable" message on limit

### News Monitoring
13. **What constitutes relevant news?**
    - Mentions of appointee names?
    - Ministry-related news?
    - Lateral entry program updates?
    - Policy changes?
    - **Recommendation**: All appointee name mentions + lateral entry keywords

14. **How is Parallel AI Monitor configured?**
    - What's the API endpoint?
    - Authentication method?
    - Query format?
    - Response structure?
    - **Recommendation**: User needs to provide configuration details

15. **How often should monitoring run?**
    - Real-time monitoring?
    - Hourly batch jobs?
    - Daily digests?
    - **Recommendation**: Hourly monitoring, cache results, update UI every 15 minutes

### User Experience
16. **What analytics should appointees see?**
    - Profile view counts?
    - Social media engagement?
    - Most viewed sections?
    - **Recommendation**: Basic view counts, trending searches that found them

17. **Should there be notifications?**
    - Email when someone views profile?
    - Weekly activity summaries?
    - New media mentions?
    - **Recommendation**: Optional weekly digest, avoid spam

18. **Mobile app or web-only?**
    - Progressive Web App?
    - Native mobile apps?
    - Mobile-optimized web interface?
    - **Recommendation**: Mobile-optimized web (current approach), optionally add PWA later

## Next Steps

1. **Clarify Open Questions**: User provides answers to remaining questions:
   - Final decision on project name ("Lateral Entry Officers Database" or alternative)
   - Google OAuth credentials (Client ID, Client Secret)
   - AI model base URL, authentication, and rate limits
   - Parallel AI Monitor configuration for both news AND job monitoring
   - Comprehensive prompt for job monitoring (list of organizations to track)
   - LinkedIn OAuth credentials (if users want Option A - real-time sync)
   - Social media API access (keys, rate limits) for homepage feeds (optional)
   - Default admin account credentials

2. **Review Design Document**: Create detailed technical design covering:
   - Project rebranding implementation (what to rename, what to keep)
   - Granular visibility control architecture (database schema, API, UI)
   - LinkedIn integration architecture (OAuth flow, field mapping, sync logic)
   - Job monitoring system architecture (Parallel AI integration, storage, filtering)
   - Database schema changes for all new features
   - API endpoint specifications
   - Authentication flow diagrams
   - File upload architecture
   - AI integration patterns
   - Social media aggregation strategy (optional)
   - News monitoring implementation

3. **Validate Feasibility**: Confirm:
   - Custom AI model is accessible and documented
   - LinkedIn OAuth is approved for production use (if Option A selected)
   - Parallel AI Monitor can handle comprehensive job monitoring prompts
   - Server can handle background jobs for job + news monitoring
   - File storage capacity is sufficient
   - Social media APIs are available (if homepage feeds desired)

4. **Create Implementation Plan**: Break down into phases:
   - Phase 0: Project rebranding (homepage title, meta tags)
   - Phase 1: Authentication and basic profile editing
   - Phase 2: Granular visibility controls (3-level permissions)
   - Phase 3: File uploads and media management
   - Phase 4: LinkedIn integration (both Option A and B)
   - Phase 5: AI assistance integration
   - Phase 6: Job monitoring system (Parallel AI)
   - Phase 7: Social media feeds (optional)
   - Phase 8: News monitoring (existing plan)
   - Phase 9: Testing, security, performance
   - Phase 10: Deployment and launch

5. **Get User Approval**: User reviews and approves:
   - Proposed architecture
   - Implementation phases
   - Timeline estimates (now ~15-16 weeks with new features)
   - Resource requirements

## Related Changes

- None (new feature set)

## References

- Current database schema: `database/lateral_entry_schema.sql`
- Project conventions: `openspec/project.md`
- Existing authentication: None currently implemented
