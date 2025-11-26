"""
Authentication Routes
Handles Google OAuth login, logout, and session management
"""

from flask import Blueprint, request, redirect, session, jsonify, url_for, make_response
from datetime import datetime
import secrets

from ..auth import google_oauth_service, session_manager, InvalidTokenError
from ..database import db, row_to_dict

# Create Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/google/login')
def google_login():
    """
    Initiate Google OAuth flow
    GET /api/auth/google/login
    """
    # Generate CSRF token
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    # Generate authorization URL
    auth_url = google_oauth_service.get_authorization_url(state)

    return redirect(auth_url)


@auth_bp.route('/google/callback')
def google_callback():
    """
    Handle Google OAuth callback
    GET /api/auth/google/callback?code=...&state=...
    """
    # Verify state token (CSRF protection)
    state = request.args.get('state')
    if not state or state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400

    # Clear state from session
    session.pop('oauth_state', None)

    # Get authorization code
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No authorization code received'}), 400

    try:
        # Exchange code for tokens
        token_data = google_oauth_service.exchange_code_for_tokens(code, state)
        user_info = token_data['user_info']

        # Check if user exists
        user = db.execute_one("""
            SELECT * FROM users WHERE google_id = ?
        """, (user_info['google_id'],))

        if user:
            user_dict = row_to_dict(user)

            # User exists - check approval status
            if not user_dict['is_approved']:
                # User not yet approved by admin
                return redirect('/pages/pending-approval.html')

            if not user_dict['is_active']:
                # User account deactivated
                return jsonify({'error': 'Account deactivated'}), 403

            # Create session
            session_id = session_manager.create_session(
                user_id=user_dict['id'],
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                google_tokens={
                    'access_token': token_data['access_token'],
                    'refresh_token': token_data['refresh_token']
                }
            )

            # Update last login
            db.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            """, (user_dict['id'],))

            # Log login
            db.execute("""
                INSERT INTO audit_log (user_id, action, entity_type, ip_address, user_agent)
                VALUES (?, 'login', 'session', ?, ?)
            """, (user_dict['id'], request.remote_addr, request.user_agent.string))

            # Set secure cookie and redirect
            response = make_response(redirect('/'))
            response.set_cookie(
                'session_id',
                session_id,
                httponly=True,
                secure=request.is_secure,  # HTTPS only in production
                samesite='Lax',
                max_age=604800  # 7 days
            )

            return response

        else:
            # User doesn't exist - check if already pending
            pending = db.execute_one("""
                SELECT * FROM pending_users WHERE google_id = ?
            """, (user_info['google_id'],))

            if pending:
                # Already requested access
                return redirect('/pages/pending-approval.html')

            # Create pending user request
            db.execute("""
                INSERT INTO pending_users (google_id, email, name, picture_url)
                VALUES (?, ?, ?, ?)
            """, (user_info['google_id'], user_info['email'],
                  user_info['name'], user_info['picture_url']))

            return redirect('/pages/access-requested.html')

    except InvalidTokenError as e:
        return jsonify({'error': f'Invalid token: {str(e)}'}), 400
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return jsonify({'error': 'Authentication failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Log out user and delete session
    POST /api/auth/logout
    """
    session_id = request.cookies.get('session_id')

    if session_id:
        # Get user ID before deleting session
        session_data = session_manager.validate_session(session_id)
        user_id = session_data['user_id'] if session_data else None

        # Delete session
        session_manager.delete_session(session_id)

        # Log logout
        if user_id:
            db.execute("""
                INSERT INTO audit_log (user_id, action, entity_type, ip_address)
                VALUES (?, 'logout', 'session', ?)
            """, (user_id, request.remote_addr))

    # Clear cookie
    response = jsonify({'success': True, 'message': 'Logged out successfully'})
    response.delete_cookie('session_id')

    return response


@auth_bp.route('/me')
def get_current_user():
    """
    Get current authenticated user info
    GET /api/auth/me
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        return jsonify({'authenticated': False}), 401

    session_data = session_manager.validate_session(session_id)

    if not session_data:
        return jsonify({'authenticated': False}), 401

    return jsonify({
        'authenticated': True,
        'user': {
            'id': session_data['user_id'],
            'name': session_data['name'],
            'email': session_data['email'],
            'role': session_data['role'],
            'entrant_id': session_data['entrant_id'],
            'picture_url': session_data['picture_url'],
            'is_approved': session_data['is_approved'],
            'is_active': session_data['is_active']
        }
    })


@auth_bp.route('/status')
def check_status():
    """
    Check approval status for pending users
    GET /api/auth/status?google_id=...
    """
    google_id = request.args.get('google_id')

    if not google_id:
        return jsonify({'error': 'Missing google_id parameter'}), 400

    # Check if user is approved
    user = db.execute_one("""
        SELECT is_approved, is_active FROM users WHERE google_id = ?
    """, (google_id,))

    if user:
        return jsonify({
            'status': 'approved' if user['is_approved'] else 'pending',
            'active': user['is_active']
        })

    # Check if pending
    pending = db.execute_one("""
        SELECT * FROM pending_users WHERE google_id = ?
    """, (google_id,))

    if pending:
        return jsonify({'status': 'pending'})

    return jsonify({'status': 'not_found'})
