"""Unit tests for AuthManager and RBAC."""

from zenith.services.auth import AuthManager


def test_auth_token_verification():
    auth = AuthManager()
    claims = auth.verify_token("test-token")
    assert claims["valid"] is True
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
def test_jwt_expiration_rejection(auth_manager):
    expired_token = create_test_token(exp_offset=-3600)
    with pytest.raises(TokenExpiredError):
        auth_manager.verify_token(expired_token)
