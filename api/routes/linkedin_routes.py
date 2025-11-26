"""
LinkedIn Integration Routes
API endpoints for LinkedIn OAuth and profile syncing
"""

from flask import Blueprint, request, jsonify, redirect, session
from datetime import datetime
import secrets
import httpx

from ..database import db, row_to_dict
from ..auth.decorators import require_auth
from ..auth.token_encryption import encrypt_token, decrypt_token
from ..config import get_config

config = get_config()

linkedin_bp = Blueprint('linkedin', __name__, url_prefix='/api/linkedin')


class LinkedInOAuthService:
    """Handle LinkedIn OAuth flow"""

    def __init__(self):
        self.client_id = config.LINKEDIN_CLIENT_ID
        self.client_secret = config.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = f"{config.BASE_URL}/api/linkedin/callback"
        self.scope = 'r_liteprofile r_emailaddress'

    def get_authorization_url(self, state: str) -> str:
        """Generate LinkedIn authorization URL"""
        return (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&state={state}"
            f"&scope={self.scope}"
        )

    async def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.linkedin.com/oauth/v2/accessToken",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )

            if response.status_code != 200:
                raise Exception("Failed to exchange code for token")

            return response.json()

    async def get_profile_data(self, access_token: str) -> dict:
        """Fetch LinkedIn profile data"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            # Get basic profile
            profile_response = await client.get(
                "https://api.linkedin.com/v2/me",
                headers=headers
            )

            if profile_response.status_code != 200:
                raise Exception("Failed to fetch profile data")

            profile = profile_response.json()

            # Get email
            email_response = await client.get(
                "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
                headers=headers
            )

            email_data = email_response.json() if email_response.status_code == 200 else {}

            return {
                'profile': profile,
                'email': email_data
            }


linkedin_oauth_service = LinkedInOAuthService()


@linkedin_bp.route('/connect', methods=['GET'])
@require_auth
def linkedin_connect():
    """Initiate LinkedIn OAuth flow"""
    try:
        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        session['linkedin_oauth_state'] = state

        # Get authorization URL
        auth_url = linkedin_oauth_service.get_authorization_url(state)

        return redirect(auth_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@linkedin_bp.route('/callback', methods=['GET'])
@require_auth
async def linkedin_callback():
    """Handle LinkedIn OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')

        if error:
            return redirect(f'/pages/profile-settings.html?error=linkedin_{error}')

        # Verify state
        if not state or state != session.get('linkedin_oauth_state'):
            return redirect('/pages/profile-settings.html?error=linkedin_csrf')

        # Exchange code for token
        tokens = await linkedin_oauth_service.exchange_code_for_token(code)

        # Get profile data
        linkedin_data = await linkedin_oauth_service.get_profile_data(tokens['access_token'])

        # Store connection
        linkedin_id = linkedin_data['profile'].get('id')

        # Check if already connected
        existing = db.execute_one("""
            SELECT id FROM linkedin_connections
            WHERE user_id = ?
        """, (request.current_user['user_id'],))

        if existing:
            # Update
            db.execute("""
                UPDATE linkedin_connections
                SET linkedin_id = ?, access_token = ?, profile_data = ?, connected_at = ?
                WHERE user_id = ?
            """, (
                linkedin_id,
                encrypt_token(tokens['access_token']),
                str(linkedin_data),
                datetime.now(),
                request.current_user['user_id']
            ))
        else:
            # Insert
            db.insert("""
                INSERT INTO linkedin_connections (
                    user_id, linkedin_id, access_token, profile_data
                )
                VALUES (?, ?, ?, ?)
            """, (
                request.current_user['user_id'],
                linkedin_id,
                encrypt_token(tokens['access_token']),
                str(linkedin_data)
            ))

        return redirect('/pages/profile-settings.html?success=linkedin_connected')
    except Exception as e:
        return redirect(f'/pages/profile-settings.html?error=linkedin_{str(e)}')


@linkedin_bp.route('/disconnect', methods=['POST'])
@require_auth
def linkedin_disconnect():
    """Disconnect LinkedIn account"""
    try:
        db.execute("""
            DELETE FROM linkedin_connections WHERE user_id = ?
        """, (request.current_user['user_id'],))

        return jsonify({
            'success': True,
            'message': 'LinkedIn disconnected successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@linkedin_bp.route('/sync', methods=['POST'])
@require_auth
async def sync_from_linkedin():
    """Sync profile data from LinkedIn"""
    try:
        # Get connection
        connection = db.execute_one("""
            SELECT * FROM linkedin_connections WHERE user_id = ?
        """, (request.current_user['user_id'],))

        if not connection:
            return jsonify({'error': 'LinkedIn not connected'}), 400

        conn_dict = row_to_dict(connection)

        # Get fresh profile data
        access_token = decrypt_token(conn_dict['access_token'])
        linkedin_data = await linkedin_oauth_service.get_profile_data(access_token)

        # Map LinkedIn fields to our schema
        profile_updates = {}

        # Example mapping (adjust based on actual LinkedIn API response)
        if 'firstName' in linkedin_data['profile']:
            profile_updates['first_name'] = linkedin_data['profile']['firstName'].get('localized', {}).get('en_US', '')

        if 'lastName' in linkedin_data['profile']:
            profile_updates['last_name'] = linkedin_data['profile']['lastName'].get('localized', {}).get('en_US', '')

        # Create field edit requests for moderation
        entrant_id = request.current_user['entrant_id']

        for field_name, new_value in profile_updates.items():
            # Get old value
            old_profile = db.execute_one(f"""
                SELECT {field_name} FROM lateral_entrants WHERE id = ?
            """, (entrant_id,))

            old_value = old_profile[field_name] if old_profile else None

            # Submit edit request
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

        # Update sync history
        db.insert("""
            INSERT INTO linkedin_sync_history (
                user_id, sync_type, fields_synced, status
            )
            VALUES (?, 'manual', ?, 'success')
        """, (
            request.current_user['user_id'],
            len(profile_updates)
        ))

        return jsonify({
            'success': True,
            'message': f'Synced {len(profile_updates)} fields (pending moderation)',
            'fields_synced': len(profile_updates)
        })
    except Exception as e:
        # Log failed sync
        db.insert("""
            INSERT INTO linkedin_sync_history (
                user_id, sync_type, status, error_message
            )
            VALUES (?, 'manual', 'failed', ?)
        """, (
            request.current_user['user_id'],
            str(e)
        ))

        return jsonify({'error': str(e)}), 500


@linkedin_bp.route('/status', methods=['GET'])
@require_auth
def get_linkedin_status():
    """Check if LinkedIn is connected"""
    try:
        connection = db.execute_one("""
            SELECT linkedin_id, connected_at FROM linkedin_connections
            WHERE user_id = ?
        """, (request.current_user['user_id'],))

        if connection:
            return jsonify({
                'success': True,
                'connected': True,
                'linkedin_id': connection['linkedin_id'],
                'connected_at': connection['connected_at']
            })
        else:
            return jsonify({
                'success': True,
                'connected': False
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
