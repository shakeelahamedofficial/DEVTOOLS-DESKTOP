"""
DevTools Desktop — Base64 Tool Logic
"""

import base64
from dataclasses import dataclass
from typing import Optional


@dataclass
class Base64Result:
    success: bool
    output: str = ""
    output_bytes: Optional[bytes] = None
    error_message: str = ""
    error_detail: str = ""


def encode_text(text: str) -> Base64Result:
    """Encode text to Base64."""
    if not text:
        return Base64Result(False, error_message="No input provided")
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
        return Base64Result(True, output=encoded)
    except Exception as e:
        return Base64Result(False, error_message="Encoding failed",
                           error_detail=str(e))


def decode_text(b64_text: str) -> Base64Result:
    """Decode Base64 to text."""
    if not b64_text.strip():
        return Base64Result(False, error_message="No input provided")
    try:
        decoded = base64.b64decode(b64_text, validate=True).decode("utf-8")
        return Base64Result(True, output=decoded)
    except base64.binascii.Error as e:
        return Base64Result(
            False,
            error_message="Invalid Base64 input",
            error_detail="The provided value contains characters that are not valid Base64."
        )
    except UnicodeDecodeError:
        return Base64Result(
            False,
            error_message="Decoded data is not valid UTF-8 text",
            error_detail="The Base64 decoded successfully but contains binary data, not text."
        )


def encode_file(file_path: str) -> Base64Result:
    """Encode a file to Base64."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode("ascii")
        return Base64Result(True, output=encoded)
    except FileNotFoundError:
        return Base64Result(False, error_message="File not found")
    except Exception as e:
        return Base64Result(False, error_message="Failed to read file",
                           error_detail=str(e))


def decode_to_bytes(b64_text: str) -> Base64Result:
    """Decode Base64 to raw bytes."""
    if not b64_text.strip():
        return Base64Result(False, error_message="No input provided")
    try:
        decoded = base64.b64decode(b64_text, validate=True)
        return Base64Result(True, output_bytes=decoded)
    except base64.binascii.Error:
        return Base64Result(
            False,
            error_message="Invalid Base64 input",
            error_detail="The provided value contains characters that are not valid Base64."
        )
