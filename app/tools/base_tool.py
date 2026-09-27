"""
DevTools Desktop — Base Tool Widget

Common base class for all tool widgets.
Provides standard layout patterns and shared functionality.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QPlainTextEdit, QFrame, QSplitter, QApplication, QFileDialog,
    QSizePolicy, QMessageBox,
)

from app.core.theme import ThemeTokens
from app.core.settings import SettingsManager


class ToolWidget(QWidget):
    """Base class for all tool widgets."""

    # Standard content margins for all tools
    CONTENT_MARGINS = (28, 24, 28, 20)
    TOOLBAR_SPACING = 8

    def __init__(self, tool_id: str, title: str, description: str = "", parent=None):
        super().__init__(parent)
        self.tool_id = tool_id
        self._title = title
        self._description = description
        self._tokens: ThemeTokens | None = None

    def apply_theme(self, tokens: ThemeTokens) -> None:
        """Apply theme to this tool. Override in subclasses for custom styling."""
        self._tokens = tokens
        if hasattr(self, 'status_label') and self.status_label.text():
            # Reset transient status text to a safe, contrasted secondary color on theme switch
            self.status_label.setStyleSheet(f"color: {tokens.text_secondary}; font-size: 11px;")

    def get_result(self) -> str:
        """Return current result text for copy operations. Override in subclasses."""
        return ""

    def clear_workspace(self) -> None:
        """Clear the tool workspace. Override in subclasses."""
        pass

    # ─── Shared Status Handling ───

    def _set_status(self, text: str, status_type: str = "info"):
        """Set the status label text with theme-aware coloring."""
        if self._tokens:
            colors = {
                "success": self._tokens.status_success,
                "error": self._tokens.status_error,
                "warning": self._tokens.status_warning,
                "info": self._tokens.text_secondary,
            }
            color = colors.get(status_type, self._tokens.text_secondary)
            self.status_label.setStyleSheet(f"color: {color}; font-size: 11px;")
        self.status_label.setText(text)

    # ─── Helpers ───

    @staticmethod
    def _make_label(text: str, class_name: str = "") -> QLabel:
        label = QLabel(text)
        if class_name:
            label.setProperty("class", class_name)
        return label

    @staticmethod
    def _make_button(text: str, class_name: str = "", tooltip: str = "") -> QPushButton:
        btn = QPushButton(text)
        if class_name:
            btn.setProperty("class", class_name)
        if tooltip:
            btn.setToolTip(tooltip)
        return btn

    @staticmethod
    def _make_mono_edit(placeholder: str = "", read_only: bool = False) -> QPlainTextEdit:
        edit = QPlainTextEdit()
        edit.setPlaceholderText(placeholder)
        edit.setReadOnly(read_only)
        edit.setTabStopDistance(32)
        return edit

    def _make_toolbar(self, *buttons: QPushButton) -> QHBoxLayout:
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setSpacing(self.TOOLBAR_SPACING)
        for btn in buttons:
            toolbar.addWidget(btn)
        toolbar.addStretch()
        return toolbar

    def _make_section_header(self, title: str, description: str = "") -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 12)
        title_label = QLabel(title)
        title_label.setProperty("class", "heading")
        layout.addWidget(title_label)
        if description:
            desc_label = QLabel(description)
            desc_label.setProperty("class", "secondary")
            layout.addWidget(desc_label)
        return layout

    def _make_status_label(self) -> QLabel:
        """Create and return a standardized status label."""
        label = QLabel("")
        label.setProperty("class", "secondary")
        return label

    def _copy_to_clipboard(self, text: str) -> None:
        if text:
            QApplication.clipboard().setText(text)

    def _show_error(self, title: str, message: str, details: str = "") -> None:
        """Show user-friendly error message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        if details:
            msg.setDetailedText(details)
        msg.exec()

    def _open_file_dialog(self, title: str = "Open File",
                          filters: str = "All Files (*)") -> str | None:
        path, _ = QFileDialog.getOpenFileName(self, title, "", filters)
        return path if path else None

    def _save_file_dialog(self, title: str = "Save File",
                          filters: str = "All Files (*)",
                          default_name: str = "") -> str | None:
        path, _ = QFileDialog.getSaveFileName(self, title, default_name, filters)
        return path if path else None
