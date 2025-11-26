# Granular Visibility Controls Capability

**Change ID**: `add-user-profiles-and-feeds`  
**Capability**: `visibility-controls`  
**Status**: Draft

## ADDED Requirements

### Requirement: Three-Level Field Visibility

The system SHALL provide three visibility levels for each profile field: Public, Lateral Entrants Only, and Private.

#### Scenario: User sets field visibility to Public
- **WHEN** an authenticated lateral entrant edits a profile field
- **AND** sets the visibility toggle to "Public"
- **THEN** the field is visible to all visitors (authenticated and unauthenticated)
- **AND** the field appears on the public profile page
- **AND** the field is included in search results and browse listings

#### Scenario: User sets field visibility to Lateral Entrants Only
- **WHEN** an authenticated lateral entrant edits a profile field
- **AND** sets the visibility toggle to "Lateral Entrants Only"
- **THEN** the field is visible ONLY to authenticated lateral entry officers
- **AND** the field is hidden from unauthenticated visitors
- **AND** the field appears with a 🔒 icon indicating restricted access
- **AND** unauthenticated visitors see placeholder text: "Sign in as a lateral entrant to view"

#### Scenario: User sets field visibility to Private
- **WHEN** an authenticated lateral entrant edits a profile field
- **AND** sets the visibility toggle to "Private"
- **THEN** the field is visible ONLY to the profile owner
- **AND** the field is hidden from all other users (authenticated or not)
- **AND** the field does NOT appear on the profile page for anyone except the owner
- **AND** the profile owner sees the field with a "Private" badge

#### Scenario: Public visitor views profile with mixed visibility
- **WHEN** an unauthenticated visitor views a lateral entrant's profile
- **THEN** the system displays ONLY fields marked as "Public"
- **AND** fields marked "Lateral Entrants Only" show placeholder: "🔒 Visible to lateral entrants only"
- **AND** fields marked "Private" are completely hidden (not shown at all)
- **AND** the page structure adjusts to hide empty sections

#### Scenario: Authenticated lateral entrant views peer profile
- **WHEN** an authenticated lateral entrant views another lateral entrant's profile
- **THEN** the system displays fields marked as "Public"
- **AND** the system displays fields marked as "Lateral Entrants Only"
- **AND** fields marked "Private" remain hidden
- **AND** "Lateral Entrants Only" fields are marked with 🔒 icon

#### Scenario: Profile owner views own profile
- **WHEN** an authenticated lateral entrant views their own profile
- **THEN** the system displays ALL fields (Public, Lateral Entrants Only, and Private)
- **AND** each field shows its current visibility setting
- **AND** the owner can toggle visibility inline
- **AND** visibility changes require admin approval before taking effect (if moderation enabled)

### Requirement: Visibility Control Interface

The system SHALL provide an intuitive interface for users to control field visibility.

#### Scenario: Inline visibility toggle in profile editor
- **WHEN** an authenticated lateral entrant opens the profile editor
- **THEN** each editable field displays a small visibility dropdown/toggle
- **AND** the dropdown shows three options: "Public 🌐", "Lateral Entrants Only 🔒", "Private 👁️"
- **AND** the current setting is highlighted
- **AND** clicking an option changes the visibility setting
- **AND** a save button applies all changes

#### Scenario: Bulk visibility controls
- **WHEN** an authenticated lateral entrant clicks "Manage Visibility" in profile settings
- **THEN** the system displays a table/list of all profile fields
- **AND** each row shows: Field Name | Current Visibility | Toggle Options
- **AND** the user can quickly change multiple field visibilities
- **AND** a "Save All" button applies all changes
- **AND** the system shows a confirmation: "Visibility settings updated"

#### Scenario: Default visibility for new fields
- **WHEN** a user adds a new profile field
- **THEN** the system sets default visibility to "Public"
- **AND** the user is prompted to review and adjust visibility
- **AND** a tooltip explains: "You can change who sees this field"

### Requirement: Visibility Enforcement in API

The system SHALL enforce visibility controls in all API responses based on the requester's authentication status.

#### Scenario: API returns profile for unauthenticated request
- **WHEN** an unauthenticated client requests GET /api/profile/:id
- **THEN** the response includes ONLY fields where visibility = 'public'
- **AND** restricted fields are NOT included in the JSON response
- **AND** the response includes a flag: `hasRestrictedFields: true` if any fields are hidden

#### Scenario: API returns profile for authenticated lateral entrant
- **WHEN** an authenticated lateral entrant requests GET /api/profile/:id for another entrant
- **THEN** the response includes fields where visibility = 'public' OR 'lateral_entrants_only'
- **AND** private fields are NOT included
- **AND** each field includes a `visibility` attribute in the response

#### Scenario: API returns own profile
- **WHEN** an authenticated lateral entrant requests GET /api/profile (own profile)
- **THEN** the response includes ALL fields regardless of visibility setting
- **AND** each field includes its current visibility setting
- **AND** the response includes edit permissions for each field

