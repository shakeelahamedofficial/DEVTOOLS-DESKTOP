"""
DevTools Desktop — Base64 Tool Widget
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QWidget,
)

from app.tools.base_tool import ToolWidget
from app.tools.base64_tool.logic import encode_text, decode_text, encode_file, decode_to_bytes
from app.core.theme import ThemeTokens


class Base64ToolWidget(ToolWidget):
    """Base64 encoder/decoder with text and file support."""

    def __init__(self, parent=None):
        super().__init__("base64", "Base64 Encoder/Decoder",
                         "Encode and decode Base64", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("Base64 Encoder / Decoder",
                                           "Encode text or files to Base64, decode Base64 back")
        layout.addLayout(header)

        # Tabs: Text and File
        tabs = QTabWidget()

        # ─── Text Tab ───
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)
        text_layout.setContentsMargins(16, 16, 16, 16)
        text_layout.setSpacing(0)

        # Toolbar
        self.btn_encode = self._make_button("Encode", "primary")
        self.btn_decode = self._make_button("Decode")
        self.btn_swap = self._make_button("↕ Swap")
        self.btn_clear = self._make_button("Clear")
        toolbar = self._make_toolbar(self.btn_encode, self.btn_decode,
                                     self.btn_swap, self.btn_clear)
        text_layout.addLayout(toolbar)
        text_layout.addSpacing(16)

        # Input
        input_label = QLabel("Input")
        input_label.setProperty("class", "secondary")
        text_layout.addWidget(input_label)
        text_layout.addSpacing(4)
        
        self.input_edit = self._make_mono_edit("Enter text or Base64…")
        text_layout.addWidget(self.input_edit, 1)
        text_layout.addSpacing(16)

        # Output
        output_header = QHBoxLayout()
        output_label = QLabel("Output")
        output_label.setProperty("class", "secondary")
        output_header.addWidget(output_label)
        output_header.addStretch()
        self.btn_copy = self._make_button("Copy", "ghost")
        output_header.addWidget(self.btn_copy)
        text_layout.addLayout(output_header)
        text_layout.addSpacing(4)

        self.output_edit = self._make_mono_edit("Result will appear here…", read_only=True)
        text_layout.addWidget(self.output_edit, 1)

        tabs.addTab(text_tab, "Text")

        # ─── File Tab ───
        file_tab = QWidget()
        file_layout = QVBoxLayout(file_tab)
        file_layout.setContentsMargins(16, 16, 16, 16)
        file_layout.setSpacing(0)

        self.btn_encode_file = self._make_button("Encode File to Base64", "primary")
        self.btn_decode_file = self._make_button("Decode Base64 to File")
        file_toolbar = self._make_toolbar(self.btn_encode_file, self.btn_decode_file)
        file_layout.addLayout(file_toolbar)
        file_layout.addSpacing(16)

        file_output_label = QLabel("Base64 Output / Input")
        file_output_label.setProperty("class", "secondary")
        file_layout.addWidget(file_output_label)
        file_layout.addSpacing(4)

        self.file_b64_edit = self._make_mono_edit(
            "File Base64 content will appear here, or paste Base64 to decode to a file…"
        )
        file_layout.addWidget(self.file_b64_edit, 1)
        file_layout.addSpacing(8)

        self.btn_copy_file = self._make_button("Copy", "ghost")
        file_copy_row = QHBoxLayout()
        file_copy_row.addStretch()
        file_copy_row.addWidget(self.btn_copy_file)
        file_layout.addLayout(file_copy_row)

        tabs.addTab(file_tab, "File")

        layout.addWidget(tabs, 1)

        # Status
        layout.addSpacing(8)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_encode.clicked.connect(self._on_encode)
        self.btn_decode.clicked.connect(self._on_decode)
        self.btn_swap.clicked.connect(self._on_swap)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_copy.clicked.connect(
            lambda: self._copy_and_status(self.output_edit.toPlainText()))
        self.btn_encode_file.clicked.connect(self._on_encode_file)
        self.btn_decode_file.clicked.connect(self._on_decode_file)
        self.btn_copy_file.clicked.connect(
            lambda: self._copy_and_status(self.file_b64_edit.toPlainText()))

    def _on_encode(self):
        result = encode_text(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            self._set_status("Encoded successfully", "success")
        else:
            self._set_status(result.error_message, "error")

    def _on_decode(self):
        result = decode_text(self.input_edit.toPlainText())
        if result.success:
            self.output_edit.setPlainText(result.output)
            self._set_status("Decoded successfully", "success")
        else:
            self._set_status(result.error_message, "error")

    def _on_swap(self):
        inp = self.input_edit.toPlainText()
        out = self.output_edit.toPlainText()
        self.input_edit.setPlainText(out)
        self.output_edit.setPlainText(inp)

    def _on_encode_file(self):
        path = self._open_file_dialog("Select File to Encode", "All Files (*)")
        if path:
            result = encode_file(path)
            if result.success:
                self.file_b64_edit.setPlainText(result.output)
                self._set_status(f"File encoded: {path}", "success")
            else:
                self._set_status(result.error_message, "error")

    def _on_decode_file(self):
        b64 = self.file_b64_edit.toPlainText()
        result = decode_to_bytes(b64)
        if not result.success:
            self._set_status(result.error_message, "error")
            return
        path = self._save_file_dialog("Save Decoded File", "All Files (*)")
        if path:
            try:
                with open(path, "wb") as f:
                    f.write(result.output_bytes)
                self._set_status(f"File saved: {path}", "success")
            except Exception as e:
                self._set_status(f"Failed to save: {e}", "error")

    def _copy_and_status(self, text: str):
        if text:
            self._copy_to_clipboard(text)
            self._set_status("Copied to clipboard", "info")

    def clear_workspace(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.file_b64_edit.clear()
        self.status_label.clear()

    def get_result(self) -> str:
        return self.output_edit.toPlainText()
