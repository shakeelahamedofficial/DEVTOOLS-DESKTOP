"""
DevTools Desktop — UUID Generator Widget
"""

import uuid as uuid_mod

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QCheckBox
)

from app.tools.base_tool import ToolWidget
from app.core.theme import ThemeTokens


BATCH_SIZES = [1, 5, 10, 25, 50, 100, 500, 1000]


class UuidToolWidget(ToolWidget):
    """UUID v4 generator with batch support."""

    def __init__(self, parent=None):
        super().__init__("uuid", "UUID Generator",
                         "Generate UUIDs in bulk", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("UUID Generator", "Generate UUID v4 identifiers")
        layout.addLayout(header)

        # Controls
        controls = QHBoxLayout()
        controls.setSpacing(16)

        count_label = QLabel("Count:")
        controls.addWidget(count_label)

        self.count_combo = QComboBox()
        for size in BATCH_SIZES:
            self.count_combo.addItem(str(size), size)
        self.count_combo.setCurrentIndex(0)
        self.count_combo.setFixedWidth(80)
        controls.addWidget(self.count_combo)

        self.uppercase_cb = QCheckBox("Uppercase")
        controls.addWidget(self.uppercase_cb)

        self.no_hyphens_cb = QCheckBox("No hyphens")
        controls.addWidget(self.no_hyphens_cb)

        controls.addStretch()

        self.btn_generate = self._make_button("Generate", "primary")
        self.btn_clear = self._make_button("Clear")
        controls.addWidget(self.btn_generate)
        controls.addWidget(self.btn_clear)

        layout.addLayout(controls)
        layout.addSpacing(16)

        # Output
        output_header = QHBoxLayout()
        output_label = QLabel("Generated UUIDs")
        output_label.setProperty("class", "secondary")
        output_header.addWidget(output_label)
        output_header.addStretch()
        self.btn_copy = self._make_button("Copy All", "ghost")
        self.btn_export_txt = self._make_button("Export TXT", "ghost")
        self.btn_export_csv = self._make_button("Export CSV", "ghost")
        output_header.addWidget(self.btn_copy)
        output_header.addWidget(self.btn_export_txt)
        output_header.addWidget(self.btn_export_csv)
        layout.addLayout(output_header)
        layout.addSpacing(4)

        self.output_edit = self._make_mono_edit("Generated UUIDs will appear here…",
                                                read_only=True)
        layout.addWidget(self.output_edit, 1)

        # Status
        layout.addSpacing(8)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.btn_copy.clicked.connect(self._on_copy)
        self.btn_export_txt.clicked.connect(self._on_export_txt)
        self.btn_export_csv.clicked.connect(self._on_export_csv)

    def _on_generate(self):
        count = self.count_combo.currentData()
        uppercase = self.uppercase_cb.isChecked()
        no_hyphens = self.no_hyphens_cb.isChecked()

        uuids = set()
        while len(uuids) < count:
            u = str(uuid_mod.uuid4())
            if no_hyphens:
                u = u.replace("-", "")
            if uppercase:
                u = u.upper()
            uuids.add(u)

        result = "\n".join(sorted(uuids))
        self.output_edit.setPlainText(result)
        self._set_status(f"Generated {count} unique UUID(s)", "success")

    def _on_copy(self):
        text = self.output_edit.toPlainText()
        if text:
            self._copy_to_clipboard(text)
            self._set_status("Copied to clipboard", "info")

    def _on_export_txt(self):
        text = self.output_edit.toPlainText()
        if not text:
            return
        path = self._save_file_dialog("Export UUIDs", "Text Files (*.txt)", "uuids.txt")
        if path:
            with open(path, "w") as f:
                f.write(text)
            self._set_status(f"Exported to {path}", "success")

    def _on_export_csv(self):
        text = self.output_edit.toPlainText()
        if not text:
            return
        path = self._save_file_dialog("Export UUIDs", "CSV Files (*.csv)", "uuids.csv")
        if path:
            lines = text.strip().split("\n")
            with open(path, "w") as f:
                f.write("uuid\n")
                for line in lines:
                    f.write(f"{line}\n")
            self._set_status(f"Exported to {path}", "success")

    def clear_workspace(self):
        self.output_edit.clear()
        self.status_label.clear()

    def get_result(self) -> str:
        return self.output_edit.toPlainText()
