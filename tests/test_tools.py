"""
DevTools Desktop — Tests
"""

import os
import sys
import pytest

# Ensure app package is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.json_tool.logic import format_json, minify_json, validate_json
from app.tools.jwt_tool.logic import decode_jwt
from app.tools.base64_tool.logic import encode_text, decode_text
from app.tools.regex_tool.logic import test_regex as run_regex
from app.tools.sql_tool.logic import format_sql, minify_sql

# ─── JSON Tests ───

def test_json_format_valid():
    res = format_json('{"a":1}')
    assert res.success is True
    assert '{\n  "a": 1\n}' in res.output

def test_json_format_invalid():
    res = format_json('{a:1}')
    assert res.success is False
    assert res.error_message != ""

def test_json_minify_valid():
    res = minify_json('{\n  "a": 1\n}')
    assert res.success is True
    assert res.output == '{"a":1}'

def test_json_validate():
    res = validate_json('[1, 2, 3]')
    assert res.success is True
    assert "Valid JSON array" in res.output

# ─── JWT Tests ───

def test_jwt_decode_valid_structure():
    # Header: {"alg":"HS256"} -> eyJhbGciOiJIUzI1NiJ9
    # Payload: {"sub":"123"} -> eyJzdWIiOiIxMjMifQ
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.Signature"
    res = decode_jwt(token)
    assert res.success is True
    assert res.header["alg"] == "HS256"
    assert res.payload["sub"] == "123"

def test_jwt_decode_invalid():
    res = decode_jwt("invalid_token_format")
    assert res.success is False

# ─── Base64 Tests ───

def test_base64_encode_decode():
    res_enc = encode_text("Hello World")
    assert res_enc.success is True
    assert res_enc.output == "SGVsbG8gV29ybGQ="
    
    res_dec = decode_text("SGVsbG8gV29ybGQ=")
    assert res_dec.success is True
    assert res_dec.output == "Hello World"

def test_base64_decode_invalid():
    res = decode_text("!@#$%")
    assert res.success is False

# ─── Regex Tests ───

def test_regex_match():
    res = run_regex(r"\d+", "abc 123 def 456")
    assert res.success is True
    assert len(res.matches) == 2
    assert res.matches[0].full_match == "123"
    assert res.matches[1].full_match == "456"

def test_regex_invalid():
    res = run_regex(r"[a-z", "test")
    assert res.success is False

# ─── SQL Tests ───

def test_sql_format():
    res = format_sql("select id from users where active=1")
    assert res.success is True
    assert "SELECT" in res.output
    assert "FROM" in res.output
    assert "WHERE" in res.output

def test_sql_minify():
    res = minify_sql("SELECT id\nFROM users\n-- comment\nWHERE active=1")
    assert res.success is True
    assert res.output == "SELECT id FROM users WHERE active=1"
