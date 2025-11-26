#!/bin/bash

################################################################################
# Lateral Entry Portal - Phase Management System
# Automatically creates backups before each phase and tracks progress
# Usage: ./phase_manager.sh start <phase_number>
#        ./phase_manager.sh rollback <phase_number>
#        ./phase_manager.sh status
################################################################################

set -e

PROJECT_ROOT="/home/ubuntu/projects/lateral-entry-portal"
PHASE_TRACKER="${PROJECT_ROOT}/.phase_tracker.json"
BACKUP_SCRIPT="${PROJECT_ROOT}/backup_system.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_phase() { echo -e "${MAGENTA}[PHASE]${NC} $1"; }

# Phase definitions
declare -A PHASES
PHASES[0]="Phase 0: Foundation & Project Rebranding"
PHASES[1]="Phase 1: Authentication Backend (Google OAuth)"
PHASES[2]="Phase 2: Admin Panel & User Management"
PHASES[3]="Phase 3: Granular Visibility Controls"
PHASES[4]="Phase 4: Profile Editing with Moderation"
PHASES[5]="Phase 5: File Upload System"
PHASES[6]="Phase 6: LinkedIn Integration"
PHASES[7]="Phase 7: AI Assistance"
PHASES[8]="Phase 8: Comprehensive Job Monitoring"
PHASES[9]="Phase 9: Social Feeds & News"
PHASES[10]="Phase 10: Testing & QA"
PHASES[11]="Phase 11: Deployment"

# Initialize phase tracker
initialize_tracker() {
    if [ ! -f "$PHASE_TRACKER" ]; then
        cat > "$PHASE_TRACKER" <<EOF
{
  "current_phase": -1,
  "phases": {},
  "created_at": "$(date -Iseconds)"
}
EOF
        log_success "Initialized phase tracker: $PHASE_TRACKER"
    fi
}

# Get current phase
get_current_phase() {
    if [ ! -f "$PHASE_TRACKER" ]; then
        echo "-1"
        return
    fi
    python3 -c "import json; print(json.load(open('$PHASE_TRACKER'))['current_phase'])"
}

# Update phase tracker
update_tracker() {
    local phase=$1
    local status=$2
    local backup_name=$3
    
    python3 <<EOF
import json
from datetime import datetime

with open('$PHASE_TRACKER', 'r') as f:
    data = json.load(f)

if '$phase' not in data['phases']:
    data['phases']['$phase'] = {}

data['phases']['$phase']['status'] = '$status'
data['phases']['$phase']['backup'] = '$backup_name'
data['phases']['$phase']['timestamp'] = datetime.now().isoformat()

if '$status' == 'started':
    data['current_phase'] = int('$phase')
elif '$status' == 'completed':
    pass  # Keep current phase as is
elif '$status' == 'rolled_back':
    data['current_phase'] = int('$phase') - 1

with open('$PHASE_TRACKER', 'w') as f:
    json.dump(data, f, indent=2)
EOF
}

# Start a new phase
start_phase() {
    local phase_num=$1
    
    if [ -z "$phase_num" ]; then
        log_error "Phase number is required!"
        show_usage
        exit 1
    fi
    
    if [ -z "${PHASES[$phase_num]}" ]; then
        log_error "Invalid phase number: $phase_num"
        echo "Valid phases: 0-11"
        exit 1
    fi
    
    local current_phase=$(get_current_phase)
    
    log_phase "=========================================="
    log_phase "Starting ${PHASES[$phase_num]}"
    log_phase "=========================================="
    echo ""
    
    # Verify prerequisites
    if [ $phase_num -gt 0 ] && [ $current_phase -lt $((phase_num - 1)) ]; then
        log_warning "⚠️  Warning: Previous phase not completed!"
        echo "Current phase: $current_phase"
        echo "Attempting to start: $phase_num"
        read -p "Continue anyway? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log_info "Phase start cancelled."
            exit 0
        fi
    fi
    
    # Create backup
    local backup_name="phase-${phase_num}-pre-start"
    log_info "📦 Creating backup before starting phase..."
    echo ""
    
    if bash "$BACKUP_SCRIPT" create "$backup_name"; then
        log_success "Backup created successfully!"
        echo ""
        
        # Update tracker
        update_tracker "$phase_num" "started" "$backup_name"
        
        # Show phase checklist
        show_phase_checklist "$phase_num"
        
        log_success "=========================================="
        log_success "Phase $phase_num ready to begin!"
        log_success "=========================================="
        echo ""
        echo "📋 Backup: $backup_name"
        echo "🔄 To rollback: ./phase_manager.sh rollback $phase_num"
        echo ""
    else
        log_error "Backup failed! Cannot start phase."
        exit 1
    fi
}

