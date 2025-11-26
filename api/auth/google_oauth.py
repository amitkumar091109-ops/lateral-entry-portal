"""
Google OAuth Service
Handles Google OAuth 2.0 authentication flow
"""

from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from typing import Dict, Optional
import secrets

from ..config import get_config

config = get_config()


class GoogleOAuthService:
    """Google OAuth authentication service"""

    def __init__(self):
        self.client_id = config.GOOGLE_CLIENT_ID
        self.client_secret = config.GOOGLE_CLIENT_SECRET
        self.redirect_uri = config.GOOGLE_REDIRECT_URI
        self.scopes = config.GOOGLE_SCOPES

        if not self.client_id or not self.client_secret:
            raise ValueError("Google OAuth credentials not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env")

    def get_authorization_url(self, state: str) -> str:
        """
        Generate Google OAuth authorization URL

        Args:
            state: CSRF protection token

        Returns:
            Authorization URL to redirect user to
        """
        flow = self._create_flow()
        flow.redirect_uri = self.redirect_uri

        authorization_url, _ = flow.authorization_url(
            access_type='offline',  # Request refresh token
            include_granted_scopes='true',
            state=state,
            prompt='consent'  # Force consent screen to get refresh token
        )

        return authorization_url

    def exchange_code_for_tokens(self, code: str, state: str) -> Dict:
        """
        Exchange authorization code for access and refresh tokens

        Args:
            code: Authorization code from Google
            state: CSRF protection token

        Returns:
            Dictionary containing tokens and user info
        """
        flow = self._create_flow()
        flow.redirect_uri = self.redirect_uri

        # Fetch tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Get user info from ID token
        user_info = self.get_user_info(credentials.id_token)

        return {
            'access_token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'id_token': credentials.id_token,
            'token_uri': credentials.token_uri,
            'user_info': user_info
        }

    def get_user_info(self, id_token_str: str) -> Dict:
        """
        Extract and verify user info from ID token

        Args:
            id_token_str: JWT ID token from Google

        Returns:
            Dictionary with user information
        """
        try:
            # Verify the token
            id_info = id_token.verify_oauth2_token(
                id_token_str,
                requests.Request(),
                self.client_id
            )

            # Extract user information
            return {
                'google_id': id_info['sub'],
                'email': id_info['email'],
                'name': id_info.get('name', ''),
                'picture_url': id_info.get('picture', ''),
                'email_verified': id_info.get('email_verified', False)
            }
        except ValueError as e:
            raise InvalidTokenError(f"Invalid ID token: {e}")

    def refresh_access_token(self, refresh_token: str) -> Dict:
        """
        Refresh access token using refresh token

        Args:
            refresh_token: OAuth refresh token

        Returns:
            Dictionary with new access token and expiry
        """
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        # Refresh the credentials
        credentials.refresh(Request())

        return {
            'access_token': credentials.token,
            'expires_at': credentials.expiry
        }

    def _create_flow(self) -> Flow:
        """Create OAuth flow instance"""
        client_config = {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [self.redirect_uri]
            }
        }

        return Flow.from_client_config(
            client_config=client_config,
            scopes=self.scopes
        )


class InvalidTokenError(Exception):
    """Raised when token verification fails"""
    pass


# Global service instance
google_oauth_service = GoogleOAuthService() if config.GOOGLE_CLIENT_ID else None
