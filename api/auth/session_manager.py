"""
Session Management
Handles user session creation, validation, and cleanup
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict

from ..database import db, row_to_dict
from ..config import get_config
from .token_encryption import encrypt_token, decrypt_token

config = get_config()


class SessionManager:
    """Manages user authentication sessions"""

    def create_session(
        self,
        user_id: int,
        ip_address: str,
        user_agent: str,
        google_tokens: Dict
    ) -> str:
        """
        Create new session for authenticated user

        Args:
            user_id: User ID
            ip_address: Client IP address
            user_agent: Browser user agent string
            google_tokens: Dictionary with access_token and refresh_token

        Returns:
            Session ID
        """
        # Generate secure session ID
        session_id = secrets.token_urlsafe(32)

        # Calculate expiry (7 days from now)
        expires_at = datetime.now() + timedelta(days=config.SESSION_LIFETIME_DAYS)

        # Encrypt Google tokens before storing
        encrypted_access = encrypt_token(google_tokens.get('access_token'))
        encrypted_refresh = encrypt_token(google_tokens.get('refresh_token'))

        # Insert session into database
        db.execute("""
            INSERT INTO sessions (
                id, user_id, google_access_token, google_refresh_token,
                ip_address, user_agent, expires_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            user_id,
            encrypted_access,
            encrypted_refresh,
            ip_address,
            user_agent,
            expires_at
        ))

        return session_id

    def validate_session(self, session_id: str) -> Optional[Dict]:
        """
        Validate session and return user info if valid

        Args:
            session_id: Session ID to validate

        Returns:
            Dictionary with session and user info, or None if invalid
        """
        if not session_id:
            return None

        # Get session from database with user info
        session = db.execute_one("""
            SELECT
                s.*,
                u.id as user_id,
                u.email,
                u.name,
                u.role,
                u.is_approved,
                u.is_active,
                u.entrant_id,
                u.picture_url
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.id = ? AND s.expires_at > ?
        """, (session_id, datetime.now()))

        if not session:
            return None

        session_dict = row_to_dict(session)

        # Check if user is still approved and active
        if not session_dict['is_approved'] or not session_dict['is_active']:
            # Admin revoked access, delete session
            self.delete_session(session_id)
            return None

        return session_dict

    def refresh_google_token(self, session_id: str):
        """
        Refresh Google access token if expired

        Args:
            session_id: Session ID

        Returns:
            New access token or None
        """
        session = db.execute_one("""
            SELECT google_refresh_token FROM sessions WHERE id = ?
        """, (session_id,))

        if not session:
            return None

        # Decrypt refresh token
        refresh_token = decrypt_token(session['google_refresh_token'])

        if not refresh_token:
            return None

        # Refresh token with Google
        from .google_oauth import google_oauth_service
        new_tokens = google_oauth_service.refresh_access_token(refresh_token)

        # Update session with new access token
        encrypted_access = encrypt_token(new_tokens['access_token'])
        db.execute("""
            UPDATE sessions
            SET google_access_token = ?
            WHERE id = ?
        """, (encrypted_access, session_id))

        return new_tokens

    def delete_session(self, session_id: str):
        """
        Delete session (logout)

        Args:
            session_id: Session ID to delete
        """
        db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    def cleanup_expired_sessions(self):
        """
        Remove expired sessions (run daily via background job)

        Returns:
            Number of sessions deleted
        """
        result = db.execute("""
            DELETE FROM sessions WHERE expires_at < ?
        """, (datetime.now(),))

        return len(result)

    def get_active_sessions(self, user_id: int):
        """
        Get all active sessions for a user

        Args:
            user_id: User ID

        Returns:
            List of active sessions
        """
        sessions = db.execute("""
            SELECT id, ip_address, user_agent, created_at, expires_at
            FROM sessions
            WHERE user_id = ? AND expires_at > ?
            ORDER BY created_at DESC
        """, (user_id, datetime.now()))

        return [row_to_dict(row) for row in sessions]

    def revoke_all_sessions(self, user_id: int):
        """
        Revoke all sessions for a user (force logout everywhere)

        Args:
            user_id: User ID

        Returns:
            Number of sessions revoked
        """
        result = db.execute("""
            DELETE FROM sessions WHERE user_id = ?
        """, (user_id,))

        return len(result)


# Global session manager instance
session_manager = SessionManager()
