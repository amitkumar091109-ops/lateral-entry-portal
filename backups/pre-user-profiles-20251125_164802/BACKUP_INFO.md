# Backup and Restore Information

**Backup Created**: 2025-11-25 16:48:02  
**Backup ID**: `pre-user-profiles-20251125_164802`  
**Purpose**: Complete system backup before implementing user-editable profiles and social feeds feature

## What's Backed Up

This backup contains the complete state of the Lateral Entry Portal **before** implementing the new user profiles feature:

- ✅ Database (`database/lateral_entry.db` and all schema files)
- ✅ All HTML pages (`pages/*.html`)
- ✅ All assets (CSS, JavaScript, images)
- ✅ Main index.html
- ✅ Data files and exports

## One-Click Restore

To restore the portal to this exact state, run:

```bash
cd /home/ubuntu/projects/lateral-entry-portal
./RESTORE_BACKUP.sh
```

The restore script will:
1. Stop any running API server
2. Create a safety backup of current state
3. Restore all files from this backup
4. Remove new implementation files (api/, uploads/, scripts/)
5. Clean up configuration files (.env, requirements.txt)

## Backup Location

```
/home/ubuntu/projects/lateral-entry-portal/backups/pre-user-profiles-20251125_164802/
├── database/          # Complete database backup
├── pages/             # All HTML pages
├── assets/            # CSS, JS, images
├── data/              # JSON exports
└── index.html         # Main page
```

## Safety Features

- Restore script creates a safety backup before restoring
- Original backup is never deleted
- Confirmation required before restore
- All operations logged

## Testing Restore

You can test the restore process in a development environment first:

```bash
# Test restore (will ask for confirmation)
./RESTORE_BACKUP.sh

# Then test the portal
python3 -m http.server 8000
# Visit: http://localhost:8000/
```

## Related Files

- **Restore Script**: `RESTORE_BACKUP.sh` (executable)
- **Implementation Proposal**: `openspec/changes/add-user-profiles-and-feeds/`

## Notes

- This backup represents the state BEFORE any user profile features
- No authentication system
- No file upload capability
- No admin panel
- Static JSON-based content only
