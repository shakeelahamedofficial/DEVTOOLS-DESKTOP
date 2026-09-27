"""
DevTools Desktop — JWT Decoder Logic

Decode JWT tokens without verification. Local-only processing.
"""

import base64
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class JwtResult:
    success: bool
    header: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None
    header_raw: str = ""
    payload_raw: str = ""
    error_message: str = ""
    error_detail: str = ""
    algorithm: str = ""
    token_type: str = ""
    expiration: Optional[str] = None
    issued_at: Optional[str] = None
    is_expired: Optional[bool] = None


def _base64url_decode(data: str) -> bytes:
    """Decode Base64URL-encoded data."""
    # Add padding if necessary
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data)


def _format_timestamp(ts: Any) -> Optional[str]:
    """Format a Unix timestamp to human-readable string."""
    try:
        ts_int = int(ts)
        dt = datetime.fromtimestamp(ts_int, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (ValueError, TypeError, OSError):
        return None


def decode_jwt(token: str) -> JwtResult:
    """Decode a JWT token into its components."""
    token = token.strip()
    if not token:
        return JwtResult(False, error_message="No token provided",
                         error_detail="Please enter a JWT token to decode.")

    parts = token.split(".")
    if len(parts) not in (2, 3):
        return JwtResult(
            False,
            error_message="Invalid JWT structure",
            error_detail=f"Expected 2 or 3 parts separated by dots, got {len(parts)}."
        )

    try:
        header_bytes = _base64url_decode(parts[0])
        header = json.loads(header_bytes)
        header_raw = json.dumps(header, indent=2, ensure_ascii=False)
    except Exception as e:
        return JwtResult(
            False,
            error_message="Failed to decode JWT header",
            error_detail=f"The header part is not valid Base64URL-encoded JSON.\n{e}"
        )

    try:
        payload_bytes = _base64url_decode(parts[1])
        payload = json.loads(payload_bytes)
        payload_raw = json.dumps(payload, indent=2, ensure_ascii=False)
    except Exception as e:
        return JwtResult(
            False,
            error_message="Failed to decode JWT payload",
            error_detail=f"The payload part is not valid Base64URL-encoded JSON.\n{e}"
        )

    # Extract common fields
    algorithm = header.get("alg", "Unknown")
    token_type = header.get("typ", "Unknown")

    exp = payload.get("exp")
    iat = payload.get("iat")

    exp_str = _format_timestamp(exp)
    iat_str = _format_timestamp(iat)

    is_expired = None
    if exp is not None:
        try:
            exp_dt = datetime.fromtimestamp(int(exp), tz=timezone.utc)
            is_expired = datetime.now(timezone.utc) > exp_dt
        except (ValueError, TypeError, OSError):
            pass

    return JwtResult(
        success=True,
        header=header,
        payload=payload,
        header_raw=header_raw,
        payload_raw=payload_raw,
        algorithm=algorithm,
        token_type=token_type,
        expiration=exp_str,
        issued_at=iat_str,
        is_expired=is_expired,
    )
