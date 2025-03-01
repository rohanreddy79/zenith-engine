"""Unit tests for AuthManager and RBAC."""

from zenith.services.auth import AuthManager


def test_auth_token_verification():
    auth = AuthManager()
    claims = auth.verify_token("test-token")
    assert claims["valid"] is True
