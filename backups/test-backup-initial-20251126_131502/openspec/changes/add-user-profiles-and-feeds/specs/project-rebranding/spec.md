# Project Rebranding Capability

**Change ID**: `add-user-profiles-and-feeds`  
**Capability**: `project-rebranding`  
**Status**: Draft

## ADDED Requirements

### Requirement: Update Project Display Name

The system SHALL update the display name from "Lateral Entry Portal" to accurately reflect the platform's purpose as an officers' database and professional network, not an application portal.

#### Scenario: Homepage displays new project name
- **WHEN** a visitor navigates to the homepage
- **THEN** the main heading displays the new project name (e.g., "Lateral Entry Officers Database")
- **AND** the browser tab title shows the new name
- **AND** the page meta description reflects the new purpose
- **AND** the About section explains: "This is an information database, not an application portal"

#### Scenario: Navigation shows updated branding
- **WHEN** a user is on any page of the portal
- **THEN** the site logo/header displays the new project name
- **AND** footer copyright displays the new name
- **AND** internal page titles consistently use the new name

#### Scenario: Meta tags updated for SEO
- **WHEN** search engines crawl the portal
- **THEN** meta title tags reflect new name
- **AND** meta descriptions clarify: "Comprehensive database of lateral entry officers in Government of India"
- **AND** Open Graph tags show updated name
- **AND** Twitter Card tags show updated name

### Requirement: Clarify Portal Purpose

The system SHALL prominently display messaging that clarifies the portal is for information, not for applying to lateral entry positions.

#### Scenario: Homepage explains portal purpose
- **WHEN** a visitor lands on the homepage
- **THEN** a prominent message states: "This platform provides information about lateral entry officers. To apply for lateral entry positions, visit [UPSC website]."
- **AND** a FAQ section includes: "How do I apply for lateral entry?" with link to official application process
- **AND** the About section clearly describes the portal as an information and networking resource

#### Scenario: Search engines understand portal purpose
- **WHEN** search engines index the portal
- **THEN** meta descriptions include: "Information database" or "Officers directory"
- **AND** does NOT include: "Apply now", "Application portal", "Join lateral entry"

### Requirement: Maintain Technical Infrastructure

The system SHALL maintain existing technical infrastructure (URLs, database names, repository names) to avoid breaking changes.

#### Scenario: URLs remain unchanged
- **WHEN** existing links to the portal are accessed
- **THEN** all URLs continue to work without redirects
- **AND** base path remains `/lateral-entry/`
- **AND** API endpoints remain unchanged
- **AND** no 404 errors occur from old links

#### Scenario: Database and code references unchanged
- **WHEN** the system operates after rebranding
- **THEN** database name `lateral_entry.db` remains unchanged
- **AND** Python module names remain unchanged
- **AND** repository name remains `lateral-entry-portal`
- **AND** internal code references to "lateral entry" remain as-is
- **AND** only user-facing display text is updated

#### Scenario: Configuration files unchanged
- **WHEN** deployment scripts run
- **THEN** environment variable names remain unchanged
- **AND** file paths remain unchanged
- **AND** service names remain unchanged
- **AND** only display strings in config are updated

### Requirement: Update Documentation

The system SHALL update all user-facing documentation to reflect the new project name and purpose.

#### Scenario: README updated
- **WHEN** someone views the project README
- **THEN** the title shows the new project name
- **AND** the description clarifies it's an information database
- **AND** the purpose section explains the rebranding
- **AND** links to old documentation are updated

#### Scenario: User guides updated
- **WHEN** users access help documentation
- **THEN** all user guides reference the new project name
- **AND** screenshots are updated to show new branding (if applicable)
- **AND** terminology is consistent throughout

### Requirement: Backward Compatibility

The system SHALL ensure no breaking changes occur from the rebranding.

#### Scenario: External links continue to work
- **WHEN** external websites link to the portal
- **THEN** all links continue to resolve correctly
- **AND** no content is moved or removed
- **AND** page structure remains compatible

#### Scenario: Bookmarks remain valid
- **WHEN** users access their bookmarked pages
- **THEN** bookmarks continue to work
- **AND** page content is accessible
- **AND** navigation is unchanged

#### Scenario: API consumers unaffected
- **WHEN** external systems call the API
- **THEN** API endpoints return same response format
- **AND** API authentication remains unchanged
- **AND** API versioning is maintained

## Technical Specifications

### Files to Update

#### Frontend Display Text
```
# Update in these files:
- index.html (main heading, title tag, meta description)
- pages/*.html (page titles, headings)
- manifest.json (name, short_name, description)
- assets/js/main.js (constants, error messages)
```

#### Meta Tags (index.html and all pages)
```html
<!-- OLD -->
<title>Lateral Entry Portal</title>
<meta name="description" content="Portal for lateral entry appointees in Government of India">

<!-- NEW -->
<title>Lateral Entry Officers Database</title>
<meta name="description" content="Comprehensive information database of lateral entry officers in Government of India - not an application portal">

<!-- Add clarification -->
<meta name="keywords" content="lateral entry, officers database, government of india, information, directory">
```

#### Homepage Clarification Section
```html
<section class="purpose-clarification">
  <div class="alert alert-info">
    <i class="fas fa-info-circle"></i>
    <strong>Note:</strong> This is an information database showcasing lateral entry officers. 
    To apply for lateral entry positions, please visit the 
    <a href="https://www.upsc.gov.in" target="_blank">UPSC website</a>.
  </div>
</section>
```

#### Suggested Project Names (User to Choose)

