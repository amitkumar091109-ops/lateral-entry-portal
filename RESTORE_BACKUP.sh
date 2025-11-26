#!/bin/bash
# One-Click Restore Script for Lateral Entry Portal
# Restores system to state before user-profiles-and-feeds implementation
# Created: 2025-11-25 16:48:02
# Backup ID: pre-user-profiles-20251125_164802

set -e

BACKUP_DIR="/home/ubuntu/projects/lateral-entry-portal/backups/pre-user-profiles-20251125_164802"
PROJECT_DIR="/home/ubuntu/projects/lateral-entry-portal"

echo "=========================================="
echo "Lateral Entry Portal - Restore Script"
echo "=========================================="
echo ""
echo "This will restore your portal to the state BEFORE user profiles implementation."
echo ""
echo "⚠️  WARNING: This will:"
echo "   - Remove all new user accounts and authentication data"
echo "   - Remove all uploaded files"
echo "   - Restore database to previous state"
echo "   - Remove new API endpoints and admin panel"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "Starting restore process..."
echo ""

# Stop API server if running
echo "[1/7] Stopping API server (if running)..."
pkill -f "api/server.py" 2>/dev/null || echo "   No API server running"

# Backup current state before restore (just in case)
echo "[2/7] Creating safety backup of current state..."
SAFETY_BACKUP="$PROJECT_DIR/backups/safety-backup-before-restore-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SAFETY_BACKUP"
cp -r "$PROJECT_DIR/database" "$SAFETY_BACKUP/" 2>/dev/null || true
cp -r "$PROJECT_DIR/api" "$SAFETY_BACKUP/" 2>/dev/null || true
cp -r "$PROJECT_DIR/uploads" "$SAFETY_BACKUP/" 2>/dev/null || true
echo "   Safety backup created at: $SAFETY_BACKUP"

# Restore database
echo "[3/7] Restoring database..."
rm -rf "$PROJECT_DIR/database"
cp -r "$BACKUP_DIR/database" "$PROJECT_DIR/"
echo "   ✓ Database restored"

# Restore pages
echo "[4/7] Restoring pages..."
rm -rf "$PROJECT_DIR/pages"
cp -r "$BACKUP_DIR/pages" "$PROJECT_DIR/"
echo "   ✓ Pages restored"

# Restore assets
echo "[5/7] Restoring assets..."
rm -rf "$PROJECT_DIR/assets"
cp -r "$BACKUP_DIR/assets" "$PROJECT_DIR/"
echo "   ✓ Assets restored"

# Restore index.html
echo "[6/7] Restoring index.html..."
cp "$BACKUP_DIR/index.html" "$PROJECT_DIR/"
echo "   ✓ Index page restored"

# Remove new directories created during implementation
echo "[7/7] Cleaning up new implementation files..."
rm -rf "$PROJECT_DIR/api" 2>/dev/null || true
rm -rf "$PROJECT_DIR/uploads" 2>/dev/null || true
rm -rf "$PROJECT_DIR/scripts" 2>/dev/null || true
rm -f "$PROJECT_DIR/requirements.txt" 2>/dev/null || true
rm -f "$PROJECT_DIR/.env" 2>/dev/null || true
echo "   ✓ New files removed"

echo ""
echo "=========================================="
echo "✓ Restore completed successfully!"
echo "=========================================="
echo ""
echo "Your portal has been restored to its previous state."
echo ""
echo "Next steps:"
echo "1. Test the portal: python3 -m http.server 8000"
echo "2. Visit: http://localhost:8000/"
echo "3. If you need the new features back, check the safety backup at:"
echo "   $SAFETY_BACKUP"
echo ""
echo "The original backup is preserved at:"
echo "   $BACKUP_DIR"
echo ""
