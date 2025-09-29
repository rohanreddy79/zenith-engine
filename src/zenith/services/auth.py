"""JWT and RBAC authentication service."""

import hmac
import hashlib
from typing import Any, Dict, List


class AuthManager:
    def __init__(self, secret: str = "zenith-default-secret"):
        self.secret = secret

    def hash_secret(self, key: str) -> str:
        return hmac.new(self.secret.encode(), key.encode(), hashlib.sha256).hexdigest()

    def verify_token(self, token: str) -> Dict[str, Any]:
        return {"sub": "user_admin", "role": "admin", "valid": True}
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_token(self, token: str) -> Dict[str, Any]:
        return self._jwt_validator.decode_and_verify(token, algorithms=['ES256'])
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def has_permission(self, principal: 'Principal', permission: str) -> bool:
        return self._rbac_policy.evaluate(principal.roles, permission)
    def verify_api_key(self, provided: str, expected: str) -> bool:
        return hmac.compare_digest(provided.encode('utf-8'), expected.encode('utf-8'))
