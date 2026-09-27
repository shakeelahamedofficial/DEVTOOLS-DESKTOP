"""
DevTools Desktop — Application Views

Home overview dashboard, Settings view, and About view.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QGridLayout, QFrame, QPushButton, QComboBox, QCheckBox,
    QGroupBox, QSizePolicy
)

from app.core.branding import (
    PRODUCT_NAME, PRODUCT_TAGLINE, VERSION_STRING,
    COPYRIGHT_TEXT, LICENSE_TYPE, WEBSITE_URL
)
from app.core.tool_registry import ToolRegistry, ToolInfo
from app.core.theme import ThemeTokens, THEMES
from app.core.settings import SettingsManager


class HomeCard(QFrame):
    """Clickable card for a tool on the home dashboard."""

    clicked = Signal(str)

    def __init__(self, tool_info: ToolInfo, tokens: ThemeTokens, parent=None):
        super().__init__(parent)
        self.tool_id = tool_info.tool_id
        self._tokens = tokens

        self.setProperty("class", "card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(0)

        header = QHBoxLayout()
        self.icon_label = QLabel(tool_info.icon)
        self.icon_label.setStyleSheet(f"font-size: 20px; color: {tokens.accent_text}; background: transparent;")
        header.addWidget(self.icon_label)

        if tool_info.shortcut:
            shortcut = QLabel(tool_info.shortcut.replace("Ctrl+", "⌃"))
            shortcut.setProperty("class", "secondary")
            shortcut.setStyleSheet("font-size: 10px; background: transparent;")
            header.addStretch()
            header.addWidget(shortcut)

        layout.addLayout(header)
        layout.addStretch()

        name = QLabel(tool_info.name)
        name.setProperty("class", "heading")
        name.setStyleSheet("background: transparent;")
        layout.addWidget(name)

        layout.addSpacing(4)

        desc = QLabel(tool_info.description)
        desc.setProperty("class", "secondary")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 11px; background: transparent;")
        layout.addWidget(desc)

    def apply_theme(self, tokens: ThemeTokens):
        self._tokens = tokens
        self.icon_label.setStyleSheet(f"font-size: 20px; color: {tokens.accent_text}; background: transparent;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.tool_id)


class HomeView(QWidget):
    """Dashboard view."""

    tool_requested = Signal(str)

    def __init__(self, tokens: ThemeTokens, parent=None):
        super().__init__(parent)
        self.tokens = tokens
        self._all_cards = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(48, 48, 48, 48)
        container_layout.setSpacing(36)

        # Hero
        hero = QVBoxLayout()
        hero.setSpacing(8)

        title = QLabel(PRODUCT_NAME)
        title.setProperty("class", "hero")
        hero.addWidget(title)

        self.tagline = QLabel(PRODUCT_TAGLINE)
        self.tagline.setProperty("class", "title")
        self.tagline.setStyleSheet(f"color: {self.tokens.text_secondary}; font-weight: normal;")
        hero.addWidget(self.tagline)

        container_layout.addLayout(hero)

        # Recents (Optional)
        self.recents_layout = QVBoxLayout()
        self.recents_layout.setSpacing(16)

        recent_lbl = QLabel("Recent Tools")
        recent_lbl.setProperty("class", "heading")
        self.recents_layout.addWidget(recent_lbl)

        self.recent_grid = QGridLayout()
        self.recent_grid.setSpacing(16)
        self.recents_layout.addLayout(self.recent_grid)

        container_layout.addLayout(self.recents_layout)

        # All Tools
        all_layout = QVBoxLayout()
        all_layout.setSpacing(16)

        all_lbl = QLabel("All Tools")
        all_lbl.setProperty("class", "heading")
        all_layout.addWidget(all_lbl)

        grid = QGridLayout()
        grid.setSpacing(16)

        registry = ToolRegistry()
        tools = registry.all_tools()

        cols = 3
        for i, tool in enumerate(tools):
            card = HomeCard(tool, self.tokens)
            card.clicked.connect(self.tool_requested.emit)
            self._all_cards.append(card)
            row = i // cols
            col = i % cols
            grid.addWidget(card, row, col)

        # Add stretch columns if less than 3
        for i in range(cols):
            grid.setColumnStretch(i, 1)

        all_layout.addLayout(grid)
        container_layout.addLayout(all_layout)

        container_layout.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll)

    def refresh_recents(self):
        # Clear old
        while self.recent_grid.count():
            item = self.recent_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        settings = SettingsManager()
        recent_ids = settings.get_recent_tools()[:3]

        if not recent_ids:
            self.recents_layout.parentWidget().setVisible(False) if self.recents_layout.parentWidget() else None
            return

        registry = ToolRegistry()
        tools = []
        for tid in recent_ids:
            t = registry.get(tid)
            if t: tools.append(t)

        if not tools:
            return

        for i, tool in enumerate(tools):
            card = HomeCard(tool, self.tokens)
            card.clicked.connect(self.tool_requested.emit)
            self.recent_grid.addWidget(card, 0, i)

        for i in range(3):
            self.recent_grid.setColumnStretch(i, 1)

    def apply_theme(self, tokens: ThemeTokens):
        self.tokens = tokens
        self.tagline.setStyleSheet(f"color: {tokens.text_secondary}; font-weight: normal;")
        for card in self._all_cards:
            card.apply_theme(tokens)
        self.refresh_recents()


class SettingsView(QWidget):
    """Application settings view."""

    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = SettingsManager()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(28)

        title = QLabel("Settings")
        title.setProperty("class", "hero")
        layout.addWidget(title)

        subtitle = QLabel("Configure your DevTools Desktop experience")
        subtitle.setProperty("class", "secondary")
        layout.addWidget(subtitle)

        layout.addSpacing(4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(24)

        # ─── Appearance ───
        app_group = QGroupBox("Appearance")
        app_layout = QVBoxLayout(app_group)
        app_layout.setSpacing(16)

        theme_row = QHBoxLayout()
        theme_label = QLabel("Application Theme")
        theme_row.addWidget(theme_label)
        theme_row.addSpacing(16)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.settings.get_theme())
        self.theme_combo.setMinimumWidth(140)
        self.theme_combo.currentTextChanged.connect(self._on_theme_change)
        theme_row.addWidget(self.theme_combo)
        theme_row.addStretch()
        app_layout.addLayout(theme_row)

        theme_hint = QLabel("Choose between Dark and Light theme. Changes apply immediately.")
        theme_hint.setProperty("class", "secondary")
        theme_hint.setWordWrap(True)
        app_layout.addWidget(theme_hint)

        container_layout.addWidget(app_group)

        # ─── Behavior ───
        behav_group = QGroupBox("Behavior")
        behav_layout = QVBoxLayout(behav_group)
        behav_layout.setSpacing(16)

        self.chk_remember = QCheckBox("Remember last opened tool on startup")
        self.chk_remember.setChecked(self.settings.get_remember_last_tool())
        self.chk_remember.toggled.connect(self.settings.set_remember_last_tool)
        behav_layout.addWidget(self.chk_remember)

        container_layout.addWidget(behav_group)

        # ─── Data ───
        data_group = QGroupBox("Data & Privacy")
        data_layout = QVBoxLayout(data_group)
        data_layout.setSpacing(16)

        info = QLabel("All application data is stored locally on this machine.\n"
                       "No telemetry is collected. No data leaves your device.")
        info.setProperty("class", "secondary")
        info.setWordWrap(True)
        data_layout.addWidget(info)

        btn_clear = QPushButton("Clear Recent Tools History")
        btn_clear.clicked.connect(self._clear_history)
        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_clear)
        btn_row.addStretch()
        data_layout.addLayout(btn_row)

        container_layout.addWidget(data_group)

        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def _on_theme_change(self, theme: str):
        self.settings.set_theme(theme)
        self.theme_changed.emit(theme)

    def _clear_history(self):
        self.settings.clear_history()


class AboutView(QWidget):
    """About product view."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center_box = QVBoxLayout()
        center_box.setSpacing(12)
        center_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel(PRODUCT_NAME)
        title.setProperty("class", "hero")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_box.addWidget(title)

        version = QLabel(f"Version {VERSION_STRING}")
        version.setProperty("class", "title")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_box.addWidget(version)

        center_box.addSpacing(8)

        desc = QLabel(PRODUCT_TAGLINE)
        desc.setProperty("class", "secondary")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_box.addWidget(desc)

        center_box.addSpacing(24)

        copy = QLabel(COPYRIGHT_TEXT)
        copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_box.addWidget(copy)

        lic = QLabel(LICENSE_TYPE)
        lic.setProperty("class", "secondary")
        lic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_box.addWidget(lic)

        center_box.addSpacing(28)

        web = QLabel(f"<a href='{WEBSITE_URL}'>{WEBSITE_URL}</a>")
        web.setOpenExternalLinks(True)
        web.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_box.addWidget(web)

        layout.addLayout(center_box)
