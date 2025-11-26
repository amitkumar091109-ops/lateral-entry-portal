"""
Admin Routes
API endpoints for administrative functions
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from ..database import db, row_to_dict
from ..auth.decorators import require_admin
from ..auth.session_manager import session_manager

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# ============================================================================
# User Management
# ============================================================================

@admin_bp.route('/users/pending', methods=['GET'])
@require_admin
def get_pending_users():
    """Get all pending user approval requests"""
    try:
        users = db.execute("""
            SELECT
                id, google_id, email, name, picture_url,
                requested_at, ip_address, user_agent
            FROM pending_users
            ORDER BY requested_at DESC
        """)

        return jsonify({
            'success': True,
            'users': [row_to_dict(u) for u in users]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/pending/<int:pending_id>/approve', methods=['POST'])
@require_admin
def approve_user(pending_id):
    """Approve a pending user"""
    try:
        data = request.get_json() or {}
        entrant_id = data.get('entrant_id')  # Optional: link to existing entrant

        # Get pending user
        pending = db.execute_one("""
            SELECT * FROM pending_users WHERE id = ?
        """, (pending_id,))

        if not pending:
            return jsonify({'error': 'Pending user not found'}), 404

        pending_dict = row_to_dict(pending)

        # Create user account
        user_id = db.insert("""
            INSERT INTO users (
                google_id, email, name, picture_url,
                entrant_id, role, is_approved, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pending_dict['google_id'],
            pending_dict['email'],
            pending_dict['name'],
            pending_dict['picture_url'],
            entrant_id,
            'appointee',
            True,
            True
        ))

        # Delete from pending_users
        db.execute("DELETE FROM pending_users WHERE id = ?", (pending_id,))

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'approve_user',
            'user',
            user_id,
            'pending',
            'approved',
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'User approved successfully',
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/pending/<int:pending_id>/reject', methods=['POST'])
@require_admin
def reject_user(pending_id):
    """Reject a pending user"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'No reason provided')

        # Get pending user
        pending = db.execute_one("""
            SELECT * FROM pending_users WHERE id = ?
        """, (pending_id,))

        if not pending:
            return jsonify({'error': 'Pending user not found'}), 404

        # Delete from pending_users
        db.execute("DELETE FROM pending_users WHERE id = ?", (pending_id,))

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'reject_user',
            'pending_user',
            pending_id,
            'pending',
            f'rejected: {reason}',
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'User rejected successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_all_users():
    """Get all approved users"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        search = request.args.get('search', '')

        offset = (page - 1) * per_page

        # Build query
        where_clause = ""
        params = []

        if search:
            where_clause = "WHERE email LIKE ? OR name LIKE ?"
            params = [f'%{search}%', f'%{search}%']

        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM users {where_clause}"
        count_result = db.execute_one(count_query, params)
        total = count_result['count'] if count_result else 0

        # Get users
        query = f"""
            SELECT
                u.id, u.google_id, u.email, u.name, u.picture_url,
                u.entrant_id, u.role, u.is_approved, u.is_active,
                u.created_at, u.last_login,
                le.name as entrant_name
            FROM users u
            LEFT JOIN lateral_entrants le ON u.entrant_id = le.id
            {where_clause}
            ORDER BY u.created_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        users = db.execute(query, params)

        return jsonify({
            'success': True,
            'users': [row_to_dict(u) for u in users],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['PATCH'])
@require_admin
def update_user(user_id):
    """Update user account"""
    try:
        data = request.get_json()

        # Build update query dynamically
        allowed_fields = ['role', 'is_active', 'entrant_id']
        updates = []
        values = []

        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = ?")
                values.append(data[field])

        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

        db.execute(query, values)

        # If user is deactivated, revoke all sessions
        if 'is_active' in data and not data['is_active']:
            session_manager.revoke_all_sessions(user_id)

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'update_user',
            'user',
            user_id,
            None,
            str(data),
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'User updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Delete user account"""
    try:
        # Check if user exists
        user = db.execute_one("SELECT * FROM users WHERE id = ?", (user_id,))
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Revoke all sessions
        session_manager.revoke_all_sessions(user_id)

        # Delete user
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'delete_user',
            'user',
            user_id,
            str(row_to_dict(user)),
            'deleted',
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Content Moderation
# ============================================================================

