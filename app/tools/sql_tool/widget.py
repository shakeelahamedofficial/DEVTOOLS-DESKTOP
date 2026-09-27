"""
DevTools Desktop — SQL Tool Widget
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QSplitter, QLabel, QWidget
)

from app.tools.base_tool import ToolWidget
from app.tools.sql_tool.logic import format_sql, minify_sql
from app.core.theme import ThemeTokens


class SqlToolWidget(ToolWidget):
    """SQL formatter and minifier."""

    def __init__(self, parent=None):
        super().__init__("sql", "SQL Formatter",
                         "Format and minify SQL queries", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("SQL Formatter",
                                           "Format, minify, and clean up SQL queries")
        layout.addLayout(header)

        # Toolbar
        self.btn_format = self._make_button("Format", "primary", "Format SQL (Ctrl+Enter)")
        self.btn_minify = self._make_button("Minify", tooltip="Minify SQL")
        self.btn_example = self._make_button("Example", tooltip="Load example query")
        self.btn_clear = self._make_button("Clear", tooltip="Clear all")

        toolbar = self._make_toolbar(
            self.btn_format, self.btn_minify, self.btn_example, self.btn_clear
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

        self.input_edit = self._make_mono_edit("Paste or type SQL here…")
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
        output_header.addWidget(self.btn_copy)
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
        self.btn_example.clicked.connect(self._on_example)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_copy.clicked.connect(self._on_copy)

    def _on_format(self):
        result = format_sql(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            self._set_status("Formatted successfully", "success")
        else:
            self._set_status(result.error_message, "error")

    def _on_minify(self):
        result = minify_sql(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            self._set_status("Minified successfully", "success")
        else:
            self._set_status(result.error_message, "error")

    def _on_example(self):
        example_sql = """SELECT u.id, u.username, p.title, COUNT(c.id) AS comment_count FROM users u LEFT JOIN posts p ON u.id = p.user_id LEFT JOIN comments c ON p.id = c.post_id WHERE u.active = 1 AND p.published_at IS NOT NULL GROUP BY u.id, u.username, p.title ORDER BY comment_count DESC LIMIT 10"""
        self.input_edit.setPlainText(example_sql)
        self._set_status("Loaded example", "info")

    def _on_copy(self):
        text = self.output_edit.toPlainText()
        if text:
            self._copy_to_clipboard(text)
            self._set_status("Copied to clipboard", "info")

    def clear_workspace(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.status_label.setText("")

    def get_result(self) -> str:
        return self.output_edit.toPlainText()
