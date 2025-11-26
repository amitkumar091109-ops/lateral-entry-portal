"""
Profile Routes
API endpoints for viewing and editing profiles with visibility controls
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from ..database import db, row_to_dict
from ..auth.decorators import require_auth, require_own_profile, optional_auth
from ..config import get_config

config = get_config()

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profiles')


# ============================================================================
# Visibility Helper Functions
# ============================================================================

def get_field_visibility(entrant_id: int) -> dict:
    """Get visibility settings for all fields of an entrant"""
    settings = db.execute("""
        SELECT field_name, visibility_level
        FROM field_visibility_settings
        WHERE entrant_id = ?
    """, (entrant_id,))

    return {row['field_name']: row['visibility_level'] for row in settings}


def can_view_field(field_name: str, visibility_level: str, viewer_role: str = None, is_same_user: bool = False) -> bool:
    """
    Check if a field can be viewed based on visibility settings

    Args:
        field_name: Name of the field
        visibility_level: public, lateral_entrants_only, or private
        viewer_role: Role of the viewer (None for unauthenticated)
        is_same_user: Whether the viewer is viewing their own profile

    Returns:
        True if field can be viewed
    """
    # Owner can always see their own fields
    if is_same_user:
        return True

    # Admins can see everything
    if viewer_role == 'admin':
        return True

    # Public fields are visible to everyone
    if visibility_level == 'public':
        return True

    # Lateral entrants only fields
    if visibility_level == 'lateral_entrants_only':
        return viewer_role == 'appointee'

    # Private fields only visible to owner and admin
    return False


def filter_profile_fields(profile: dict, viewer_user: dict = None, is_own_profile: bool = False) -> dict:
    """
    Filter profile fields based on visibility settings

    Args:
        profile: Profile data dictionary
        viewer_user: Viewing user dictionary (None if not authenticated)
        is_own_profile: Whether viewing own profile

    Returns:
        Filtered profile dictionary
    """
    if not profile:
        return None

    entrant_id = profile['id']
    viewer_role = viewer_user['role'] if viewer_user else None

    # Get visibility settings
    visibility_settings = get_field_visibility(entrant_id)

    # Filter fields
    filtered = {}

    # Always include these basic fields
    always_visible = ['id', 'name', 'photo_url']
    for field in always_visible:
        if field in profile:
            filtered[field] = profile[field]

    # Filter other fields based on visibility
    for field_name, value in profile.items():
        if field_name in always_visible:
            continue

        visibility_level = visibility_settings.get(field_name, 'public')

        if can_view_field(field_name, visibility_level, viewer_role, is_own_profile):
            filtered[field_name] = value
        else:
            # Field is hidden
            filtered[field_name] = None

    return filtered


# ============================================================================
# Profile Viewing
# ============================================================================

@profile_bp.route('', methods=['GET'])
@optional_auth
def get_all_profiles():
    """Get all profiles (filtered by visibility)"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search = request.args.get('search', '')

        offset = (page - 1) * per_page
        viewer_user = getattr(request, 'current_user', None)

        # Build query
        where_clause = "WHERE 1=1"
        params = []

        if search:
            where_clause += " AND name LIKE ?"
            params.append(f'%{search}%')

        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM lateral_entrants {where_clause}"
        count_result = db.execute_one(count_query, params)
        total = count_result['count'] if count_result else 0

        # Get profiles
        query = f"""
            SELECT * FROM lateral_entrants
            {where_clause}
            ORDER BY name
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        profiles = db.execute(query, params)

        # Filter based on visibility
        filtered_profiles = []
        for profile in profiles:
            profile_dict = row_to_dict(profile)
            filtered = filter_profile_fields(profile_dict, viewer_user, False)
            filtered_profiles.append(filtered)

        return jsonify({
            'success': True,
            'profiles': filtered_profiles,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/<int:entrant_id>', methods=['GET'])
@optional_auth
def get_profile(entrant_id):
    """Get single profile (filtered by visibility)"""
    try:
        viewer_user = getattr(request, 'current_user', None)

        # Check if viewing own profile
        is_own_profile = False
        if viewer_user and viewer_user.get('entrant_id') == entrant_id:
            is_own_profile = True

        # Get profile
        profile = db.execute_one("""
            SELECT * FROM lateral_entrants WHERE id = ?
        """, (entrant_id,))

        if not profile:
            return jsonify({'error': 'Profile not found'}), 404

        profile_dict = row_to_dict(profile)

        # Filter based on visibility
        filtered = filter_profile_fields(profile_dict, viewer_user, is_own_profile)

        return jsonify({
            'success': True,
            'profile': filtered,
            'is_own_profile': is_own_profile
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Visibility Settings Management
# ============================================================================

@profile_bp.route('/<int:entrant_id>/visibility', methods=['GET'])
@require_auth
def get_visibility_settings(entrant_id):
    """Get visibility settings for a profile"""
    try:
        # Only owner or admin can view visibility settings
        if request.current_user['entrant_id'] != entrant_id and request.current_user['role'] != 'admin':
            return jsonify({'error': 'Forbidden'}), 403

        settings = db.execute("""
            SELECT field_name, visibility_level
            FROM field_visibility_settings
            WHERE entrant_id = ?
            ORDER BY field_name
        """, (entrant_id,))

        return jsonify({
            'success': True,
            'settings': [row_to_dict(s) for s in settings]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/<int:entrant_id>/visibility/<field_name>', methods=['PATCH'])
@require_auth
def update_field_visibility(entrant_id, field_name):
    """Update visibility for a single field"""
    try:
        # Only owner can update visibility settings
        if request.current_user['entrant_id'] != entrant_id:
            return jsonify({'error': 'Can only update your own visibility settings'}), 403

        data = request.get_json()
        new_visibility = data.get('visibility_level')

        if new_visibility not in ['public', 'lateral_entrants_only', 'private']:
            return jsonify({'error': 'Invalid visibility level'}), 400

        # Get old value for audit
        old_setting = db.execute_one("""
            SELECT visibility_level
            FROM field_visibility_settings
            WHERE entrant_id = ? AND field_name = ?
        """, (entrant_id, field_name))

        # Update or insert
        if old_setting:
            db.execute("""
                UPDATE field_visibility_settings
                SET visibility_level = ?
                WHERE entrant_id = ? AND field_name = ?
            """, (new_visibility, entrant_id, field_name))
        else:
            db.insert("""
                INSERT INTO field_visibility_settings (entrant_id, field_name, visibility_level)
                VALUES (?, ?, ?)
            """, (entrant_id, field_name, new_visibility))

        # Log to visibility audit
        db.insert("""
            INSERT INTO visibility_audit (
                entrant_id, field_name, old_visibility, new_visibility, changed_by
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            entrant_id,
            field_name,
            old_setting['visibility_level'] if old_setting else 'public',
            new_visibility,
            request.current_user['user_id']
        ))

        return jsonify({
            'success': True,
            'message': 'Visibility updated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/<int:entrant_id>/visibility/bulk', methods=['PATCH'])
@require_auth
def bulk_update_visibility(entrant_id):
    """Bulk update visibility settings"""
    try:
        # Only owner can update visibility settings
        if request.current_user['entrant_id'] != entrant_id:
            return jsonify({'error': 'Can only update your own visibility settings'}), 403

        data = request.get_json()
        updates = data.get('updates', [])  # List of {field_name, visibility_level}

        if not updates:
            return jsonify({'error': 'No updates provided'}), 400

        # Validate all updates first
        for update in updates:
            if update.get('visibility_level') not in ['public', 'lateral_entrants_only', 'private']:
                return jsonify({'error': f'Invalid visibility level for {update.get("field_name")}'}), 400

        # Apply updates
        for update in updates:
            field_name = update['field_name']
            new_visibility = update['visibility_level']

            # Get old value
            old_setting = db.execute_one("""
                SELECT visibility_level
                FROM field_visibility_settings
                WHERE entrant_id = ? AND field_name = ?
            """, (entrant_id, field_name))

            # Update or insert
            if old_setting:
                db.execute("""
                    UPDATE field_visibility_settings
                    SET visibility_level = ?
                    WHERE entrant_id = ? AND field_name = ?
                """, (new_visibility, entrant_id, field_name))
            else:
                db.insert("""
                    INSERT INTO field_visibility_settings (entrant_id, field_name, visibility_level)
                    VALUES (?, ?, ?)
                """, (entrant_id, field_name, new_visibility))

            # Log to audit
            db.insert("""
                INSERT INTO visibility_audit (
                    entrant_id, field_name, old_visibility, new_visibility, changed_by
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                entrant_id,
                field_name,
                old_setting['visibility_level'] if old_setting else 'public',
                new_visibility,
                request.current_user['user_id']
            ))

        return jsonify({
            'success': True,
            'message': f'Updated {len(updates)} fields'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Profile Editing (with moderation)
# ============================================================================

@profile_bp.route('/<int:entrant_id>/fields/<field_name>', methods=['PATCH'])
@require_auth
def update_profile_field(entrant_id, field_name):
    """Submit field edit request (goes to moderation queue)"""
    try:
        # Only owner can edit their profile
        if request.current_user['entrant_id'] != entrant_id:
            return jsonify({'error': 'Can only edit your own profile'}), 403

        data = request.get_json()
        new_value = data.get('value')

        if new_value is None:
            return jsonify({'error': 'Value is required'}), 400

        # Get old value
        old_profile = db.execute_one(f"""
            SELECT {field_name} FROM lateral_entrants WHERE id = ?
        """, (entrant_id,))

        old_value = old_profile[field_name] if old_profile else None

        # Check if moderation is enabled for this field
        moderation_enabled = db.execute_one("""
            SELECT setting_value FROM admin_settings WHERE setting_key = 'moderation_enabled'
        """)

        if moderation_enabled and moderation_enabled['setting_value'] == 'true':
            # Submit to moderation queue
            db.insert("""
                INSERT INTO field_edit_requests (
                    user_id, entrant_id, field_name, old_value, new_value, status
                )
                VALUES (?, ?, ?, ?, ?, 'pending')
            """, (
                request.current_user['user_id'],
                entrant_id,
                field_name,
                old_value,
                new_value
            ))

            return jsonify({
                'success': True,
                'message': 'Edit request submitted for review',
                'requires_approval': True
            })
        else:
            # Apply immediately
            db.execute(f"""
                UPDATE lateral_entrants
                SET {field_name} = ?
                WHERE id = ?
            """, (new_value, entrant_id))

            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'requires_approval': False
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# User's Own Profile
# ============================================================================

@profile_bp.route('/me', methods=['GET'])
@require_auth
def get_my_profile():
    """Get current user's own profile (no filtering)"""
    try:
        entrant_id = request.current_user.get('entrant_id')

        if not entrant_id:
            return jsonify({'error': 'No profile associated with this account'}), 404

        profile = db.execute_one("""
            SELECT * FROM lateral_entrants WHERE id = ?
        """, (entrant_id,))

        if not profile:
            return jsonify({'error': 'Profile not found'}), 404

        return jsonify({
            'success': True,
            'profile': row_to_dict(profile)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profile_bp.route('/me/edit-requests', methods=['GET'])
@require_auth
def get_my_edit_requests():
    """Get current user's pending edit requests"""
    try:
        requests = db.execute("""
            SELECT * FROM field_edit_requests
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'requests': [row_to_dict(r) for r in requests]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