@admin_bp.route('/moderation/field-edits', methods=['GET'])
@require_admin
def get_field_edit_requests():
    """Get all pending field edit requests"""
    try:
        status = request.args.get('status', 'pending')

        requests_data = db.execute("""
            SELECT
                fer.*,
                u.name as user_name,
                u.email as user_email,
                le.name as entrant_name
            FROM field_edit_requests fer
            JOIN users u ON fer.user_id = u.id
            LEFT JOIN lateral_entrants le ON fer.entrant_id = le.id
            WHERE fer.status = ?
            ORDER BY fer.created_at DESC
        """, (status,))

        return jsonify({
            'success': True,
            'requests': [row_to_dict(r) for r in requests_data]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/field-edits/<int:request_id>/approve', methods=['POST'])
@require_admin
def approve_field_edit(request_id):
    """Approve a field edit request"""
    try:
        # Get request
        edit_request = db.execute_one("""
            SELECT * FROM field_edit_requests WHERE id = ?
        """, (request_id,))

        if not edit_request:
            return jsonify({'error': 'Request not found'}), 404

        req_dict = row_to_dict(edit_request)

        # Apply the change to lateral_entrants table
        db.execute(f"""
            UPDATE lateral_entrants
            SET {req_dict['field_name']} = ?
            WHERE id = ?
        """, (req_dict['new_value'], req_dict['entrant_id']))

        # Update request status
        db.execute("""
            UPDATE field_edit_requests
            SET status = ?, reviewed_by = ?, reviewed_at = ?
            WHERE id = ?
        """, ('approved', request.current_user['user_id'], datetime.now(), request_id))

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'approve_edit',
            'field_edit_request',
            request_id,
            req_dict['old_value'],
            req_dict['new_value'],
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'Edit approved and applied'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/field-edits/<int:request_id>/reject', methods=['POST'])
@require_admin
def reject_field_edit(request_id):
    """Reject a field edit request"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'No reason provided')

        # Update request status
        db.execute("""
            UPDATE field_edit_requests
            SET status = ?, reviewed_by = ?, reviewed_at = ?, rejection_reason = ?
            WHERE id = ?
        """, ('rejected', request.current_user['user_id'], datetime.now(), reason, request_id))

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'reject_edit',
            'field_edit_request',
            request_id,
            'pending',
            f'rejected: {reason}',
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'Edit rejected'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/uploads', methods=['GET'])
@require_admin
def get_pending_uploads():
    """Get pending file uploads for moderation"""
    try:
        status = request.args.get('status', 'pending')

        uploads = db.execute("""
            SELECT
                u.*,
                usr.name as user_name,
                usr.email as user_email
            FROM uploads u
            JOIN users usr ON u.user_id = usr.id
            WHERE u.moderation_status = ?
            ORDER BY u.uploaded_at DESC
        """, (status,))

        return jsonify({
            'success': True,
            'uploads': [row_to_dict(u) for u in uploads]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/uploads/<int:upload_id>/approve', methods=['POST'])
@require_admin
def approve_upload(upload_id):
    """Approve an upload"""
    try:
        db.execute("""
            UPDATE uploads
            SET moderation_status = ?, moderated_by = ?, moderated_at = ?
            WHERE id = ?
        """, ('approved', request.current_user['user_id'], datetime.now(), upload_id))

        return jsonify({
            'success': True,
            'message': 'Upload approved'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/uploads/<int:upload_id>/reject', methods=['POST'])
@require_admin
def reject_upload(upload_id):
    """Reject an upload"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'No reason provided')

        db.execute("""
            UPDATE uploads
            SET moderation_status = ?, moderated_by = ?, moderated_at = ?, rejection_reason = ?
            WHERE id = ?
        """, ('rejected', request.current_user['user_id'], datetime.now(), reason, upload_id))

        return jsonify({
            'success': True,
            'message': 'Upload rejected'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/flagged-content', methods=['GET'])
@require_admin
def get_flagged_content():
    """Get flagged content reports"""
    try:
        status = request.args.get('status', 'pending')

        flagged = db.execute("""
            SELECT
                fc.*,
                u.name as reporter_name,
                u.email as reporter_email
            FROM flagged_content fc
            JOIN users u ON fc.reported_by = u.id
            WHERE fc.status = ?
            ORDER BY fc.reported_at DESC
        """, (status,))

        return jsonify({
            'success': True,
            'flagged': [row_to_dict(f) for f in flagged]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/moderation/flagged-content/<int:flag_id>/resolve', methods=['POST'])
@require_admin
def resolve_flagged_content(flag_id):
    """Resolve a flagged content report"""
    try:
        data = request.get_json()
        action = data.get('action')  # 'remove' or 'keep'
        notes = data.get('notes', '')

        if action not in ['remove', 'keep']:
            return jsonify({'error': 'Invalid action'}), 400

        # Update flagged content status
        db.execute("""
            UPDATE flagged_content
            SET status = ?, resolved_by = ?, resolved_at = ?, admin_notes = ?
            WHERE id = ?
        """, ('resolved', request.current_user['user_id'], datetime.now(), notes, flag_id))

        # If action is remove, delete the content
        if action == 'remove':
            flag = db.execute_one("SELECT * FROM flagged_content WHERE id = ?", (flag_id,))
            if flag:
                flag_dict = row_to_dict(flag)
                # Delete based on content type
                if flag_dict['content_type'] == 'profile_field':
                    # Clear the field
                    db.execute(f"""
                        UPDATE lateral_entrants
                        SET {flag_dict['content_id']} = NULL
                        WHERE id = {flag_dict['entrant_id']}
                    """)
                elif flag_dict['content_type'] == 'upload':
                    db.execute("DELETE FROM uploads WHERE id = ?", (flag_dict['content_id'],))

        return jsonify({
            'success': True,
            'message': 'Flagged content resolved'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Settings Management
# ============================================================================

@admin_bp.route('/settings', methods=['GET'])
@require_admin
def get_settings():
    """Get all admin settings"""
    try:
        settings = db.execute("SELECT * FROM admin_settings ORDER BY setting_key")

        return jsonify({
            'success': True,
            'settings': [row_to_dict(s) for s in settings]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/settings/<setting_key>', methods=['PATCH'])
@require_admin
def update_setting(setting_key):
    """Update a single setting"""
    try:
        data = request.get_json()
        new_value = data.get('value')

        if new_value is None:
            return jsonify({'error': 'Value is required'}), 400

        # Get old value for audit log
        old_setting = db.execute_one("""
            SELECT setting_value FROM admin_settings WHERE setting_key = ?
        """, (setting_key,))

        # Update setting
        db.execute("""
            UPDATE admin_settings
            SET setting_value = ?, updated_at = ?, updated_by = ?
            WHERE setting_key = ?
        """, (new_value, datetime.now(), request.current_user['user_id'], setting_key))

        # Log audit trail
        db.insert("""
            INSERT INTO audit_log (
                user_id, action, entity_type, entity_id,
                old_value, new_value, ip_address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.current_user['user_id'],
            'update_setting',
            'admin_setting',
            setting_key,
            old_setting['setting_value'] if old_setting else None,
            new_value,
            request.remote_addr
        ))

        return jsonify({
            'success': True,
            'message': 'Setting updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Statistics & Analytics
# ============================================================================

@admin_bp.route('/stats/dashboard', methods=['GET'])
@require_admin
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Pending approvals
        pending_count = db.execute_one("""
            SELECT COUNT(*) as count FROM pending_users
        """)['count']

        # Total users
        total_users = db.execute_one("""
            SELECT COUNT(*) as count FROM users WHERE is_active = 1
        """)['count']

        # Pending edits
        pending_edits = db.execute_one("""
            SELECT COUNT(*) as count FROM field_edit_requests WHERE status = 'pending'
        """)['count']

        # Pending uploads
        pending_uploads = db.execute_one("""
            SELECT COUNT(*) as count FROM uploads WHERE moderation_status = 'pending'
        """)['count']

        # Flagged content
        flagged_count = db.execute_one("""
            SELECT COUNT(*) as count FROM flagged_content WHERE status = 'pending'
        """)['count']

        # Recent activity (last 7 days)
        recent_logins = db.execute_one("""
            SELECT COUNT(DISTINCT user_id) as count
            FROM sessions
            WHERE created_at >= datetime('now', '-7 days')
        """)['count']

        return jsonify({
            'success': True,
            'stats': {
                'pending_approvals': pending_count,
                'total_users': total_users,
                'pending_edits': pending_edits,
                'pending_uploads': pending_uploads,
                'flagged_content': flagged_count,
                'recent_logins': recent_logins
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/audit-log', methods=['GET'])
@require_admin
def get_audit_log():
    """Get audit log entries"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        action_filter = request.args.get('action', '')

        offset = (page - 1) * per_page

        # Build query
        where_clause = ""
        params = []

        if action_filter:
            where_clause = "WHERE a.action = ?"
            params = [action_filter]

        # Get logs
        query = f"""
            SELECT
                a.*,
                u.name as user_name,
                u.email as user_email
            FROM audit_log a
            JOIN users u ON a.user_id = u.id
            {where_clause}
            ORDER BY a.created_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        logs = db.execute(query, params)

        return jsonify({
            'success': True,
            'logs': [row_to_dict(log) for log in logs]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
