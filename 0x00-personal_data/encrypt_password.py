#!/usr/bin/env python3
import bcrypt

def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the hashed password as a byte string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
