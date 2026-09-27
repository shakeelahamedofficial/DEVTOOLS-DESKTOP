"""
DevTools Desktop — JWT Decoder Widget

JWT token inspection with header, payload, and metadata display.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGridLayout, QWidget,
)

from app.tools.base_tool import ToolWidget
from app.tools.jwt_tool.logic import decode_jwt
from app.core.theme import ThemeTokens


class JwtToolWidget(ToolWidget):
    """JWT decoder and inspector."""

    def __init__(self, parent=None):
        super().__init__("jwt", "JWT Decoder",
                         "Decode and inspect JWT tokens", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        # Header
        header = self._make_section_header(
            "JWT Decoder",
            "Decode and inspect JSON Web Tokens — does not verify signatures"
        )
        layout.addLayout(header)

        # Input
        input_row = QHBoxLayout()
        input_row.setSpacing(8)
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Paste JWT token here (eyJ…)")
        self.token_input.setMinimumHeight(36)
        input_row.addWidget(self.token_input, 1)

        self.btn_decode = self._make_button("Decode", "primary")
        self.btn_clear = self._make_button("Clear")
        input_row.addWidget(self.btn_decode)
        input_row.addWidget(self.btn_clear)
        layout.addLayout(input_row)

        layout.addSpacing(8)

        # Warning notice
        notice = QLabel("⚠ Token decoding does not verify the token signature. "
                        "Never send tokens to untrusted services.")
        notice.setProperty("class", "notice")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        layout.addSpacing(16)

        # Metadata grid
        self.meta_widget = QWidget()
        meta_grid = QGridLayout(self.meta_widget)
        meta_grid.setContentsMargins(0, 0, 0, 0)
        meta_grid.setSpacing(12)
        meta_grid.setColumnStretch(1, 1)
        meta_grid.setColumnStretch(3, 1)

        self.meta_labels = {}
        fields = [
            ("Algorithm", 0, 0), ("Token Type", 0, 2),
            ("Issued At", 1, 0), ("Expiration", 1, 2),
            ("Status", 2, 0),
        ]
        for name, row, col in fields:
            label = QLabel(name)
            label.setProperty("class", "secondary")
            value = QLabel("—")
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.meta_labels[name] = value
            meta_grid.addWidget(label, row, col)
            meta_grid.addWidget(value, row, col + 1)

        self.meta_widget.setVisible(False)
        layout.addWidget(self.meta_widget)

        layout.addSpacing(16)

        # Header output
        header_label = QLabel("Header")
        header_label.setProperty("class", "secondary")
        layout.addWidget(header_label)
        layout.addSpacing(4)
        
        self.header_edit = self._make_mono_edit("JWT header will appear here…", read_only=True)
        self.header_edit.setMaximumHeight(120)
        layout.addWidget(self.header_edit)

        layout.addSpacing(16)

        # Payload output
        payload_header = QHBoxLayout()
        payload_label = QLabel("Payload")
        payload_label.setProperty("class", "secondary")
        payload_header.addWidget(payload_label)
        payload_header.addStretch()
        self.btn_copy_payload = self._make_button("Copy", "ghost")
        payload_header.addWidget(self.btn_copy_payload)
        layout.addLayout(payload_header)
        layout.addSpacing(4)

        self.payload_edit = self._make_mono_edit("JWT payload will appear here…", read_only=True)
        layout.addWidget(self.payload_edit, 1)

        # Status
        layout.addSpacing(8)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_decode.clicked.connect(self._on_decode)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_copy_payload.clicked.connect(self._on_copy_payload)
        self.token_input.returnPressed.connect(self._on_decode)

    def _on_decode(self):
        result = decode_jwt(self.token_input.text())
        if result.success:
            self.header_edit.setPlainText(result.header_raw)
            self.payload_edit.setPlainText(result.payload_raw)

            self.meta_labels["Algorithm"].setText(result.algorithm)
            self.meta_labels["Token Type"].setText(result.token_type)
            self.meta_labels["Issued At"].setText(result.issued_at or "—")
            self.meta_labels["Expiration"].setText(result.expiration or "—")

            if result.is_expired is True:
                self.meta_labels["Status"].setText("Expired")
                if self._tokens:
                    self.meta_labels["Status"].setStyleSheet(
                        f"color: {self._tokens.status_error};")
            elif result.is_expired is False:
                self.meta_labels["Status"].setText("Active")
                if self._tokens:
                    self.meta_labels["Status"].setStyleSheet(
                        f"color: {self._tokens.status_success};")
            else:
                self.meta_labels["Status"].setText("—")

            self.meta_widget.setVisible(True)
            self._set_status("Token decoded successfully", "success")
        else:
            self.header_edit.clear()
            self.payload_edit.clear()
            self.meta_widget.setVisible(False)
            self._set_status(result.error_message, "error")

    def _on_copy_payload(self):
        text = self.payload_edit.toPlainText()
        if text:
            self._copy_to_clipboard(text)
            self._set_status("Payload copied to clipboard", "info")

    def clear_workspace(self):
        self.token_input.clear()
        self.header_edit.clear()
        self.payload_edit.clear()
        self.meta_widget.setVisible(False)
        self.status_label.clear()

    def get_result(self) -> str:
        return self.payload_edit.toPlainText()
