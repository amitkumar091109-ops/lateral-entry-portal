# LinkedIn Integration Capability

**Change ID**: `add-user-profiles-and-feeds`  
**Capability**: `linkedin-integration`  
**Status**: Draft

## ADDED Requirements

### Requirement: LinkedIn Profile Synchronization

The system SHALL provide optional LinkedIn profile integration allowing lateral entry officers to sync their LinkedIn profile data with their portal profile.

#### Scenario: User chooses LinkedIn OAuth sync
- **WHEN** an authenticated lateral entrant clicks "Connect LinkedIn" in profile settings
- **THEN** the system redirects to LinkedIn OAuth consent page
- **AND** after authorization, the system fetches LinkedIn profile data
- **AND** the system presents a field mapping interface showing LinkedIn fields and corresponding portal fields
- **AND** the user selects which LinkedIn fields to sync to which portal fields
- **AND** the user clicks "Sync Now" to populate selected fields
- **AND** synced data populates the corresponding profile fields (respecting moderation requirements)

#### Scenario: User chooses manual LinkedIn entry
- **WHEN** an authenticated lateral entrant chooses "Add LinkedIn URL manually" in profile settings
- **THEN** the system provides a text input for LinkedIn profile URL
- **AND** the system saves the LinkedIn URL as a link in the profile
- **AND** the profile adopts LinkedIn-style layout and design
- **AND** the user manually enters or copies data from their LinkedIn profile

#### Scenario: LinkedIn sync with field mapping
- **WHEN** a user has connected their LinkedIn account and clicks "Sync from LinkedIn"
- **THEN** the system calls LinkedIn API to fetch current profile data
- **AND** the system applies user's configured field mappings
- **AND** the system populates portal fields with LinkedIn data
- **AND** synced fields maintain user's visibility settings (Public/Lateral Entrants Only/Private)
- **AND** changes go through moderation queue if moderation is enabled

#### Scenario: LinkedIn API unavailable
- **WHEN** a user attempts LinkedIn sync but the LinkedIn API returns an error
- **THEN** the system displays a clear error message: "LinkedIn sync temporarily unavailable"
- **AND** the system offers fallback: "You can manually enter your information instead"
- **AND** the user can proceed with manual entry

#### Scenario: User disconnects LinkedIn
- **WHEN** an authenticated lateral entrant clicks "Disconnect LinkedIn" in profile settings
- **THEN** the system revokes LinkedIn OAuth tokens
- **AND** the system removes LinkedIn sync configuration
- **AND** the system retains previously synced data (does not delete)
- **AND** the system displays confirmation: "LinkedIn disconnected. Your profile data is unchanged."

### Requirement: LinkedIn Field Mapping Configuration

The system SHALL allow users to configure which LinkedIn profile fields map to which portal profile fields.

#### Scenario: User configures field mappings
- **WHEN** a user connects their LinkedIn account
- **THEN** the system displays a mapping configuration interface
- **AND** the interface shows LinkedIn fields on the left and portal fields on the right
- **AND** the user can select or deselect each mapping
- **AND** common default mappings are pre-selected (Headline → Position Summary, Summary → About, etc.)
- **AND** the user can save custom mapping configuration
- **AND** the configuration persists for future syncs

#### Scenario: User syncs only selected fields
- **WHEN** a user has configured custom field mappings
- **AND** the user clicks "Sync from LinkedIn"
- **THEN** the system syncs ONLY the fields that are mapped
- **AND** unmapped fields remain unchanged
- **AND** the system shows which fields were synced successfully

### Requirement: LinkedIn-Style Profile Layout

The system SHALL adopt a LinkedIn-style professional profile layout for displaying lateral entry officer profiles.

