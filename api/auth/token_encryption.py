"""
Token Encryption Utilities
Encrypts and decrypts OAuth tokens before storing in database
"""

from cryptography.fernet import Fernet
from ..config import get_config

config = get_config()


def get_encryption_key() -> bytes:
    """
    Get or generate encryption key for tokens

    Returns:
        Fernet encryption key as bytes
    """
    key = config.TOKEN_ENCRYPTION_KEY

    if not key:
        raise ValueError(
            "TOKEN_ENCRYPTION_KEY not set in environment. "
            "Generate one with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )

    # Convert string to bytes if needed
    if isinstance(key, str):
        key = key.encode()

    return key


def encrypt_token(token: str) -> str:
    """
    Encrypt OAuth token before storing in database

    Args:
        token: Plain text token

    Returns:
        Encrypted token as string
    """
    if not token:
        return None

    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(token.encode())
    return encrypted.decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypt OAuth token when retrieving from database

    Args:
        encrypted_token: Encrypted token string

    Returns:
        Decrypted plain text token
    """
    if not encrypted_token:
        return None

    f = Fernet(get_encryption_key())
    decrypted = f.decrypt(encrypted_token.encode())
    return decrypted.decode()