### Requirement: Visibility Audit Logging

The system SHALL log all visibility setting changes for audit purposes.

#### Scenario: Visibility change is logged
- **WHEN** an authenticated lateral entrant changes a field's visibility setting
- **THEN** the system creates an audit log entry with:
  - User ID
  - Field name
  - Old visibility setting
  - New visibility setting
  - Timestamp
  - IP address
- **AND** admin can view audit log in admin panel

#### Scenario: Bulk visibility changes logged
- **WHEN** a user changes multiple field visibilities at once
- **THEN** the system creates separate audit log entries for each field change
- **AND** all entries share the same timestamp
- **AND** the log indicates it was a bulk change operation

### Requirement: Visibility in Search and Browse

The system SHALL respect visibility controls in search results and browse listings.

#### Scenario: Unauthenticated search results
- **WHEN** an unauthenticated user searches for lateral entrants
- **THEN** search results show ONLY public field values
- **AND** results are ranked using only public fields
- **AND** profile cards in results display only public information

#### Scenario: Authenticated lateral entrant search results
- **WHEN** an authenticated lateral entrant searches for peers
- **THEN** search results can match against "Public" and "Lateral Entrants Only" fields
- **AND** profile cards show both public and lateral-entrants-only information
- **AND** fields are marked with appropriate visibility indicators

## Technical Specifications

### Database Schema

```sql
-- Field visibility settings
CREATE TABLE field_visibility_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrant_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL, -- e.g., 'email', 'phone', 'profile_summary'
    visibility VARCHAR(50) DEFAULT 'public', -- public, lateral_entrants_only, private
    updated_by INTEGER, -- user_id who made the change
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant_id) REFERENCES lateral_entrants(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    UNIQUE(entrant_id, field_name)
);

-- Create index for performance
CREATE INDEX idx_visibility_lookup ON field_visibility_settings(entrant_id, field_name);

-- Add default visibility column to lateral_entrants (for backward compatibility)
ALTER TABLE lateral_entrants ADD COLUMN default_visibility VARCHAR(50) DEFAULT 'public';
```

### API Endpoints

```
GET    /api/profile/:id/visibility        - Get visibility settings for profile
PUT    /api/profile/visibility/:field     - Update single field visibility
PUT    /api/profile/visibility/bulk       - Update multiple field visibilities
GET    /api/visibility/audit-log          - Get visibility change history (admin or own)
GET    /api/visibility/defaults           - Get default visibility for each field type
```

### Field Categories and Default Visibility

| Field Category | Example Fields | Default Visibility | User Can Change? |
|----------------|----------------|-------------------|------------------|
| Basic Identity | Name, Position, Ministry, Batch | Public | No (admin only) |
| Contact | Email, Phone, Address | Private | Yes |
| Professional | Experience, Education, Skills | Public | Yes |
| Summary | Profile Summary, About | Public | Yes |
| Media | Profile Photo, Documents | Public | Yes |
| Achievements | Awards, Certifications, Publications | Public | Yes |
| Social Links | LinkedIn, Twitter, Personal Website | Public | Yes |

### Configuration

```python
# Field visibility configuration
VISIBILITY_LEVELS = {
    'public': {
        'label': 'Public',
        'icon': '🌐',
        'description': 'Visible to everyone',
        'access': ['unauthenticated', 'authenticated', 'owner']
    },
    'lateral_entrants_only': {
        'label': 'Lateral Entrants Only',
        'icon': '🔒',
        'description': 'Visible only to other lateral entrants',
        'access': ['authenticated', 'owner']
    },
    'private': {
        'label': 'Private',
        'icon': '👁️',
        'description': 'Visible only to you',
        'access': ['owner']
    }
}

# Fields that cannot have visibility changed (always public)
LOCKED_PUBLIC_FIELDS = [
    'name',
    'position',
    'ministry',
    'department',
    'batch_year',
    'batch_advertisement_number'
]

# Fields that default to private
DEFAULT_PRIVATE_FIELDS = [
    'personal_email',
    'personal_phone',
    'home_address'
]
```

### API Response Example

```json
// GET /api/profile/123 (unauthenticated)
{
  "id": 123,
  "name": "Dr. John Doe",
  "position": "Joint Secretary",
  "ministry": "Ministry of Finance",
  "profile_summary": "Experienced economist...",
  "hasRestrictedFields": true,
  "restrictedFieldCount": 5
}

// GET /api/profile/123 (authenticated lateral entrant)
{
  "id": 123,
  "name": "Dr. John Doe",
  "position": "Joint Secretary",
  "ministry": "Ministry of Finance",
  "profile_summary": "Experienced economist...",
  "email": "john.doe@gov.in",  // Lateral entrants only
  "phone": "[PRIVATE]",  // Private, not shown
  "hasPrivateFields": true
}

// GET /api/profile (own profile)
{
  "id": 123,
  "name": "Dr. John Doe",
  "position": "Joint Secretary",
  "ministry": "Ministry of Finance",
  "profile_summary": {
    "value": "Experienced economist...",
    "visibility": "public",
    "canEdit": true
  },
  "email": {
    "value": "john.doe@gov.in",
    "visibility": "lateral_entrants_only",
    "canEdit": true
  },
  "phone": {
    "value": "+91-xxx-xxx-xxxx",
    "visibility": "private",
    "canEdit": true
  }
}
```

