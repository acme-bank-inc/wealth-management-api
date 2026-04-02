"""Auth0 JWT authentication middleware for the Wealth Management API.

Validates access tokens using Auth0 JWKS (JSON Web Key Sets).
Requires AUTH0_DOMAIN and AUTH0_AUDIENCE environment variables.
"""

import os
from functools import wraps
from urllib.request import urlopen
import json

from authlib.jose import JsonWebToken, JsonWebKey
from authlib.jose.errors import JoseError
from flask import request, jsonify


class Auth0Error(Exception):
    """Represents an Auth0 authentication error."""

    def __init__(self, message, status_code=401):
        self.message = message
        self.status_code = status_code


def get_jwks(domain):
    """Fetch the JWKS from the Auth0 domain."""
    jwks_url = f"https://{domain}/.well-known/jwks.json"
    with urlopen(jwks_url) as response:
        return json.loads(response.read())


def get_token_from_header():
    """Extract the Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise Auth0Error("Authorization header is missing")

    parts = auth_header.split()

    if parts[0].lower() != "bearer":
        raise Auth0Error("Authorization header must start with Bearer")

    if len(parts) == 1:
        raise Auth0Error("Token not found in Authorization header")

    if len(parts) > 2:
        raise Auth0Error("Authorization header must be a Bearer token")

    return parts[1]


def requires_auth(f):
    """Decorator that validates Auth0 JWT tokens on protected routes."""

    @wraps(f)
    def decorated(*args, **kwargs):
        domain = os.environ.get("AUTH0_DOMAIN")
        audience = os.environ.get("AUTH0_AUDIENCE")

        if not domain or not audience:
            return jsonify({"error": "Auth0 configuration is incomplete"}), 500

        try:
            token = get_token_from_header()
        except Auth0Error as e:
            return jsonify({"error": e.message}), e.status_code

        try:
            jwks_data = get_jwks(domain)
            jwt = JsonWebToken(["RS256"])
            claims = jwt.decode(
                token,
                JsonWebKey.import_key_set(jwks_data),
                claims_options={
                    "iss": {"essential": True, "value": f"https://{domain}/"},
                    "aud": {"essential": True, "value": audience},
                },
            )
            claims.validate()
        except JoseError as e:
            return jsonify({"error": f"Token validation failed: {str(e)}"}), 401
        except Exception as e:
            return jsonify({"error": f"Unable to verify token: {str(e)}"}), 401

        return f(*args, **kwargs)

    return decorated
