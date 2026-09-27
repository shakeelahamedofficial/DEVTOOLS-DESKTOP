"""
DevTools Desktop — Sidebar Navigation

Professional sidebar with tool navigation, search, and keyboard support.
"""

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QSizePolicy,
)

from app.core.branding import PRODUCT_SHORT_NAME, VERSION_STRING
from app.core.tool_registry import ToolRegistry, ToolInfo
from app.core.theme import ThemeTokens, get_theme
from app.core.settings import SettingsManager


class SidebarItem(QPushButton):
    """A single sidebar navigation item."""

    def __init__(self, tool_info: ToolInfo, parent=None):
        super().__init__(parent)
        self.tool_info = tool_info
        self._active = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(36)
        self.setCheckable(True)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 10, 0)
        layout.setSpacing(10)

        # Icon
        self.icon_label = QLabel(tool_info.icon)
        self.icon_label.setFixedWidth(22)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.icon_label.font()
        font.setPointSize(9)
        self.icon_label.setFont(font)
        layout.addWidget(self.icon_label)

        # Name
        self.name_label = QLabel(tool_info.short_name)
        self.name_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self.name_label)

        # Shortcut hint
        if tool_info.shortcut:
            self.shortcut_label = QLabel(tool_info.shortcut.replace("Ctrl+", "⌃"))
            self.shortcut_label.setProperty("class", "secondary")
            font_s = self.shortcut_label.font()
            font_s.setPointSize(7)
            self.shortcut_label.setFont(font_s)
            layout.addWidget(self.shortcut_label)

    def set_active(self, active: bool) -> None:
        self._active = active
        self.setChecked(active)

    def apply_theme(self, tokens: ThemeTokens) -> None:
        active_bg = tokens.sidebar_item_active
        hover_bg = tokens.sidebar_item_hover
        text_color = tokens.text_primary
        text_sec = tokens.text_secondary
        accent = tokens.accent_text

        self.setStyleSheet(f"""
            SidebarItem {{
                background: transparent;
                border: none;
                border-radius: 6px;
                text-align: left;
            }}
            SidebarItem:hover {{
                background-color: {hover_bg};
            }}
            SidebarItem:checked {{
                background-color: {active_bg};
            }}
        """)
        self.name_label.setStyleSheet(f"color: {text_color}; font-size: 12px; background: transparent;")
        self.icon_label.setStyleSheet(f"color: {text_sec}; background: transparent;")
        if self._active:
            self.icon_label.setStyleSheet(f"color: {accent}; background: transparent;")
            self.name_label.setStyleSheet(f"color: {text_color}; font-size: 12px; font-weight: 500; background: transparent;")


class Sidebar(QWidget):
    """Application sidebar with navigation, search, and tool list."""

    tool_selected = Signal(str)
    settings_requested = Signal()
    about_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self._items: dict[str, SidebarItem] = {}
        self._current_tool: str = ""
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(210)
        self.setMinimumWidth(170)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 16, 10, 14)
        layout.setSpacing(2)

        # ─── Header ───
        header = QHBoxLayout()
        header.setContentsMargins(10, 0, 6, 0)
        title = QLabel(PRODUCT_SHORT_NAME.upper())
        title.setProperty("class", "heading")
        font = title.font()
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.5)
        font.setPointSize(9)
        font.setWeight(QFont.Weight.Bold)
        title.setFont(font)
        header.addWidget(title)
        header.addStretch()

        version_label = QLabel(f"v{VERSION_STRING}")
        version_label.setProperty("class", "secondary")
        vfont = version_label.font()
        vfont.setPointSize(7)
        version_label.setFont(vfont)
        header.addWidget(version_label)
        layout.addLayout(header)

        layout.addSpacing(12)

        # ─── Search ───
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tools…")
        self.search_input.setFixedHeight(32)
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._filter_tools)
        layout.addWidget(self.search_input)

        layout.addSpacing(8)

        # ─── Tool List ───
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.tool_list_widget = QWidget()
        self.tool_list_layout = QVBoxLayout(self.tool_list_widget)
        self.tool_list_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_list_layout.setSpacing(2)

        # Home item
        home_info = ToolInfo("home", "Overview", "Overview",
                             "Dashboard overview", "◉", category="nav")
        home_item = SidebarItem(home_info)
        home_item.clicked.connect(lambda: self._on_tool_clicked("home"))
        self._items["home"] = home_item
        self.tool_list_layout.addWidget(home_item)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setObjectName("sidebar_sep_top")
        self.tool_list_layout.addWidget(sep)

        # Tool items
        registry = ToolRegistry()
        for tool_info in registry.all_tools():
            item = SidebarItem(tool_info)
            item.clicked.connect(lambda checked, tid=tool_info.tool_id: self._on_tool_clicked(tid))
            self._items[tool_info.tool_id] = item
            self.tool_list_layout.addWidget(item)

        self.tool_list_layout.addStretch()
        scroll.setWidget(self.tool_list_widget)
        layout.addWidget(scroll, 1)

        # ─── Bottom Section ───
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFixedHeight(1)
        sep2.setObjectName("sidebar_sep_bottom")
        layout.addWidget(sep2)

        layout.addSpacing(6)

        # Settings
        settings_info = ToolInfo("settings", "Settings", "Settings",
                                 "Application settings", "⚙", category="nav")
        settings_item = SidebarItem(settings_info)
        settings_item.clicked.connect(lambda: self._on_tool_clicked("settings"))
        self._items["settings"] = settings_item
        layout.addWidget(settings_item)

        # About
        about_info = ToolInfo("about", "About", "About",
                              "About this application", "ℹ", category="nav")
        about_item = SidebarItem(about_info)
        about_item.clicked.connect(lambda: self._on_tool_clicked("about"))
        self._items["about"] = about_item
        layout.addWidget(about_item)

    def _on_tool_clicked(self, tool_id: str):
        self.set_active_tool(tool_id)
        self.tool_selected.emit(tool_id)

    def set_active_tool(self, tool_id: str):
        self._current_tool = tool_id
        for tid, item in self._items.items():
            item.set_active(tid == tool_id)

    def _filter_tools(self, text: str):
        query = text.lower().strip()
        registry = ToolRegistry()
        for tid, item in self._items.items():
            if tid in ("home", "settings", "about"):
                item.setVisible(not query or query in tid)
                continue
            tool_info = registry.get(tid)
            if tool_info:
                visible = (not query
                           or query in tool_info.name.lower()
                           or query in tool_info.short_name.lower()
                           or query in tool_info.description.lower())
                item.setVisible(visible)

    def apply_theme(self, tokens: ThemeTokens) -> None:
        self.setStyleSheet(f"""
            #Sidebar {{
                background-color: {tokens.sidebar_bg};
                border-right: 1px solid {tokens.border_subtle};
            }}
            #sidebar_sep_top, #sidebar_sep_bottom {{
                background-color: {tokens.sidebar_separator};
                border: none;
            }}
        """)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {tokens.bg_input};
                color: {tokens.text_primary};
                border: 1px solid {tokens.border_subtle};
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border-color: {tokens.border_focus};
            }}
            QLineEdit::placeholder {{
                color: {tokens.text_tertiary};
            }}
        """)
        for item in self._items.values():
            item.apply_theme(tokens)

    def focus_search(self):
        self.search_input.setFocus()
        self.search_input.selectAll()
