#!/bin/bash

################################################################################
# Lateral Entry Portal - Automated Backup System
# Creates complete project snapshots before each deployment phase
# Usage: ./backup_system.sh create <phase_name>
#        ./backup_system.sh restore <backup_name>
#        ./backup_system.sh list
################################################################################

set -e  # Exit on error

PROJECT_ROOT="/home/ubuntu/projects/lateral-entry-portal"
BACKUP_ROOT="${PROJECT_ROOT}/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create backup directory structure
initialize_backup_system() {
    if [ ! -d "$BACKUP_ROOT" ]; then
        mkdir -p "$BACKUP_ROOT"
        log_success "Created backup directory: $BACKUP_ROOT"
    fi
}

# Calculate directory size
get_size() {
    du -sh "$1" 2>/dev/null | cut -f1
}

# Create complete project backup
create_backup() {
    local phase_name=$1
    
    if [ -z "$phase_name" ]; then
        log_error "Phase name is required!"
        echo "Usage: ./backup_system.sh create <phase_name>"
        echo "Example: ./backup_system.sh create phase-0-foundation"
        exit 1
    fi
    
    local backup_name="${phase_name}-${TIMESTAMP}"
    local backup_dir="${BACKUP_ROOT}/${backup_name}"
    
    log_info "=========================================="
    log_info "Creating Backup: ${backup_name}"
    log_info "=========================================="
    
    # Create backup directory
    mkdir -p "$backup_dir"
    
    # 1. Backup Database (most critical)
    log_info "📦 Backing up database..."
    if [ -f "${PROJECT_ROOT}/database/lateral_entry.db" ]; then
        cp "${PROJECT_ROOT}/database/lateral_entry.db" "${backup_dir}/lateral_entry.db"
        sqlite3 "${PROJECT_ROOT}/database/lateral_entry.db" ".backup '${backup_dir}/lateral_entry.db.sqlite3backup'"
        log_success "Database backed up (2 formats for safety)"
    else
        log_warning "Database file not found!"
    fi
    
    # 2. Backup entire database directory
    log_info "📦 Backing up database directory..."
    cp -r "${PROJECT_ROOT}/database" "${backup_dir}/"
    
    # 3. Backup data directory (JSON exports)
    log_info "📦 Backing up data directory..."
    if [ -d "${PROJECT_ROOT}/data" ]; then
        cp -r "${PROJECT_ROOT}/data" "${backup_dir}/"
    fi
    
    # 4. Backup API server
    log_info "📦 Backing up API server..."
    if [ -d "${PROJECT_ROOT}/api" ]; then
        cp -r "${PROJECT_ROOT}/api" "${backup_dir}/"
    fi
    
    # 5. Backup frontend files
    log_info "📦 Backing up frontend files..."
    cp -r "${PROJECT_ROOT}/pages" "${backup_dir}/"
    cp -r "${PROJECT_ROOT}/assets" "${backup_dir}/"
    cp "${PROJECT_ROOT}/index.html" "${backup_dir}/" 2>/dev/null || true
    cp "${PROJECT_ROOT}/manifest.json" "${backup_dir}/" 2>/dev/null || true
    
    # 6. Backup configuration files
    log_info "📦 Backing up configuration files..."
    cp "${PROJECT_ROOT}/.gitignore" "${backup_dir}/" 2>/dev/null || true
    cp "${PROJECT_ROOT}/requirements.txt" "${backup_dir}/" 2>/dev/null || true
    cp "${PROJECT_ROOT}"/*.md "${backup_dir}/" 2>/dev/null || true
    
    # 7. Backup OpenSpec changes (if they exist)
    if [ -d "${PROJECT_ROOT}/openspec" ]; then
        log_info "📦 Backing up OpenSpec changes..."
        cp -r "${PROJECT_ROOT}/openspec" "${backup_dir}/"
    fi
    
    # 8. Create backup manifest
    log_info "📦 Creating backup manifest..."
    cat > "${backup_dir}/BACKUP_MANIFEST.txt" <<EOF
================================================
LATERAL ENTRY PORTAL - BACKUP MANIFEST
================================================

Backup Name: ${backup_name}
Phase: ${phase_name}
Created: $(date)
Backup Directory: ${backup_dir}

================================================
CONTENTS
================================================

Database:
- lateral_entry.db (SQLite primary)
- lateral_entry.db.sqlite3backup (SQLite backup format)
- database/ directory (complete)

Data:
- data/ directory (JSON exports, scripts)

API:
- api/ directory (Flask server)

Frontend:
- pages/ directory (HTML pages)
- assets/ directory (CSS, JS, images)
- index.html (homepage)
- manifest.json (PWA manifest)

Configuration:
- requirements.txt
- .gitignore
- Documentation files (*.md)

OpenSpec:
- openspec/ directory (change proposals)

================================================
DATABASE STATISTICS (at backup time)
================================================

$(sqlite3 "${backup_dir}/lateral_entry.db" "
SELECT 'Total Entrants: ' || COUNT(*) FROM lateral_entrants;
SELECT 'Total Tables: ' || COUNT(*) FROM sqlite_master WHERE type='table';
" 2>/dev/null || echo "Unable to read database stats")

================================================
BACKUP SIZE
================================================

Total Size: $(get_size "$backup_dir")

================================================
RESTORATION
================================================

To restore this backup:
    ./backup_system.sh restore ${backup_name}

To verify this backup:
    ./backup_system.sh verify ${backup_name}

================================================
EOF
    
    # 9. Create quick restore script
    cat > "${backup_dir}/QUICK_RESTORE.sh" <<'EOF'
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
EOF
    chmod +x "${backup_dir}/QUICK_RESTORE.sh"
    
    # 10. Create verification checksums
    log_info "📦 Creating checksums for verification..."
    find "$backup_dir" -type f -exec md5sum {} \; > "${backup_dir}/CHECKSUMS.md5" 2>/dev/null || true
    
    # 11. Compress backup (optional, for space saving)
    log_info "📦 Creating compressed archive..."
    tar -czf "${backup_dir}.tar.gz" -C "$BACKUP_ROOT" "$backup_name" 2>/dev/null || log_warning "Compression failed (non-critical)"
    
    # Display summary
    log_success "=========================================="
    log_success "Backup Complete!"
    log_success "=========================================="
    echo ""
    echo "Backup Name: ${backup_name}"
    echo "Location: ${backup_dir}"
    echo "Size: $(get_size "$backup_dir")"
    echo "Compressed: ${backup_dir}.tar.gz ($(get_size "${backup_dir}.tar.gz" 2>/dev/null || echo "N/A"))"
    echo ""
    echo "📄 Manifest: ${backup_dir}/BACKUP_MANIFEST.txt"
    echo "🚀 Quick Restore: ${backup_dir}/QUICK_RESTORE.sh"
    echo ""
    log_info "To restore: ./backup_system.sh restore ${backup_name}"
    log_success "=========================================="
}

# Restore from backup
restore_backup() {
    local backup_name=$1
    
    if [ -z "$backup_name" ]; then
        log_error "Backup name is required!"
        echo "Usage: ./backup_system.sh restore <backup_name>"
        echo ""
        echo "Available backups:"
        list_backups
        exit 1
    fi
    
    local backup_dir="${BACKUP_ROOT}/${backup_name}"
    
    if [ ! -d "$backup_dir" ]; then
        log_error "Backup not found: ${backup_name}"
        echo ""
        echo "Available backups:"
        list_backups
        exit 1
    fi
    
    log_warning "=========================================="
    log_warning "⚠️  WARNING: RESTORE OPERATION"
    log_warning "=========================================="
    echo ""
    echo "This will OVERWRITE current project files with:"
    echo "Backup: ${backup_name}"
    echo "Location: ${backup_dir}"
    echo ""
    cat "${backup_dir}/BACKUP_MANIFEST.txt" 2>/dev/null | head -15 || true
    echo ""
    read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm
    
    if [ "$confirm" != "yes" ]; then
        log_info "Restore cancelled."
        exit 0
    fi
    
    log_info "=========================================="
    log_info "Starting Restore Process..."
    log_info "=========================================="
    
    # Create emergency backup of current state
    log_info "📦 Creating emergency backup of current state..."
    create_backup "emergency-pre-restore"
    
    # Restore database
    log_info "🔄 Restoring database..."
    cp -f "${backup_dir}/lateral_entry.db" "${PROJECT_ROOT}/database/"
    cp -rf "${backup_dir}/database/"* "${PROJECT_ROOT}/database/"
    
    # Restore data
    log_info "🔄 Restoring data directory..."
    rm -rf "${PROJECT_ROOT}/data"
    cp -r "${backup_dir}/data" "${PROJECT_ROOT}/"
    
    # Restore API
    log_info "🔄 Restoring API server..."
    rm -rf "${PROJECT_ROOT}/api"
    cp -r "${backup_dir}/api" "${PROJECT_ROOT}/"
    
    # Restore frontend
    log_info "🔄 Restoring frontend files..."
    rm -rf "${PROJECT_ROOT}/pages"
    cp -r "${backup_dir}/pages" "${PROJECT_ROOT}/"
    
    rm -rf "${PROJECT_ROOT}/assets"
    cp -r "${backup_dir}/assets" "${PROJECT_ROOT}/"
    
    cp -f "${backup_dir}/index.html" "${PROJECT_ROOT}/"
    cp -f "${backup_dir}/manifest.json" "${PROJECT_ROOT}/" 2>/dev/null || true
    
    # Restore OpenSpec if it exists
    if [ -d "${backup_dir}/openspec" ]; then
        log_info "🔄 Restoring OpenSpec changes..."
        rm -rf "${PROJECT_ROOT}/openspec"
        cp -r "${backup_dir}/openspec" "${PROJECT_ROOT}/"
    fi
    
    log_success "=========================================="
    log_success "✅ Restore Complete!"
    log_success "=========================================="
    echo ""
    echo "Restored from: ${backup_name}"
    echo ""
    log_info "Next steps:"
    echo "1. Verify database: sqlite3 ${PROJECT_ROOT}/database/lateral_entry.db 'SELECT COUNT(*) FROM lateral_entrants;'"
    echo "2. Test frontend: Open index.html in browser"
    echo "3. Test API: uv run python api/server.py"
    echo ""
}

# List all available backups
list_backups() {
    log_info "=========================================="
    log_info "Available Backups"
    log_info "=========================================="
    echo ""
    
    if [ ! -d "$BACKUP_ROOT" ] || [ -z "$(ls -A "$BACKUP_ROOT" 2>/dev/null)" ]; then
        log_warning "No backups found."
        return
    fi
    
    local count=0
    for backup_dir in "$BACKUP_ROOT"/*; do
        if [ -d "$backup_dir" ]; then
            count=$((count + 1))
            local backup_name=$(basename "$backup_dir")
            local size=$(get_size "$backup_dir")
            local date=$(stat -c %y "$backup_dir" 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)
            
            echo "${count}. ${backup_name}"
            echo "   Size: ${size}"
            echo "   Date: ${date}"
            
            if [ -f "${backup_dir}/BACKUP_MANIFEST.txt" ]; then
                local phase=$(grep "^Phase:" "${backup_dir}/BACKUP_MANIFEST.txt" | cut -d' ' -f2-)
                echo "   Phase: ${phase}"
            fi
            echo ""
        fi
    done
    
    if [ $count -eq 0 ]; then
        log_warning "No backups found."
    else
        log_success "Total backups: ${count}"
    fi
}

# Verify backup integrity
verify_backup() {
    local backup_name=$1
    
    if [ -z "$backup_name" ]; then
        log_error "Backup name is required!"
        echo "Usage: ./backup_system.sh verify <backup_name>"
        exit 1
    fi
    
    local backup_dir="${BACKUP_ROOT}/${backup_name}"
    
    if [ ! -d "$backup_dir" ]; then
        log_error "Backup not found: ${backup_name}"
        exit 1
    fi
    
    log_info "=========================================="
    log_info "Verifying Backup: ${backup_name}"
    log_info "=========================================="
    
    # Check database
    log_info "Checking database integrity..."
    if sqlite3 "${backup_dir}/lateral_entry.db" "PRAGMA integrity_check;" | grep -q "ok"; then
        log_success "✅ Database integrity: OK"
    else
        log_error "❌ Database integrity: FAILED"
    fi
    
    # Check checksums
    if [ -f "${backup_dir}/CHECKSUMS.md5" ]; then
        log_info "Verifying file checksums..."
        cd "$backup_dir"
        if md5sum -c CHECKSUMS.md5 --quiet 2>/dev/null; then
            log_success "✅ File checksums: OK"
        else
            log_error "❌ File checksums: FAILED"
        fi
        cd - > /dev/null
    fi
    
    # Display backup info
    echo ""
    cat "${backup_dir}/BACKUP_MANIFEST.txt" 2>/dev/null || log_warning "Manifest not found"
    
    log_success "=========================================="
    log_success "Verification Complete"
    log_success "=========================================="
}

# Delete old backups (keep last N)
cleanup_backups() {
    local keep_count=${1:-10}
    
    log_info "Cleaning up old backups (keeping last ${keep_count})..."
    
    local backup_count=$(find "$BACKUP_ROOT" -maxdepth 1 -type d | wc -l)
    backup_count=$((backup_count - 1))  # Exclude the backup root itself
    
    if [ $backup_count -le $keep_count ]; then
        log_info "Current backup count (${backup_count}) is within limit (${keep_count}). No cleanup needed."
        return
    fi
    
    log_info "Found ${backup_count} backups, removing oldest..."
    
    # Find and delete oldest backups
    find "$BACKUP_ROOT" -maxdepth 1 -type d | sort | head -n -${keep_count} | while read dir; do
        if [ "$dir" != "$BACKUP_ROOT" ]; then
            log_info "Deleting old backup: $(basename "$dir")"
            rm -rf "$dir"
            rm -f "${dir}.tar.gz"
        fi
    done
    
    log_success "Cleanup complete."
}

# Show usage
show_usage() {
    cat <<EOF
========================================
Lateral Entry Portal - Backup System
========================================

Usage: ./backup_system.sh <command> [options]

Commands:
    create <phase_name>     Create a new backup
                           Example: ./backup_system.sh create phase-0-foundation
    
    restore <backup_name>   Restore from a backup
                           Example: ./backup_system.sh restore phase-0-foundation-20250126_120000
    
    list                   List all available backups
    
    verify <backup_name>   Verify backup integrity
    
    cleanup [keep_count]   Delete old backups (default: keep last 10)
    
    help                   Show this help message

Examples:
    # Before starting Phase 0
    ./backup_system.sh create phase-0-foundation
    
    # List all backups
    ./backup_system.sh list
    
    # Restore from a backup
    ./backup_system.sh restore phase-0-foundation-20250126_120000
    
    # Verify backup
    ./backup_system.sh verify phase-0-foundation-20250126_120000

========================================
EOF
}

# Main command dispatcher
main() {
    initialize_backup_system
    
    case "${1:-help}" in
        create)
            create_backup "$2"
            ;;
        restore)
            restore_backup "$2"
            ;;
        list)
            list_backups
            ;;
        verify)
            verify_backup "$2"
            ;;
        cleanup)
            cleanup_backups "$2"
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
