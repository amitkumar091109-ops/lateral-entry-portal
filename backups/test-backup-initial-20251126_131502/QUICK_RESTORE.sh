#!/bin/bash
# Quick restore script for emergency use
# Run from backup directory: bash QUICK_RESTORE.sh

set -e
BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/ubuntu/projects/lateral-entry-portal"

echo "⚠️  WARNING: This will overwrite current project files!"
echo "Backup directory: $BACKUP_DIR"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo "🔄 Restoring from backup..."

# Restore database
cp -f "${BACKUP_DIR}/lateral_entry.db" "${PROJECT_ROOT}/database/"
cp -rf "${BACKUP_DIR}/database/"* "${PROJECT_ROOT}/database/"

# Restore data
cp -rf "${BACKUP_DIR}/data/"* "${PROJECT_ROOT}/data/"

# Restore API
cp -rf "${BACKUP_DIR}/api/"* "${PROJECT_ROOT}/api/"

# Restore frontend
cp -rf "${BACKUP_DIR}/pages/"* "${PROJECT_ROOT}/pages/"
cp -rf "${BACKUP_DIR}/assets/"* "${PROJECT_ROOT}/assets/"
cp -f "${BACKUP_DIR}/index.html" "${PROJECT_ROOT}/"
cp -f "${BACKUP_DIR}/manifest.json" "${PROJECT_ROOT}/" 2>/dev/null || true

echo "✅ Restore complete!"
echo "Please verify the application is working correctly."