#### Scenario: Profile displays with LinkedIn-style layout
- **WHEN** a visitor views a lateral entry officer's profile
- **THEN** the profile displays with LinkedIn-inspired design elements:
  - Professional header with name, position, and profile photo
  - Summary/About section prominently displayed
  - Experience section with timeline layout
  - Education section with institution logos/seals
  - Skills section with endorsement-style display (without actual endorsements)
  - Achievements section with visual cards

### Requirement: LinkedIn OAuth Security

The system SHALL securely handle LinkedIn OAuth tokens and protect user LinkedIn data.

#### Scenario: LinkedIn tokens stored encrypted
- **WHEN** a user successfully connects their LinkedIn account
- **THEN** the system encrypts the LinkedIn access token before storing
- **AND** the system encrypts the LinkedIn refresh token before storing
- **AND** tokens are stored with the same encryption method as Google OAuth tokens (Fernet encryption)

#### Scenario: LinkedIn token refresh
- **WHEN** a user's LinkedIn access token expires
- **AND** the user attempts to sync from LinkedIn
- **THEN** the system automatically refreshes the access token using the refresh token
- **AND** the system updates the encrypted access token in the database
- **AND** the sync proceeds with the refreshed token

#### Scenario: LinkedIn sync rate limiting
- **WHEN** a user attempts to sync from LinkedIn more than 10 times per hour
- **THEN** the system displays an error: "LinkedIn sync rate limit reached. Please try again later."
- **AND** the system logs the rate limit event
- **AND** the rate limit resets after 1 hour

## Technical Specifications

### Database Schema

```sql
-- LinkedIn integration settings
CREATE TABLE linkedin_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    linkedin_id VARCHAR(255) UNIQUE,
    linkedin_profile_url TEXT,
    access_token TEXT, -- Encrypted
    refresh_token TEXT, -- Encrypted
    token_expires_at TIMESTAMP,
    connection_type VARCHAR(50) DEFAULT 'oauth', -- oauth or manual
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- LinkedIn field mapping configuration
CREATE TABLE linkedin_field_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    linkedin_field VARCHAR(100) NOT NULL, -- e.g., 'headline', 'summary'
    portal_field VARCHAR(100) NOT NULL, -- e.g., 'position_summary', 'about'
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- LinkedIn sync history
CREATE TABLE linkedin_sync_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sync_status VARCHAR(50), -- success, partial, failed
    fields_synced TEXT, -- JSON array of synced fields
    error_message TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### API Endpoints

```
GET    /api/linkedin/status              - Check if user has LinkedIn connected
POST   /api/linkedin/connect             - Initiate LinkedIn OAuth flow
GET    /api/linkedin/callback            - Handle LinkedIn OAuth callback
POST   /api/linkedin/disconnect          - Disconnect LinkedIn account
GET    /api/linkedin/profile             - Fetch LinkedIn profile data
POST   /api/linkedin/sync                - Sync LinkedIn data to portal profile
GET    /api/linkedin/mappings            - Get field mapping configuration
PUT    /api/linkedin/mappings            - Update field mapping configuration
GET    /api/linkedin/sync-history        - Get sync history
```

### Configuration

```bash
# LinkedIn OAuth (optional, for Option A)
LINKEDIN_CLIENT_ID=<user-provides>
LINKEDIN_CLIENT_SECRET=<user-provides>
LINKEDIN_REDIRECT_URI=https://prabhu.app/lateral-entry/api/linkedin/callback