## User Interface

### Inline Visibility Toggle in Profile Editor

```
┌─────────────────────────────────────────────────────────┐
│ Edit Profile                                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Profile Summary                      [🌐 Public     ▾]  │
│ ┌──────────────────────────────────────────────────────┐│
│ │ Experienced economist with 15 years in policy...    ││
│ │                                                      ││
│ └──────────────────────────────────────────────────────┘│
│                                                          │
│ Email                           [🔒 Lateral Entrants ▾]  │
│ ┌──────────────────────────────────────────────────────┐│
│ │ john.doe@gov.in                                      ││
│ └──────────────────────────────────────────────────────┘│
│                                                          │
│ Phone                                [👁️ Private    ▾]  │
│ ┌──────────────────────────────────────────────────────┐│
│ │ +91-9876543210                                       ││
│ └──────────────────────────────────────────────────────┘│
│                                                          │
│                    [Cancel]  [Save Changes]              │
└─────────────────────────────────────────────────────────┘
```

### Bulk Visibility Management

```
┌─────────────────────────────────────────────────────────┐
│ Manage Field Visibility                            [×]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Field                Current         Change To           │
│ ───────────────────────────────────────────────────────  │
│ Profile Summary      🌐 Public       [🌐 🔒 👁️]         │
│ Email                🔒 Lat. Ent.    [🌐 🔒 👁️]         │
│ Phone                👁️ Private      [🌐 🔒 👁️]         │
│ LinkedIn URL         🌐 Public       [🌐 🔒 👁️]         │
│ Experience           🌐 Public       [🌐 🔒 👁️]         │
│ Education            🌐 Public       [🌐 🔒 👁️]         │
│ Skills               🔒 Lat. Ent.    [🌐 🔒 👁️]         │
│ Achievements         🌐 Public       [🌐 🔒 👁️]         │
│                                                          │
│ Legend: 🌐 Public | 🔒 Lateral Entrants Only | 👁️ Private│
│                                                          │
│          [Cancel]         [Save All Changes]             │
└─────────────────────────────────────────────────────────┘
```

### Public Profile View (Unauthenticated)

```
┌─────────────────────────────────────────────────────────┐
│ Dr. John Doe                                             │
│ Joint Secretary, Ministry of Finance                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ About                                                    │
│ Experienced economist with 15 years in policy...        │
│                                                          │
│ 🔒 Contact Information                                   │
│    Sign in as a lateral entrant to view contact details │
│                                                          │
│ Experience                                               │
│ • Joint Secretary, Ministry of Finance (2021-Present)  │
│ • ...                                                    │
│                                                          │
│ 🔒 Additional Information                                │
│    Some details are visible only to lateral entrants    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Testing Strategy

### Unit Tests
- Test visibility filtering logic for each level
- Test API response filtering based on authentication status
- Test bulk visibility update operations
- Test default visibility assignment
- Test visibility change validation
- Test audit log creation

### Integration Tests
- Test end-to-end visibility workflow (set, save, view)
- Test unauthenticated profile viewing
- Test authenticated lateral entrant profile viewing
- Test profile owner self-viewing
- Test search results respect visibility
- Test visibility in browse listings

### Security Tests
- Test unauthorized access to restricted fields via API
- Test direct database query bypassing still respects visibility
- Test JWT token validation for "lateral_entrants_only" fields
- Test rate limiting on visibility API endpoints

## Success Criteria

- [ ] Users can set visibility for each profile field
- [ ] Public visitors see only "Public" fields
- [ ] Authenticated lateral entrants see "Public" + "Lateral Entrants Only" fields
- [ ] Profile owners see all fields including "Private"
- [ ] API properly filters responses based on authentication status
- [ ] Visibility changes are logged in audit log
- [ ] Search respects visibility controls
- [ ] At least 30% of users utilize granular visibility controls
- [ ] No security vulnerabilities in visibility enforcement
- [ ] Performance impact < 50ms per profile load

## Related Specifications

- [Google OAuth Authentication](../authentication/google-oauth.md)
- [Profile Field Editing](../profile-editing/spec.md)
- [LinkedIn Integration](../linkedin-integration/spec.md)
- [Search and Browse](../../specs/search/spec.md)