# Show phase-specific checklist
show_phase_checklist() {
    local phase_num=$1
    
    echo ""
    log_info "=========================================="
    log_info "Phase $phase_num Checklist"
    log_info "=========================================="
    
    case $phase_num in
        0)
            cat <<EOF

Tasks:
□ Update homepage title to "Lateral Entry Officers Database"
□ Add clarification text about portal purpose
□ Update meta descriptions
□ Update footer and manifest.json
□ Test all existing functionality still works

Files to modify:
- index.html
- pages/*.html
- manifest.json

Estimated time: 2-3 hours
Risk level: LOW (text changes only)
EOF
            ;;
        1)
            cat <<EOF

Tasks:
□ Install Flask-Login and google-auth libraries
□ Create users and sessions tables
□ Implement /api/auth/* endpoints
□ Add session middleware
□ Test OAuth flow
□ Verify existing API endpoints still work

Files to modify:
- api/server.py
- database/lateral_entry_schema.sql (add tables)
- requirements.txt

Estimated time: 3-4 days
Risk level: MEDIUM (new backend features)
EOF
            ;;
        2)
            cat <<EOF

Tasks:
□ Create admin panel UI (pages/admin.html)
□ Implement user approval workflow
□ Link Google accounts to entrant profiles
□ Add admin-only API endpoints
□ Test approval flow end-to-end

Files to modify:
- pages/admin.html (new)
- api/server.py
- assets/js/admin.js (new)

Estimated time: 2-3 days
Risk level: MEDIUM (admin features)
EOF
            ;;
        3)
            cat <<EOF

Tasks:
□ Add field_visibility column to lateral_entrants
□ Create visibility control UI
□ Implement API filtering based on user role
□ Test public vs authenticated views
□ Add audit logging

Files to modify:
- database/lateral_entry_schema.sql
- api/server.py (visibility filtering)
- pages/my-profile.html (new)
- assets/js/main.js

Estimated time: 1 week
Risk level: MEDIUM (data visibility changes)
EOF
            ;;
        4)
            cat <<EOF

Tasks:
□ Create profile editing UI
□ Implement moderation workflow
□ Add edit history tracking
□ Test approval process
□ Verify public view unchanged for unapproved edits

Files to modify:
- pages/my-profile.html
- api/server.py (edit endpoints)
- database/lateral_entry_schema.sql (edit_history table)

Estimated time: 3-4 days
Risk level: MEDIUM (profile editing)
EOF
            ;;
        5)
            cat <<EOF

Tasks:
□ Implement file upload endpoints
□ Add virus scanning
□ Create moderation queue for uploads
□ Test file size limits
□ Implement CDN/storage integration

Files to modify:
- api/server.py (upload endpoints)
- database/lateral_entry_schema.sql (uploads table)
- pages/my-profile.html (upload UI)

Estimated time: 3-4 days
Risk level: HIGH (file uploads = security risk)
EOF
            ;;
        6)
            cat <<EOF

Tasks:
□ Implement LinkedIn OAuth (optional)
□ Create field mapping UI
□ Add sync functionality
□ Test manual profile URL entry (Option B)
□ Store encrypted tokens

Files to modify:
- api/server.py (LinkedIn integration)
- database/lateral_entry_schema.sql (LinkedIn fields)
- pages/my-profile.html (LinkedIn section)

Estimated time: 1 week
Risk level: MEDIUM (external API integration)
EOF
            ;;
        7)
            cat <<EOF

Tasks:
□ Integrate AI model for text generation
□ Add profile summary suggestions
□ Test AI quality and safety
□ Implement rate limiting
□ Add moderation for AI-generated content

Files to modify:
- api/server.py (AI endpoints)
- pages/my-profile.html (AI assistance UI)

Estimated time: 2-3 days
Risk level: MEDIUM (AI integration)
EOF
            ;;
        8)
            cat <<EOF

Tasks:
□ Create job_postings and user_job_preferences tables
□ Set up Parallel AI Monitor
□ Create comprehensive job search prompt
□ Build job board UI (authenticated only)
□ Implement notification system
□ Add relevance scoring

Files to modify:
- database/lateral_entry_schema.sql (job tables)
- api/server.py (job endpoints)
- pages/jobs.html (new)
- assets/js/jobs.js (new)

Estimated time: 2 weeks
Risk level: MEDIUM (new major feature)
EOF
            ;;
        9)
            cat <<EOF

Tasks:
□ Create news_posts table
□ Build admin content management
□ Add homepage feed carousel
□ Implement social media integration (optional)
□ Test feed rendering

Files to modify:
- database/lateral_entry_schema.sql (news table)
- api/server.py (news endpoints)
- index.html (feed section)
- pages/admin.html (content management)

Estimated time: 2 weeks
Risk level: LOW (optional feature)
EOF
            ;;
        10)
            cat <<EOF

Tasks:
□ Write comprehensive test suite
□ Test backward compatibility
□ Security audit
□ Performance testing
□ Mobile testing
□ Browser compatibility testing

Files to create:
- tests/test_backward_compatibility.py
- tests/test_authentication.py
- tests/test_visibility_controls.py
- tests/test_api_endpoints.py

Estimated time: 1 week
Risk level: LOW (testing only)
EOF
            ;;
        11)
            cat <<EOF

Tasks:
□ Export static JSON files
□ Update deployment package
□ Test on staging environment
□ Create deployment documentation
□ Deploy to production
□ Monitor for issues

Files to verify:
- data/entrants.json
- data/stats.json
- All frontend files

Estimated time: 2-3 days
Risk level: HIGH (production deployment)
EOF
            ;;
    esac
    
    echo ""
    log_info "=========================================="
}

# Complete a phase
complete_phase() {
    local phase_num=$1
    
    if [ -z "$phase_num" ]; then
        log_error "Phase number is required!"
        exit 1
    fi
    
    log_info "Marking Phase $phase_num as completed..."
    
    # Create post-completion backup
    local backup_name="phase-${phase_num}-completed"
    log_info "📦 Creating post-completion backup..."
    
    if bash "$BACKUP_SCRIPT" create "$backup_name"; then
        update_tracker "$phase_num" "completed" "$backup_name"
        log_success "Phase $phase_num marked as completed!"
        
        # Show next phase
        local next_phase=$((phase_num + 1))
        if [ -n "${PHASES[$next_phase]}" ]; then
            echo ""
            log_info "Next phase: ${PHASES[$next_phase]}"
            log_info "To start: ./phase_manager.sh start $next_phase"
        fi
    else
        log_error "Post-completion backup failed!"
        exit 1
    fi
}

# Rollback a phase
rollback_phase() {
    local phase_num=$1
    
    if [ -z "$phase_num" ]; then
        log_error "Phase number is required!"
        exit 1
    fi
    
    log_warning "=========================================="
    log_warning "⚠️  ROLLBACK Phase $phase_num"
    log_warning "=========================================="
    echo ""
    
    # Get backup name from tracker
    local backup_name=$(python3 -c "import json; data=json.load(open('$PHASE_TRACKER')); print(data['phases'].get('$phase_num', {}).get('backup', ''))")
    
    if [ -z "$backup_name" ]; then
        log_error "No backup found for Phase $phase_num"
        echo ""
        log_info "Available backups:"
        bash "$BACKUP_SCRIPT" list
        exit 1
    fi
    
    echo "This will restore the backup from before Phase $phase_num started."
    echo "Backup: $backup_name"
    echo ""
    read -p "Continue with rollback? (type 'yes' to confirm): " confirm
    
    if [ "$confirm" != "yes" ]; then
        log_info "Rollback cancelled."
        exit 0
    fi
    
    # Perform rollback
    if bash "$BACKUP_SCRIPT" restore "$backup_name"; then
        update_tracker "$phase_num" "rolled_back" "$backup_name"
        log_success "=========================================="
        log_success "✅ Rollback Complete!"
        log_success "=========================================="
        echo ""
        echo "Project restored to state before Phase $phase_num"
        echo ""
        log_info "Next steps:"
        echo "1. Verify the application is working: Open index.html"
        echo "2. Test the API: uv run python api/server.py"
        echo "3. Check the database: sqlite3 database/lateral_entry.db"
    else
        log_error "Rollback failed!"
        exit 1
    fi
}

# Show status
show_status() {
    initialize_tracker
    
    log_info "=========================================="
    log_info "Phase Progress Status"
    log_info "=========================================="
    echo ""
    
    local current_phase=$(get_current_phase)
    echo "Current Phase: ${current_phase}"
    echo ""
    
    for phase_num in {0..11}; do
        local status=$(python3 -c "import json; data=json.load(open('$PHASE_TRACKER')); print(data['phases'].get('$phase_num', {}).get('status', 'not_started'))" 2>/dev/null || echo "not_started")
        
        local icon="⚪"
        local color="$NC"
        
        case $status in
            started)
                icon="🔵"
                color="$BLUE"
                ;;
            completed)
                icon="✅"
                color="$GREEN"
                ;;
            rolled_back)
                icon="🔙"
                color="$YELLOW"
                ;;
            not_started)
                icon="⚪"
                color="$NC"
                ;;
        esac
        
        echo -e "${color}${icon} Phase ${phase_num}: ${PHASES[$phase_num]} [${status}]${NC}"
    done
    
    echo ""
    log_info "=========================================="
    
    if [ $current_phase -ge 0 ] && [ $current_phase -le 11 ]; then
        echo ""
        log_info "Current Phase Details:"
        show_phase_checklist "$current_phase"
    fi
}

# Show usage
show_usage() {
    cat <<EOF
========================================
Phase Management System
========================================

Usage: ./phase_manager.sh <command> [phase_number]

Commands:
    start <phase>      Start a new phase (auto-creates backup)
    complete <phase>   Mark phase as completed
    rollback <phase>   Rollback to before phase started
    status            Show progress status
    help              Show this help message

Examples:
    # Start Phase 0 (creates backup automatically)
    ./phase_manager.sh start 0
    
    # Mark Phase 0 as completed
    ./phase_manager.sh complete 0
    
    # Rollback Phase 0 if something went wrong
    ./phase_manager.sh rollback 0
    
    # Check progress
    ./phase_manager.sh status

Phases:
EOF
    for phase_num in {0..11}; do
        echo "  ${phase_num}. ${PHASES[$phase_num]}"
    done
    
    cat <<EOF

========================================
EOF
}

# Main
main() {
    initialize_tracker
    
    case "${1:-help}" in
        start)
            start_phase "$2"
            ;;
        complete)
            complete_phase "$2"
            ;;
        rollback)
            rollback_phase "$2"
            ;;
        status)
            show_status
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

main "$@"
