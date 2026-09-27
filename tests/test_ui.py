import sys
import os
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Ensure app is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ui.main_window import MainWindow
from app.core.tool_registry import register_all_tools

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    register_all_tools()
    yield app
    # app.quit()

@pytest.fixture
def main_window(app):
    window = MainWindow()
    yield window
    window.close()

def test_main_window_loads(main_window):
    assert main_window.windowTitle() == "DevTools Desktop"
    assert main_window.sidebar is not None
    assert main_window.content_stack is not None

def test_json_tool_ui(main_window):
    main_window._switch_tool("json")
    widget = main_window.content_stack.currentWidget()
    assert widget.tool_id == "json"
    
    # Test format
    widget.input_edit.setPlainText('{"a":1}')
    widget.btn_format.click()
    assert '{\n  "a": 1\n}' in widget.output_edit.toPlainText()
    
    # Test validate
    widget.input_edit.setPlainText('{"a":1}')
    widget.btn_validate.click()
    assert "Valid JSON object" in widget.output_edit.toPlainText()

def test_jwt_tool_ui(main_window):
    main_window._switch_tool("jwt")
    widget = main_window.content_stack.currentWidget()
    
    # Valid JWT
    widget.token_input.setText("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.Signature")
    widget.btn_decode.click()
    assert '"alg": "HS256"' in widget.header_edit.toPlainText()
    assert '"sub": "123"' in widget.payload_edit.toPlainText()
    
    # Check clear
    widget.btn_clear.click()
    assert widget.token_input.text() == ""
    assert widget.header_edit.toPlainText() == ""

def test_base64_tool_ui(main_window):
    main_window._switch_tool("base64")
    widget = main_window.content_stack.currentWidget()
    
    # Test encode
    widget.input_edit.setPlainText("Hello World")
    widget.btn_encode.click()
    assert widget.output_edit.toPlainText() == "SGVsbG8gV29ybGQ="
    
    # Test decode
    widget.input_edit.setPlainText("SGVsbG8gV29ybGQ=")
    widget.btn_decode.click()
    assert widget.output_edit.toPlainText() == "Hello World"

def test_url_tool_ui(main_window):
    main_window._switch_tool("url")
    widget = main_window.content_stack.currentWidget()
    
    widget.input_edit.setPlainText("Hello World!")
    widget.btn_encode.click()
    assert widget.output_edit.toPlainText() == "Hello%20World%21"

def test_uuid_tool_ui(main_window):
    main_window._switch_tool("uuid")
    widget = main_window.content_stack.currentWidget()
    
    # Select count=5 from the combo box (index 1 maps to 5 in BATCH_SIZES)
    widget.count_combo.setCurrentIndex(1)  # BATCH_SIZES[1] == 5
    widget.btn_generate.click()
    lines = widget.output_edit.toPlainText().strip().split("\n")
    assert len(lines) == 5
    assert len(lines[0]) == 36  # standard uuid length

def test_hash_tool_ui(main_window):
    main_window._switch_tool("hash")
    widget = main_window.content_stack.currentWidget()
    
    widget.text_input.setPlainText("test")
    widget.btn_hash_text.click()
    
    assert widget.text_table.rowCount() == 6
    md5_hash = widget.text_table.item(0, 1).text()
    assert md5_hash == "098f6bcd4621d373cade4e832627b4f6"

def test_timestamp_tool_ui(main_window):
    main_window._switch_tool("timestamp")
    widget = main_window.content_stack.currentWidget()
    
    widget.input_edit.setText("1727361180")
    widget.btn_convert.click()
    # Check conversion result labels
    assert widget.res_unix.text() == "1727361180"

def test_regex_tool_ui(main_window):
    main_window._switch_tool("regex")
    widget = main_window.content_stack.currentWidget()
    
    widget.pattern_input.setText(r"\d+")
    widget.test_edit.setPlainText("123 abc")
    
    # Wait for the debounce timer
    from PySide6.QtTest import QTest
    QTest.qWait(300)
    
    assert widget.matches_tree.topLevelItemCount() > 0
    assert widget.matches_tree.topLevelItem(0).text(1) == "123"

def test_sql_tool_ui(main_window):
    main_window._switch_tool("sql")
    widget = main_window.content_stack.currentWidget()
    
    widget.input_edit.setPlainText("select * from users")
    widget.btn_format.click()
    assert "SELECT" in widget.output_edit.toPlainText()

def test_http_tool_ui(main_window):
    main_window._switch_tool("http")
    widget = main_window.content_stack.currentWidget()
    
    # Set a URL but don't actually run a real request to avoid hanging or relying on network
    widget.url_input.setText("http://example.com")
    # Verify elements exist
    assert widget.method_combo.currentText() == "GET"
    assert widget.btn_send is not None
