"""
DevTools Desktop — HTTP Tool Widget
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSplitter, QWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QProgressBar, QAbstractItemView
)

from app.tools.base_tool import ToolWidget
from app.tools.http_tool.logic import HttpRequest, HttpResponse, HttpWorker
from app.core.theme import ThemeTokens


class HttpToolWidget(ToolWidget):
    """HTTP Client for sending API requests."""

    def __init__(self, parent=None):
        super().__init__("http", "HTTP Client",
                         "Send HTTP requests and inspect responses", parent)
        self._worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("HTTP Client", "Test APIs and web services")
        layout.addLayout(header)

        # ─── Request Bar ───
        req_bar = QHBoxLayout()
        req_bar.setSpacing(8)

        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
        self.method_combo.setFixedWidth(100)
        req_bar.addWidget(self.method_combo)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://api.example.com/v1/resource")
        self.url_input.setMinimumHeight(36)
        req_bar.addWidget(self.url_input, 1)

        self.btn_send = self._make_button("Send", "primary")
        self.btn_send.setMinimumWidth(80)
        req_bar.addWidget(self.btn_send)
        
        self.btn_clear = self._make_button("Clear")
        req_bar.addWidget(self.btn_clear)
        
        layout.addLayout(req_bar)
        layout.addSpacing(16)

        # ─── Splitter ───
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Request Area
        req_container = QWidget()
        req_layout = QVBoxLayout(req_container)
        req_layout.setContentsMargins(0, 0, 0, 0)
        
        req_tabs = QTabWidget()
        
        # Headers Tab
        self.headers_table = QTableWidget(5, 2)
        self.headers_table.setHorizontalHeaderLabels(["Key", "Value"])
        self.headers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.headers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.headers_table.verticalHeader().setVisible(False)
        req_tabs.addTab(self.headers_table, "Headers")
        
        # Body Tab
        self.req_body = self._make_mono_edit("Request body (for POST/PUT/PATCH)...")
        req_tabs.addTab(self.req_body, "Body")
        
        req_layout.addWidget(req_tabs)
        splitter.addWidget(req_container)

        # Response Area
        res_container = QWidget()
        res_layout = QVBoxLayout(res_container)
        res_layout.setContentsMargins(0, 16, 0, 0)
        
        res_header_layout = QHBoxLayout()
        self.res_status = QLabel("Response")
        self.res_status.setProperty("class", "heading")
        res_header_layout.addWidget(self.res_status)
        
        self.progress = QProgressBar()
        self.progress.setMaximum(0)
        self.progress.setMinimum(0)
        self.progress.setVisible(False)
        res_header_layout.addWidget(self.progress)
        
        res_header_layout.addStretch()
        
        self.res_meta = QLabel("")
        self.res_meta.setProperty("class", "secondary")
        res_header_layout.addWidget(self.res_meta)
        
        res_layout.addLayout(res_header_layout)
        res_layout.addSpacing(8)
        
        res_tabs = QTabWidget()
        
        # Res Body Tab
        self.res_body = self._make_mono_edit("Response will appear here...", read_only=True)
        res_tabs.addTab(self.res_body, "Body")
        
        # Res Headers Tab
        self.res_headers_table = QTableWidget(0, 2)
        self.res_headers_table.setHorizontalHeaderLabels(["Key", "Value"])
        self.res_headers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.res_headers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.res_headers_table.verticalHeader().setVisible(False)
        self.res_headers_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        res_tabs.addTab(self.res_headers_table, "Headers")
        
        res_layout.addWidget(res_tabs)
        splitter.addWidget(res_container)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter, 1)

        # Status & Notice
        layout.addSpacing(12)
        notice = QLabel("⚠ Do not enter sensitive credentials unless communicating with trusted endpoints.")
        notice.setProperty("class", "notice")
        layout.addWidget(notice)

        layout.addSpacing(4)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.btn_send.clicked.connect(self._on_send)
        self.url_input.returnPressed.connect(self._on_send)
        self.btn_clear.clicked.connect(self.clear_workspace)

    def _get_request_headers(self) -> dict:
        headers = {}
        for row in range(self.headers_table.rowCount()):
            key_item = self.headers_table.item(row, 0)
            val_item = self.headers_table.item(row, 1)
            
            if key_item and key_item.text().strip():
                key = key_item.text().strip()
                val = val_item.text().strip() if val_item else ""
                headers[key] = val
        return headers

    def _on_send(self):
        url = self.url_input.text().strip()
        if not url:
            self._set_status("URL is required", "error")
            return
            
        method = self.method_combo.currentText()
        headers = self._get_request_headers()
        body = self.req_body.toPlainText()
        
        req = HttpRequest(method, url, headers, body)
        
        self.btn_send.setEnabled(False)
        self.progress.setVisible(True)
        self.res_status.setText("Sending...")
        self.res_meta.setText("")
        self.res_body.clear()
        self.res_headers_table.setRowCount(0)
        self._set_status("Sending request...", "info")
        
        # Run in background
        self._worker = HttpWorker(req)
        self._worker.finished.connect(self._on_response)
        self._worker.start()

    def _on_response(self, res: HttpResponse):
        self.btn_send.setEnabled(True)
        self.progress.setVisible(False)
        self._worker = None
        
        if not res.success:
            self.res_status.setText("Error")
            if self._tokens:
                self.res_status.setStyleSheet(f"color: {self._tokens.status_error}; font-weight: bold;")
            self.res_body.setPlainText(res.error_message)
            self._set_status(f"Request failed ({res.time_ms}ms)", "error")
            return
            
        # Display Status
        status_text = f"{res.status_code} {res.status_reason}"
        self.res_status.setText(status_text)
        
        if self._tokens:
            if 200 <= res.status_code < 300:
                color = self._tokens.status_success
            elif 300 <= res.status_code < 400:
                color = self._tokens.status_warning
            else:
                color = self._tokens.status_error
            self.res_status.setStyleSheet(f"color: {color}; font-weight: bold;")
            
        # Meta info
        self.res_meta.setText(f"{res.time_ms} ms  |  {res.size_bytes:,} bytes")
        
        # Body
        self.res_body.setPlainText(res.body)
        
        # Headers
        if res.headers:
            self.res_headers_table.setRowCount(len(res.headers))
            for i, (k, v) in enumerate(res.headers.items()):
                self.res_headers_table.setItem(i, 0, QTableWidgetItem(k))
                self.res_headers_table.setItem(i, 1, QTableWidgetItem(v))
                
        self._set_status("Request completed", "success")

    def clear_workspace(self):
        self.url_input.clear()
        self.req_body.clear()
        self.headers_table.clearContents()
        self.res_body.clear()
        self.res_headers_table.setRowCount(0)
        self.res_status.setText("Response")
        self.res_status.setStyleSheet("")
        self.res_meta.setText("")
        self.status_label.clear()

    def get_result(self) -> str:
        return self.res_body.toPlainText()

    def apply_theme(self, tokens: ThemeTokens):
        super().apply_theme(tokens)
        if self.res_status.text() not in ("Response", "Sending...", "Error"):
            self.res_status.setStyleSheet(f"color: {tokens.text_primary}; font-weight: bold;")
        elif self.res_status.text() == "Error":
            self.res_status.setStyleSheet(f"color: {tokens.status_error}; font-weight: bold;")
