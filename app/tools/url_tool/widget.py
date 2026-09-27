"""
DevTools Desktop — URL Encoder/Decoder Widget
"""

from urllib.parse import quote, unquote

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from app.tools.base_tool import ToolWidget
from app.core.theme import ThemeTokens


class UrlToolWidget(ToolWidget):
    """URL encoder/decoder."""

    def __init__(self, parent=None):
        super().__init__("url", "URL Encoder/Decoder",
                         "URL encode and decode strings", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("URL Encoder / Decoder",
                                           "Encode and decode URL components")
        layout.addLayout(header)

        # Toolbar
        self.btn_encode = self._make_button("Encode", "primary")
        self.btn_decode = self._make_button("Decode")
        self.btn_swap = self._make_button("↕ Swap")
        self.btn_clear = self._make_button("Clear")
        toolbar = self._make_toolbar(self.btn_encode, self.btn_decode,
                                     self.btn_swap, self.btn_clear)
        layout.addLayout(toolbar)
        layout.addSpacing(16)

        # Input
        input_label = QLabel("Input")
        input_label.setProperty("class", "secondary")
        layout.addWidget(input_label)
        layout.addSpacing(4)
        
        self.input_edit = self._make_mono_edit("Enter text or URL to encode/decode…")
        layout.addWidget(self.input_edit, 1)

        layout.addSpacing(16)

        # Output
        output_header = QHBoxLayout()
        output_label = QLabel("Output")
        output_label.setProperty("class", "secondary")
        output_header.addWidget(output_label)
        output_header.addStretch()
        self.btn_copy = self._make_button("Copy", "ghost")
        output_header.addWidget(self.btn_copy)
        layout.addLayout(output_header)
        layout.addSpacing(4)

        self.output_edit = self._make_mono_edit("Result will appear here…", read_only=True)
        layout.addWidget(self.output_edit, 1)

        # Status
        layout.addSpacing(8)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_encode.clicked.connect(self._on_encode)
        self.btn_decode.clicked.connect(self._on_decode)
        self.btn_swap.clicked.connect(self._on_swap)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_copy.clicked.connect(self._on_copy)

    def _on_encode(self):
        text = self.input_edit.toPlainText()
        if not text.strip():
            self._set_status("No input provided", "error")
            return
        try:
            encoded = quote(text, safe="")
            self.output_edit.setPlainText(encoded)
            self._set_status("URL encoded", "success")
        except Exception as e:
            self._set_status(f"Encoding error: {e}", "error")

    def _on_decode(self):
        text = self.input_edit.toPlainText()
        if not text.strip():
            self._set_status("No input provided", "error")
            return
        try:
            decoded = unquote(text)
            self.output_edit.setPlainText(decoded)
            self._set_status("URL decoded", "success")
        except Exception as e:
            self._set_status(f"Decoding error: {e}", "error")

    def _on_swap(self):
        inp = self.input_edit.toPlainText()
        out = self.output_edit.toPlainText()
        self.input_edit.setPlainText(out)
        self.output_edit.setPlainText(inp)

    def _on_copy(self):
        text = self.output_edit.toPlainText()
        if text:
            self._copy_to_clipboard(text)
            self._set_status("Copied to clipboard", "info")

    def clear_workspace(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.status_label.clear()

    def get_result(self) -> str:
        return self.output_edit.toPlainText()
