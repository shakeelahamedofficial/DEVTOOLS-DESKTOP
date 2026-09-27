"""
DevTools Desktop — Regex Tool Widget
"""

import re
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QCheckBox, QSplitter, QWidget,
    QTreeWidget, QTreeWidgetItem
)

from app.tools.base_tool import ToolWidget
from app.tools.regex_tool.logic import test_regex
from app.core.theme import ThemeTokens


class RegexToolWidget(ToolWidget):
    """Regular Expression tester."""

    def __init__(self, parent=None):
        super().__init__("regex", "Regex Tester",
                         "Test and debug regular expressions", parent)
        self._setup_ui()
        
        # Debounce timer for live testing
        self._test_timer = QTimer(self)
        self._test_timer.setSingleShot(True)
        self._test_timer.timeout.connect(self._run_test)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.CONTENT_MARGINS)
        layout.setSpacing(0)

        header = self._make_section_header("Regex Tester", "Test and debug regular expressions")
        layout.addLayout(header)

        # ─── Inputs ───
        input_area = QVBoxLayout()
        input_area.setSpacing(12)

        # Pattern
        pat_row = QHBoxLayout()
        pat_lbl = QLabel("Pattern:")
        pat_lbl.setFixedWidth(60)
        pat_row.addWidget(pat_lbl)
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("e.g. ^[a-z]+$")
        self.pattern_input.setFont(self._make_mono_edit().font())
        pat_row.addWidget(self.pattern_input, 1)
        input_area.addLayout(pat_row)

        # Replacement (Optional)
        rep_row = QHBoxLayout()
        rep_lbl = QLabel("Replace:")
        rep_lbl.setFixedWidth(60)
        rep_row.addWidget(rep_lbl)
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Optional replacement string...")
        self.replace_input.setFont(self._make_mono_edit().font())
        rep_row.addWidget(self.replace_input, 1)
        input_area.addLayout(rep_row)

        # Flags
        flags_row = QHBoxLayout()
        self.chk_ignorecase = QCheckBox("Ignore Case (i)")
        self.chk_multiline = QCheckBox("Multiline (m)")
        self.chk_dotall = QCheckBox("Dot All (s)")
        
        self.btn_clear = self._make_button("Clear")
        
        flags_row.addWidget(self.chk_ignorecase)
        flags_row.addWidget(self.chk_multiline)
        flags_row.addWidget(self.chk_dotall)
        flags_row.addStretch()
        flags_row.addWidget(self.btn_clear)
        input_area.addLayout(flags_row)

        layout.addLayout(input_area)
        layout.addSpacing(24)

        # ─── Splitter ───
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Test Text
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(8)
        
        text_label = QLabel("Test String")
        text_label.setProperty("class", "secondary")
        text_layout.addWidget(text_label)
        
        self.test_edit = self._make_mono_edit("Enter test string here...")
        text_layout.addWidget(self.test_edit)
        splitter.addWidget(text_container)

        # Results Area (Groups & Replacement)
        res_container = QWidget()
        res_layout = QVBoxLayout(res_container)
        res_layout.setContentsMargins(0, 16, 0, 0)
        res_layout.setSpacing(8)
        
        res_label = QLabel("Match Information & Replacement")
        res_label.setProperty("class", "secondary")
        res_layout.addWidget(res_label)
        
        # Results split horizontally
        h_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Matches Tree
        self.matches_tree = QTreeWidget()
        self.matches_tree.setHeaderLabels(["Match / Group", "Value", "Pos"])
        self.matches_tree.setAlternatingRowColors(True)
        h_splitter.addWidget(self.matches_tree)
        
        # Replacement output
        self.rep_output = self._make_mono_edit("Replacement result will appear here...", read_only=True)
        h_splitter.addWidget(self.rep_output)
        
        h_splitter.setStretchFactor(0, 1)
        h_splitter.setStretchFactor(1, 1)
        res_layout.addWidget(h_splitter)
        
        splitter.addWidget(res_container)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter, 1)

        # Status
        layout.addSpacing(12)
        self.status_label = self._make_status_label()
        layout.addWidget(self.status_label)

        # Connect
        self.pattern_input.textChanged.connect(self._schedule_test)
        self.replace_input.textChanged.connect(self._schedule_test)
        self.test_edit.textChanged.connect(self._schedule_test)
        self.chk_ignorecase.stateChanged.connect(self._schedule_test)
        self.chk_multiline.stateChanged.connect(self._schedule_test)
        self.chk_dotall.stateChanged.connect(self._schedule_test)
        self.btn_clear.clicked.connect(self.clear_workspace)

    def _schedule_test(self):
        self._test_timer.start(200)

    def _get_flags(self) -> int:
        flags = 0
        if self.chk_ignorecase.isChecked():
            flags |= re.IGNORECASE
        if self.chk_multiline.isChecked():
            flags |= re.MULTILINE
        if self.chk_dotall.isChecked():
            flags |= re.DOTALL
        return flags

    def _run_test(self):
        pattern = self.pattern_input.text()
        text = self.test_edit.toPlainText()
        replace_pat = self.replace_input.text()
        
        # Clear highlights
        cursor = self.test_edit.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(Qt.GlobalColor.transparent)
        cursor.setCharFormat(fmt)
        
        self.matches_tree.clear()
        self.rep_output.clear()
        
        if not pattern:
            self.status_label.clear()
            return
            
        result = test_regex(pattern, text, self._get_flags(), replace_pat)
        
        if not result.success:
            self._set_status(f"Error: {result.error_message} - {result.error_detail}", "error")
            return
            
        matches = result.matches
        if not matches:
            self._set_status("No matches found", "info")
            return
            
        # Highlight matches and populate tree
        cursor = QTextCursor(self.test_edit.document())
        
        highlight_fmt = QTextCharFormat()
        if self._tokens:
            highlight_fmt.setBackground(QColor(self._tokens.accent_muted))
        else:
            highlight_fmt.setBackground(QColor(0, 120, 215, 64))
            
        for i, match in enumerate(matches):
            # Highlight
            cursor.setPosition(match.start)
            cursor.setPosition(match.end, QTextCursor.MoveMode.KeepAnchor)
            cursor.setCharFormat(highlight_fmt)
            
            # Tree Item
            match_item = QTreeWidgetItem(self.matches_tree)
            match_item.setText(0, f"Match {i+1}")
            match_item.setText(1, match.full_match)
            match_item.setText(2, f"{match.start}-{match.end}")
            
            # Groups
            for j, grp in enumerate(match.groups):
                grp_item = QTreeWidgetItem(match_item)
                grp_item.setText(0, f"Group {j+1}")
                grp_item.setText(1, grp if grp is not None else "")
                
            # Named Groups
            for name, val in match.named_groups.items():
                name_item = QTreeWidgetItem(match_item)
                name_item.setText(0, f"Name: {name}")
                name_item.setText(1, val if val is not None else "")
                
        self.matches_tree.expandAll()
        
        if replace_pat:
            self.rep_output.setPlainText(result.replacement)
            
        count_str = "1000+ (limited)" if len(matches) == 1000 else str(len(matches))
        self._set_status(f"Found {count_str} match(es)", "success")

    def clear_workspace(self):
        self.pattern_input.clear()
        self.replace_input.clear()
        self.test_edit.clear()
        self.matches_tree.clear()
        self.rep_output.clear()
        self.status_label.clear()

    def get_result(self) -> str:
        return self.rep_output.toPlainText()
