"""
DevTools Desktop — Hash Generator Widget
"""

import hashlib
import time
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView,
)

from app.tools.base_tool import ToolWidget
from app.core.theme import ThemeTokens

ALGORITHMS = ["MD5", "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512"]
ALGO_MAP = {
    "MD5": "md5",
    "SHA-1": "sha1",
    "SHA-224": "sha224",
    "SHA-256": "sha256",
    "SHA-384": "sha384",
    "SHA-512": "sha512",
}
INSECURE_ALGOS = {"MD5", "SHA-1"}


class HashToolWidget(ToolWidget):
    """Cryptographic hash generator for text and files."""

    def __init__(self, parent=None):
        super().__init__("hash", "Hash Generator",
                         "Generate cryptographic hashes", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("Hash Generator",
                                           "Generate MD5, SHA-1, SHA-256, SHA-384, SHA-512 hashes")
        layout.addLayout(header)

        tabs = QTabWidget()

        # ─── Text Tab ───
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)
        text_layout.setContentsMargins(16, 16, 16, 16)
        text_layout.setSpacing(0)

        self.btn_hash_text = self._make_button("Hash", "primary")
        self.btn_clear = self._make_button("Clear")
        text_toolbar = self._make_toolbar(self.btn_hash_text, self.btn_clear)
        text_layout.addLayout(text_toolbar)
        text_layout.addSpacing(16)

        input_label = QLabel("Input Text")
        input_label.setProperty("class", "secondary")
        text_layout.addWidget(input_label)
        text_layout.addSpacing(4)
        
        self.text_input = self._make_mono_edit("Enter text to hash…")
        self.text_input.setMaximumHeight(100)
        text_layout.addWidget(self.text_input)
        text_layout.addSpacing(16)

        # Results table
        self.text_table = QTableWidget(0, 3)
        self.text_table.setHorizontalHeaderLabels(["Algorithm", "Hash", ""])
        self.text_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents)
        self.text_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch)
        self.text_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents)
        self.text_table.verticalHeader().setVisible(False)
        self.text_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.text_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        text_layout.addWidget(self.text_table)

        tabs.addTab(text_tab, "Text")

        # ─── File Tab ───
        file_tab = QWidget()
        file_layout = QVBoxLayout(file_tab)
        file_layout.setContentsMargins(16, 16, 16, 16)
        file_layout.setSpacing(0)

        self.btn_hash_file = self._make_button("Hash File", "primary")
        file_toolbar = self._make_toolbar(self.btn_hash_file)
        file_layout.addLayout(file_toolbar)
        file_layout.addSpacing(16)

        self.file_label = QLabel("No file selected")
        self.file_label.setProperty("class", "secondary")
        file_layout.addWidget(self.file_label)
        file_layout.addSpacing(8)

        self.file_table = QTableWidget(0, 3)
        self.file_table.setHorizontalHeaderLabels(["Algorithm", "Hash", ""])
        self.file_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents)
        self.file_table.verticalHeader().setVisible(False)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.file_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        file_layout.addWidget(self.file_table)

        tabs.addTab(file_tab, "File")

        layout.addWidget(tabs, 1)

        # Notice
        layout.addSpacing(12)
        notice = QLabel("⚠ MD5 and SHA-1 are not suitable for security-critical purposes "
                        "such as password hashing or digital signatures.")
        notice.setProperty("class", "notice")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        # Status
        layout.addSpacing(8)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_hash_text.clicked.connect(self._on_hash_text)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_hash_file.clicked.connect(self._on_hash_file)

    def _compute_hashes(self, data: bytes) -> list:
        results = []
        for algo_name in ALGORITHMS:
            algo_key = ALGO_MAP[algo_name]
            t0 = time.perf_counter()
            h = hashlib.new(algo_key, data)
            digest = h.hexdigest()
            elapsed = time.perf_counter() - t0
            results.append((algo_name, digest, elapsed))
        return results

    def _populate_table(self, table: QTableWidget, results: list, data_size: int):
        table.setRowCount(len(results))
        for row, (algo, digest, elapsed) in enumerate(results):
            algo_item = QTableWidgetItem(algo)
            if algo in INSECURE_ALGOS:
                algo_item.setForeground(Qt.GlobalColor.darkYellow)
            table.setItem(row, 0, algo_item)
            table.setItem(row, 1, QTableWidgetItem(digest))
            copy_btn = self._make_button("Copy", "ghost")
            copy_btn.clicked.connect(lambda _, d=digest: self._copy_to_clipboard(d))
            table.setCellWidget(row, 2, copy_btn)

        size_str = f"{data_size:,} bytes"
        total_time = sum(r[2] for r in results)
        self._set_status(f"Input: {size_str} — Total: {total_time:.3f}s", "success")

    def _on_hash_text(self):
        text = self.text_input.toPlainText()
        if not text:
            self._set_status("No input provided", "error")
            return
        data = text.encode("utf-8")
        results = self._compute_hashes(data)
        self._populate_table(self.text_table, results, len(data))

    def _on_hash_file(self):
        path = self._open_file_dialog("Select File to Hash", "All Files (*)")
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = f.read()
            self.file_label.setText(f"{os.path.basename(path)} — {len(data):,} bytes")
            results = self._compute_hashes(data)
            self._populate_table(self.file_table, results, len(data))
        except Exception as e:
            self._set_status(f"Failed to read file: {e}", "error")

    def clear_workspace(self):
        self.text_input.clear()
        self.text_table.setRowCount(0)
        self.file_table.setRowCount(0)
        self.file_label.setText("No file selected")
        self.status_label.clear()

    def get_result(self) -> str:
        lines = []
        for row in range(self.text_table.rowCount()):
            algo = self.text_table.item(row, 0)
            digest = self.text_table.item(row, 1)
            if algo and digest:
                lines.append(f"{algo.text()}: {digest.text()}")
        return "\n".join(lines)