| Option | Pros | Cons |
|--------|------|------|
| Lateral Entry Officers Database | Clear, descriptive, SEO-friendly | Somewhat long |
| Lateral Entry Officers Directory | Professional, concise | Could imply contact directory only |
| Government Lateral Entry Officers Platform | Comprehensive | Very long |
| Lateral Entry Information Portal | Balanced | Still uses "Portal" |
| **Recommended: Lateral Entry Officers Database** | - | - |

### Configuration

```bash
# Display configuration (new environment variables)
PROJECT_DISPLAY_NAME="Lateral Entry Officers Database"
PROJECT_SHORT_NAME="LE Officers DB"
PROJECT_TAGLINE="Comprehensive database of lateral entry officers in Government of India"
PROJECT_PURPOSE="Information and professional networking platform"
```

### Files NOT to Change

```
# Keep unchanged to avoid breaking changes:
- Repository name: lateral-entry-portal
- Database filename: lateral_entry.db
- API base path: /lateral-entry/api
- Python module names: lateral_entry_*
- CSS class names: .lateral-entry-*
- Environment variables: LATERAL_ENTRY_*
- Log file names: lateral_entry.log
```

### Documentation Updates Required

1. **README.md**
   - Update title
   - Update description
   - Add "About the Rebranding" section
   - Update screenshots (if showing old name)

2. **PROJECT_SUMMARY.md**
   - Update purpose statement
   - Clarify it's not an application portal

3. **USAGE_GUIDE.md**
   - Update all references to project name
   - Add FAQ about applying to lateral entry

4. **DEPLOYMENT_GUIDE.md**
   - Update display configuration instructions
   - Note: technical paths remain unchanged

## User Interface Changes

### Before (Current)

```
┌─────────────────────────────────────────────┐
│ Lateral Entry Portal                        │
│ ─────────────────────────────────────────── │
│ View lateral entry appointees to Government │
│ of India                                     │
└─────────────────────────────────────────────┘
```

### After (Proposed)

```
┌─────────────────────────────────────────────┐
│ Lateral Entry Officers Database             │
│ ─────────────────────────────────────────── │
│ Comprehensive information database of       │
│ lateral entry officers in Government of     │
│ India                                        │
│                                              │
│ ℹ️ Note: This is an information platform.   │
│ To apply for lateral entry, visit UPSC.     │
└─────────────────────────────────────────────┘
```

### Footer Update

```
<!-- OLD -->
<footer>
  © 2025 Lateral Entry Portal
</footer>

<!-- NEW -->
<footer>
  © 2025 Lateral Entry Officers Database
  <br>
  <small>Information platform - not for applications</small>
</footer>
```

## Testing Strategy

### Manual Testing
- [ ] Verify homepage displays new name
- [ ] Verify all page titles updated
- [ ] Verify browser tabs show new name
- [ ] Verify footer shows new name
- [ ] Verify meta tags updated
- [ ] Verify clarification message displays
- [ ] Verify all internal links work
- [ ] Verify external links work
- [ ] Verify API endpoints unchanged
- [ ] Verify no console errors

### Automated Testing
```bash
# Test script to verify branding consistency
grep -r "Lateral Entry Portal" pages/*.html
# Should return 0 results after update

# Verify new name is present
grep -r "Lateral Entry Officers Database" pages/*.html
# Should return multiple results

# Verify URLs unchanged
curl -I https://prabhu.app/lateral-entry/
# Should return 200 OK
```

### SEO Testing
- Use Google Search Console to verify:
  - Meta tags updated
  - Descriptions accurate
  - No duplicate content issues
  - Search results show new name within 2-4 weeks

## Implementation Steps

1. **Update Display Strings**
   - Update index.html title and headings
   - Update all pages/*.html titles
   - Update manifest.json
   - Update constants in main.js

2. **Add Clarification Messaging**
   - Add info banner on homepage
   - Update About section
   - Add FAQ entry
   - Update footer

3. **Update Meta Tags**
   - Update all title tags
   - Update all meta descriptions
   - Update Open Graph tags
   - Update Twitter Card tags

4. **Update Documentation**
   - Update README.md
   - Update PROJECT_SUMMARY.md
   - Update user guides
   - Update deployment docs

5. **Test Thoroughly**
   - Manual testing on all pages
   - Link checking (internal and external)
   - SEO validation
   - Cross-browser testing

6. **Deploy Changes**
   - Deploy to staging first
   - Verify staging
   - Deploy to production
   - Monitor for issues

## Rollback Plan

If issues arise:
1. Revert HTML/JS changes (simple text revert)
2. Revert meta tag changes
3. Revert documentation (git revert)
4. No database or API changes needed (nothing changed)
5. Clear CDN cache if applicable

## Success Criteria

- [ ] Homepage displays new project name
- [ ] All pages show consistent branding
- [ ] Meta tags reflect new name and purpose
- [ ] Clarification message about application process is prominent
- [ ] No 404 errors or broken links
- [ ] All external links continue to work
- [ ] API functionality unchanged
- [ ] Documentation updated
- [ ] User feedback is positive
- [ ] Search engine results updated within 4 weeks
- [ ] No confusion about how to apply for lateral entry

## Timeline

- **Preparation**: 1 day (finalize new name with user)
- **Implementation**: 2 days (update files, documentation)
- **Testing**: 1 day (thorough testing)
- **Deployment**: 1 day (staging → production)
- **Total**: ~5 days

## Related Specifications

- [Homepage Design](../../specs/frontend/homepage.md)
- [SEO Optimization](../../specs/seo/spec.md)
- [Documentation Standards](../../specs/documentation/spec.md)
