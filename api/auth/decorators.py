"""
Authentication Decorators
Decorators for protecting routes and checking permissions
"""

from functools import wraps
from flask import request, jsonify

from .session_manager import session_manager


def require_auth(f):
    """
    Require authentication and approval

    Usage:
        @app.route('/api/profile')
        @require_auth
        def get_profile():
            user = request.current_user
            # ... handle request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get session ID from cookie
        session_id = request.cookies.get('session_id')

        if not session_id:
            return jsonify({'error': 'Authentication required'}), 401

        # Validate session
        session = session_manager.validate_session(session_id)

        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401

        # Check if user is approved
        if not session['is_approved']:
            return jsonify({'error': 'Account pending approval'}), 403

        # Attach user to request object
        request.current_user = session

        return f(*args, **kwargs)

    return decorated_function


def require_admin(f):
    """
    Require admin role

    Usage:
        @app.route('/api/admin/users')
        @require_admin
        def get_users():
            # ... handle request
    """
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        if request.current_user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return f(*args, **kwargs)

    return decorated_function


def require_own_profile(f):
    """
    Require user to be editing their own profile

    Usage:
        @app.route('/api/profile/<int:profile_id>')
        @require_own_profile
        def update_profile(profile_id):
            # ... handle request
    """
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        profile_id = kwargs.get('id') or kwargs.get('profile_id')

        if profile_id is None:
            return jsonify({'error': 'Profile ID required'}), 400

        if str(request.current_user['entrant_id']) != str(profile_id):
            return jsonify({'error': 'Cannot edit other profiles'}), 403

        return f(*args, **kwargs)

    return decorated_function


def optional_auth(f):
    """
    Optional authentication - attaches user if authenticated, but allows unauthenticated access

    Usage:
        @app.route('/api/profile/<int:profile_id>')
        @optional_auth
        def get_profile(profile_id):
            user = request.current_user  # May be None
            # ... handle request
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get session ID from cookie
        session_id = request.cookies.get('session_id')

        if session_id:
            # Try to validate session
            session = session_manager.validate_session(session_id)
            if session and session['is_approved']:
                request.current_user = session
            else:
                request.current_user = None
        else:
            request.current_user = None

        return f(*args, **kwargs)

    return decorated_function
