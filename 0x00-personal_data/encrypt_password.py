#!/usr/bin/env python3
import bcrypt

def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the hashed password as a byte string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)