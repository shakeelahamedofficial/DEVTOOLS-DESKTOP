"""
DevTools Desktop — JSON Tool Widget

Complete JSON workspace with format, minify, validate, and file operations.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QSplitter, QLabel, QPushButton,
    QPlainTextEdit, QApplication, QWidget,
)

from app.tools.base_tool import ToolWidget
from app.tools.json_tool.logic import format_json, minify_json, validate_json
from app.core.theme import ThemeTokens


class JsonToolWidget(ToolWidget):
    """JSON formatter, minifier, and validator."""

    def __init__(self, parent=None):
        super().__init__("json", "JSON Formatter",
                         "Format, minify, and validate JSON", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        # Header
        header = self._make_section_header("JSON Formatter",
                                           "Format, minify, and validate JSON data")
        layout.addLayout(header)

        # Toolbar
        self.btn_format = self._make_button("Format", "primary", "Format JSON (Ctrl+Enter)")
        self.btn_minify = self._make_button("Minify", tooltip="Minify JSON")
        self.btn_validate = self._make_button("Validate", tooltip="Validate JSON")
        self.btn_load = self._make_button("Load File", tooltip="Load JSON from file")
        self.btn_clear = self._make_button("Clear", tooltip="Clear all (Ctrl+Shift+X)")

        toolbar = self._make_toolbar(
            self.btn_format, self.btn_minify, self.btn_validate,
            self.btn_load, self.btn_clear
        )
        layout.addLayout(toolbar)
        layout.addSpacing(16)

        # Splitter for input/output
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Input
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        input_label = QLabel("Input")
        input_label.setProperty("class", "secondary")
        input_layout.addWidget(input_label)

        self.input_edit = self._make_mono_edit("Paste or type JSON here…")
        input_layout.addWidget(self.input_edit)
        splitter.addWidget(input_container)

        # Output
        output_container = QWidget()
        output_layout = QVBoxLayout(output_container)
        output_layout.setContentsMargins(0, 16, 0, 0)
        output_layout.setSpacing(8)

        output_header = QHBoxLayout()
        output_label = QLabel("Output")
        output_label.setProperty("class", "secondary")
        output_header.addWidget(output_label)
        output_header.addStretch()

        self.btn_copy = self._make_button("Copy", "ghost", "Copy output (Ctrl+Shift+C)")
        self.btn_save = self._make_button("Save", "ghost", "Save output to file")
        output_header.addWidget(self.btn_copy)
        output_header.addWidget(self.btn_save)
        output_layout.addLayout(output_header)

        self.output_edit = self._make_mono_edit("Output will appear here…", read_only=True)
        output_layout.addWidget(self.output_edit)
        splitter.addWidget(output_container)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)

        # Status bar
        layout.addSpacing(12)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect signals
        self.btn_format.clicked.connect(self._on_format)
        self.btn_minify.clicked.connect(self._on_minify)
        self.btn_validate.clicked.connect(self._on_validate)
        self.btn_load.clicked.connect(self._on_load)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_copy.clicked.connect(self._on_copy)
        self.btn_save.clicked.connect(self._on_save)

    def _on_format(self):
        result = format_json(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            self._set_status("Formatted successfully", "success")
        else:
            self.output_edit.setPlainText("")
            self._set_status(result.error_message, "error")

    def _on_minify(self):
        result = minify_json(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            size = len(result.output.encode("utf-8"))
            self._set_status(f"Minified — {size:,} bytes", "success")
        else:
            self.output_edit.setPlainText("")
            self._set_status(result.error_message, "error")

    def _on_validate(self):
        result = validate_json(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            self._set_status("✓ Valid JSON", "success")
        else:
            self.output_edit.setPlainText("")
            self._set_status(result.error_message, "error")

    def _on_load(self):
        path = self._open_file_dialog("Open JSON File", "JSON Files (*.json);;All Files (*)")
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.input_edit.setPlainText(content)
                self._set_status(f"Loaded: {path}", "info")
            except Exception as e:
                self._set_status(f"Failed to load file: {e}", "error")

    def _on_copy(self):
        text = self.output_edit.toPlainText()
        if text:
            self._copy_to_clipboard(text)
            self._set_status("Copied to clipboard", "info")

    def _on_save(self):
        text = self.output_edit.toPlainText()
        if not text:
            self._set_status("Nothing to save", "error")
            return
        path = self._save_file_dialog("Save JSON", "JSON Files (*.json);;All Files (*)",
                                      "output.json")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                self._set_status(f"Saved: {path}", "success")
            except Exception as e:
                self._set_status(f"Failed to save: {e}", "error")

    def clear_workspace(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.status_label.clear()

    def get_result(self) -> str:
        return self.output_edit.toPlainText()