# LinkedIn API rate limits
LINKEDIN_SYNC_RATE_LIMIT_PER_HOUR=10
LINKEDIN_API_TIMEOUT=10
```

### Dependencies

```
linkedin-api-client==1.0.0  # Or similar LinkedIn API library
```

### Default Field Mappings

| LinkedIn Field | Portal Field | Default Enabled |
|----------------|--------------|-----------------|
| headline | position_summary | Yes |
| summary | profile_summary | Yes |
| positions | experience_details | Yes |
| educations | education_details | Yes |
| skills | skills_expertise | Yes |
| certifications | achievements | Yes |
| honors | achievements | Yes |
| publications | achievements | Yes |

## User Interface

### LinkedIn Connection Settings (in Profile Settings)

```
┌─────────────────────────────────────────────────────────┐
│ LinkedIn Integration                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ○ Not Connected                                          │
│                                                          │
│ Connect your LinkedIn profile to automatically sync     │
│ your professional information.                          │
│                                                          │
│ ┌──────────────────────┐  ┌──────────────────────────┐ │
│ │ Connect LinkedIn     │  │ Add Manual URL          │ │
│ │ (OAuth Sync)         │  │ (Manual Entry)          │ │
│ └──────────────────────┘  └──────────────────────────┘ │
│                                                          │
│ Note: LinkedIn sync is optional and controlled by you.  │
└─────────────────────────────────────────────────────────┘
```

### After LinkedIn Connected

```
┌─────────────────────────────────────────────────────────┐
│ LinkedIn Integration                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ✓ Connected to LinkedIn                                 │
│                                                          │
│ Profile: linkedin.com/in/john-doe                       │
│ Last synced: 2 hours ago                                │
│                                                          │
│ ┌──────────────────────┐  ┌──────────────────────────┐ │
│ │ Sync Now             │  │ Configure Fields        │ │
│ └──────────────────────┘  └──────────────────────────┘ │
│                                                          │
│ ┌──────────────────────┐  ┌──────────────────────────┐ │
│ │ View Sync History    │  │ Disconnect LinkedIn     │ │
│ └──────────────────────┘  └──────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Field Mapping Configuration Modal

```
┌─────────────────────────────────────────────────────────┐
│ Configure LinkedIn Sync                            [×]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Select which fields to sync from your LinkedIn profile: │
│                                                          │
│ LinkedIn Field          →  Portal Field         Sync?  │
│ ─────────────────────────────────────────────────────── │
│ Headline                →  Position Summary     [✓]     │
│ Summary                 →  Profile Summary      [✓]     │
│ Positions (Experience)  →  Experience           [✓]     │
│ Education               →  Education            [✓]     │
│ Skills                  →  Expertise            [ ]     │
│ Certifications          →  Achievements         [✓]     │
│ Publications            →  Achievements         [ ]     │
│                                                          │
│ Note: Synced data will respect your visibility settings │
│ and go through moderation if required.                  │
│                                                          │
│          [Cancel]         [Save & Sync Now]              │
└─────────────────────────────────────────────────────────┘
```

## Testing Strategy

### Unit Tests
- Test LinkedIn OAuth flow (initiation, callback, token exchange)
- Test field mapping configuration (CRUD operations)
- Test sync logic with various field combinations
- Test token encryption/decryption
- Test token refresh mechanism
- Test rate limiting

### Integration Tests
- Test end-to-end LinkedIn connection and sync
- Test LinkedIn API error handling
- Test manual URL entry flow
- Test disconnect flow
- Test sync with moderation queue integration

### Security Tests
- Test LinkedIn token storage encryption
- Test OAuth state parameter validation (CSRF protection)
- Test rate limiting enforcement
- Test unauthorized access prevention

## Success Criteria

- [ ] Users can connect LinkedIn accounts via OAuth
- [ ] Users can manually add LinkedIn URL
- [ ] Field mapping configuration works correctly
- [ ] Sync successfully populates portal fields
- [ ] Synced data respects visibility controls
- [ ] LinkedIn tokens are stored encrypted
- [ ] Token refresh works automatically
- [ ] Rate limiting prevents abuse
- [ ] Profile displays with LinkedIn-style layout
- [ ] Error handling provides clear user feedback
- [ ] At least 20% of users connect their LinkedIn accounts

## Related Specifications

- [Google OAuth Authentication](../authentication/google-oauth.md)
- [Granular Visibility Controls](../visibility-controls/spec.md)
- [Profile Field Moderation](../moderation/upload-moderation.md)
