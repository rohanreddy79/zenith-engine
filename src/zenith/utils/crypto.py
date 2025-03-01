"""Cryptographic hashing and signature helpers."""

import hashlib
import os


def generate_secure_token(length: int = 32) -> str:
    return os.urandom(length).hex()


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
