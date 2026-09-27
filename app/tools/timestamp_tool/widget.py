"""
DevTools Desktop — Timestamp Converter Widget
"""

import time
from datetime import datetime, timezone
import dateutil.parser

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGroupBox, QGridLayout,
)

from app.tools.base_tool import ToolWidget
from app.core.theme import ThemeTokens


class TimestampToolWidget(ToolWidget):
    """Timestamp converter."""

    def __init__(self, parent=None):
        super().__init__("timestamp", "Timestamp Converter",
                         "Convert between Unix timestamps and dates", parent)
        self._setup_ui()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_current_time)
        self._timer.start(1000)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("Timestamp Converter",
                                           "Convert Unix timestamps to human-readable dates and vice-versa")
        layout.addLayout(header)

        # ─── Current Time ───
        current_group = QGroupBox("Current Time")
        current_layout = QGridLayout(current_group)
        current_layout.setContentsMargins(16, 20, 16, 16)
        current_layout.setSpacing(12)
        
        self.lbl_current_unix = QLabel("—")
        self.lbl_current_unix.setProperty("class", "title")
        self.lbl_current_unix.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        self.lbl_current_utc = QLabel("—")
        self.lbl_current_utc.setProperty("class", "secondary")
        self.lbl_current_utc.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.lbl_current_local = QLabel("—")
        self.lbl_current_local.setProperty("class", "secondary")
        self.lbl_current_local.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        btn_copy_current = self._make_button("Copy", "ghost")
        btn_copy_current.clicked.connect(lambda: self._copy_and_status(self.lbl_current_unix.text()))

        current_layout.addWidget(QLabel("Unix (s):"), 0, 0)
        current_layout.addWidget(self.lbl_current_unix, 0, 1)
        current_layout.addWidget(btn_copy_current, 0, 2, Qt.AlignmentFlag.AlignRight)
        
        current_layout.addWidget(QLabel("UTC:"), 1, 0)
        current_layout.addWidget(self.lbl_current_utc, 1, 1, 1, 2)
        
        current_layout.addWidget(QLabel("Local:"), 2, 0)
        current_layout.addWidget(self.lbl_current_local, 2, 1, 1, 2)

        current_layout.setColumnStretch(1, 1)
        layout.addWidget(current_group)

        layout.addSpacing(24)

        # ─── Conversion ───
        conv_group = QGroupBox("Convert")
        conv_layout = QVBoxLayout(conv_group)
        conv_layout.setContentsMargins(16, 20, 16, 16)
        conv_layout.setSpacing(16)
        
        input_row = QHBoxLayout()
        input_row.setSpacing(8)
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Enter Unix timestamp or date string…")
        self.input_edit.setMinimumHeight(36)
        input_row.addWidget(self.input_edit, 1)

        self.btn_convert = self._make_button("Convert", "primary")
        self.btn_clear = self._make_button("Clear")
        input_row.addWidget(self.btn_convert)
        input_row.addWidget(self.btn_clear)
        conv_layout.addLayout(input_row)

        res_grid = QGridLayout()
        res_grid.setSpacing(12)
        self.res_unix = QLabel("—")
        self.res_unix.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.res_unix_ms = QLabel("—")
        self.res_unix_ms.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.res_utc = QLabel("—")
        self.res_utc.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.res_local = QLabel("—")
        self.res_local.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        res_grid.addWidget(QLabel("Unix (s):"), 0, 0)
        res_grid.addWidget(self.res_unix, 0, 1)
        res_grid.addWidget(QLabel("Unix (ms):"), 1, 0)
        res_grid.addWidget(self.res_unix_ms, 1, 1)
        res_grid.addWidget(QLabel("UTC:"), 2, 0)
        res_grid.addWidget(self.res_utc, 2, 1)
        res_grid.addWidget(QLabel("Local:"), 3, 0)
        res_grid.addWidget(self.res_local, 3, 1)
        res_grid.setColumnStretch(1, 1)

        conv_layout.addLayout(res_grid)
        layout.addWidget(conv_group)

        layout.addStretch()

        # Status
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_convert.clicked.connect(self._on_convert)
        self.btn_clear.clicked.connect(self.clear_workspace)
        self.input_edit.returnPressed.connect(self._on_convert)

        self._update_current_time()

    def _update_current_time(self):
        now_ts = int(time.time())
        now_utc = datetime.now(timezone.utc)
        now_local = datetime.now().astimezone()

        self.lbl_current_unix.setText(str(now_ts))
        self.lbl_current_utc.setText(now_utc.strftime("%Y-%m-%d %H:%M:%S %Z"))
        self.lbl_current_local.setText(now_local.strftime("%Y-%m-%d %H:%M:%S %Z"))

    def _on_convert(self):
        text = self.input_edit.text().strip()
        if not text:
            self._set_status("No input provided", "error")
            return

        dt = None
        # Try parsing as timestamp (seconds or milliseconds)
        try:
            val = float(text)
            if val > 1e11:  # Likely milliseconds
                val = val / 1000.0
            dt = datetime.fromtimestamp(val, tz=timezone.utc)
        except ValueError:
            pass
        except (OSError, OverflowError):
            pass

        # Try parsing as date string
        if not dt:
            try:
                dt = dateutil.parser.parse(text)
                if dt.tzinfo is None:
                    # Assume UTC if no timezone provided
                    dt = dt.replace(tzinfo=timezone.utc)
            except Exception:
                pass

        if not dt:
            self._set_status("Could not parse input as timestamp or date", "error")
            self.res_unix.setText("—")
            self.res_unix_ms.setText("—")
            self.res_utc.setText("—")
            self.res_local.setText("—")
            return

        unix_s = int(dt.timestamp())
        unix_ms = int(dt.timestamp() * 1000)
        
        self.res_unix.setText(str(unix_s))
        self.res_unix_ms.setText(str(unix_ms))
        
        # Ensure dt has tzinfo for UTC display
        utc_dt = dt.astimezone(timezone.utc)
        local_dt = dt.astimezone()

        self.res_utc.setText(utc_dt.strftime("%Y-%m-%d %H:%M:%S %Z"))
        self.res_local.setText(local_dt.strftime("%Y-%m-%d %H:%M:%S %Z"))

        self._set_status("Converted successfully", "success")

    def _copy_and_status(self, text: str):
        if text and text != "—":
            self._copy_to_clipboard(text)
            self._set_status("Copied to clipboard", "info")

    def clear_workspace(self):
        self.input_edit.clear()
        self.res_unix.setText("—")
        self.res_unix_ms.setText("—")
        self.res_utc.setText("—")
        self.res_local.setText("—")
        self.status_label.clear()

    def get_result(self) -> str:
        return self.res_unix.text()
