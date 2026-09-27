"""
DevTools Desktop — Main Window
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget,
    QSplitter, QApplication
)

from app.core.branding import PRODUCT_NAME
from app.core.settings import SettingsManager
from app.core.theme import get_theme, generate_stylesheet, ThemeTokens
from app.core.tool_registry import ToolRegistry

from app.ui.sidebar import Sidebar
from app.ui.command_palette import CommandPalette
from app.ui.views import HomeView, SettingsView, AboutView


class MainWindow(QMainWindow):
    """Main application window container."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.registry = ToolRegistry()
        self.current_theme: ThemeTokens = None
        self._tools = {}
        
        self.setWindowTitle(PRODUCT_NAME)
        self.setMinimumSize(900, 600)
        
        self._setup_ui()
        self._setup_shortcuts()
        self._restore_state()
        self._apply_theme(self.settings.get_theme())
        
        # Load startup tool
        if self.settings.get_remember_last_tool():
            last = self.settings.get_last_tool()
            self._switch_tool(last)
        else:
            self._switch_tool("home")

    def _setup_ui(self):
        # Main Layout (Splitter)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.tool_selected.connect(self._switch_tool)
        self.splitter.addWidget(self.sidebar)
        
        # Stacked Content
        self.content_stack = QStackedWidget()
        self.splitter.addWidget(self.content_stack)
        
        # Set splitter sizes
        self.splitter.setSizes([self.settings.get_sidebar_width(), 800])
        self.splitter.splitterMoved.connect(self._save_sidebar_width)
        self.splitter.setCollapsible(0, False)
        
        # Load Views
        self.home_view = HomeView(get_theme(self.settings.get_theme()))
        self.home_view.tool_requested.connect(self._switch_tool)
        self.content_stack.addWidget(self.home_view)
        
        self.settings_view = SettingsView()
        self.settings_view.theme_changed.connect(self._apply_theme)
        self.content_stack.addWidget(self.settings_view)
        
        self.about_view = AboutView()
        self.content_stack.addWidget(self.about_view)
        
        # Load Tools
        for tool_info in self.registry.all_tools():
            if tool_info.widget_class:
                widget = tool_info.widget_class()
                self._tools[tool_info.tool_id] = widget
                self.content_stack.addWidget(widget)

    def _setup_shortcuts(self):
        # Command Palette
        sc_palette = QShortcut(QKeySequence("Ctrl+K"), self)
        sc_palette.activated.connect(self._show_command_palette)
        
        # Search focus
        sc_search = QShortcut(QKeySequence("Ctrl+L"), self)
        sc_search.activated.connect(self.sidebar.focus_search)
        
        # Action shortcuts globally available if a tool is active
        sc_copy = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        sc_copy.activated.connect(self._action_copy)
        
        sc_clear = QShortcut(QKeySequence("Ctrl+Shift+X"), self)
        sc_clear.activated.connect(self._action_clear)

    def _apply_theme(self, theme_name: str):
        """Central theme propagation — single mechanism for entire app."""
        tokens = get_theme(theme_name)
        self.current_theme = tokens
        
        # Apply global stylesheet to root window — cascades to ALL child widgets
        style = generate_stylesheet(tokens)
        self.setStyleSheet(style)
        
        # Apply to components that need programmatic style updates
        # (inline styles that use dynamic token values)
        self.sidebar.apply_theme(tokens)
        self.home_view.apply_theme(tokens)
        
        # Apply theme to all loaded tool widgets
        for widget in self._tools.values():
            if hasattr(widget, 'apply_theme'):
                widget.apply_theme(tokens)

    def _switch_tool(self, tool_id: str):
        if tool_id == "home":
            self.home_view.refresh_recents()
            self.content_stack.setCurrentWidget(self.home_view)
        elif tool_id == "settings":
            self.content_stack.setCurrentWidget(self.settings_view)
        elif tool_id == "about":
            self.content_stack.setCurrentWidget(self.about_view)
        elif tool_id in self._tools:
            self.content_stack.setCurrentWidget(self._tools[tool_id])
            self.settings.add_recent_tool(tool_id)
        
        self.sidebar.set_active_tool(tool_id)
        self.settings.set_last_tool(tool_id)

    def _show_command_palette(self):
        palette = CommandPalette(self)
        palette.apply_theme(self.current_theme)
        palette.tool_selected.connect(self._switch_tool)
        palette.action_triggered.connect(self._handle_action)
        palette.show()

    def _handle_action(self, action: str):
        if action == "toggle_theme":
            current = self.settings.get_theme()
            new_theme = "light" if current == "dark" else "dark"
            self.settings.set_theme(new_theme)
            self.settings_view.theme_combo.setCurrentText(new_theme)
            self._apply_theme(new_theme)
        elif action == "clear":
            self._action_clear()
        elif action == "copy_result":
            self._action_copy()

    def _action_clear(self):
        current_widget = self.content_stack.currentWidget()
        if hasattr(current_widget, 'clear_workspace'):
            current_widget.clear_workspace()

    def _action_copy(self):
        current_widget = self.content_stack.currentWidget()
        if hasattr(current_widget, 'get_result'):
            res = current_widget.get_result()
            if res:
                QApplication.clipboard().setText(res)

    def _save_sidebar_width(self, pos, index):
        if index == 1:
            self.settings.set_sidebar_width(self.splitter.sizes()[0])

    def _restore_state(self):
        geom = self.settings.get_window_geometry()
        if geom:
            self.restoreGeometry(geom)
        state = self.settings.get_window_state()
        if state:
            self.restoreState(state)

    def closeEvent(self, event):
        self.settings.set_window_geometry(self.saveGeometry())
        self.settings.set_window_state(self.saveState())
        super().closeEvent(event)
