"""
DevTools Desktop — JSON Tool Logic

JSON formatting, minification, and validation.
"""

import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class JsonResult:
    """Result of a JSON operation."""
    success: bool
    output: str = ""
    error_message: str = ""
    error_detail: str = ""
    line: Optional[int] = None
    column: Optional[int] = None


def format_json(text: str, indent: int = 2) -> JsonResult:
    """Format JSON with indentation."""
    if not text.strip():
        return JsonResult(False, error_message="No input provided",
                          error_detail="Please enter JSON to format.")
    try:
        parsed = json.loads(text)
        formatted = json.dumps(parsed, indent=indent, ensure_ascii=False, sort_keys=False)
        return JsonResult(True, output=formatted)
    except json.JSONDecodeError as e:
        return JsonResult(
            False,
            error_message=f"Invalid JSON at line {e.lineno}, column {e.colno}",
            error_detail=str(e),
            line=e.lineno,
            column=e.colno,
        )


def minify_json(text: str) -> JsonResult:
    """Minify JSON by removing whitespace."""
    if not text.strip():
        return JsonResult(False, error_message="No input provided",
                          error_detail="Please enter JSON to minify.")
    try:
        parsed = json.loads(text)
        minified = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
        return JsonResult(True, output=minified)
    except json.JSONDecodeError as e:
        return JsonResult(
            False,
            error_message=f"Invalid JSON at line {e.lineno}, column {e.colno}",
            error_detail=str(e),
            line=e.lineno,
            column=e.colno,
        )


def validate_json(text: str) -> JsonResult:
    """Validate JSON and return a descriptive result."""
    if not text.strip():
        return JsonResult(False, error_message="No input provided",
                          error_detail="Please enter JSON to validate.")
    try:
        parsed = json.loads(text)
        # Gather stats
        json_type = type(parsed).__name__
        if isinstance(parsed, dict):
            desc = f"Valid JSON object with {len(parsed)} key(s)"
        elif isinstance(parsed, list):
            desc = f"Valid JSON array with {len(parsed)} element(s)"
        else:
            desc = f"Valid JSON {json_type}: {repr(parsed)}"
        size = len(text.encode("utf-8"))
        desc += f"\nSize: {size:,} bytes"
        return JsonResult(True, output=desc)
    except json.JSONDecodeError as e:
        return JsonResult(
            False,
            error_message=f"Invalid JSON at line {e.lineno}, column {e.colno}",
            error_detail=str(e),
            line=e.lineno,
            column=e.colno,
        )
