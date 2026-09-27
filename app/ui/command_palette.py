"""
DevTools Desktop — Command Palette

Global command palette (Ctrl+K) for quick tool/action access.
"""

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QKeyEvent, QFont
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QWidget, QFrame,
    QGraphicsDropShadowEffect, QApplication,
)

from app.core.tool_registry import ToolRegistry, ToolInfo
from app.core.theme import ThemeTokens


class CommandPaletteItem(QWidget):
    """Single item in the command palette."""

    def __init__(self, icon: str, name: str, description: str,
                 shortcut: str = "", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setFixedWidth(24)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(1)
        text_layout.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(name)
        name_label.setObjectName("palette_name")
        text_layout.addWidget(name_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setObjectName("palette_desc")
            desc_label.setProperty("class", "secondary")
            text_layout.addWidget(desc_label)

        layout.addLayout(text_layout, 1)

        if shortcut:
            sc_label = QLabel(shortcut)
            sc_label.setObjectName("palette_shortcut")
            sc_label.setProperty("class", "secondary")
            layout.addWidget(sc_label)


class CommandPalette(QDialog):
    """Global command palette dialog."""

    tool_selected = Signal(str)
    action_triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.Popup
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(540)
        self.setMaximumHeight(440)

        self._actions = [
            ("action:toggle_theme", "🎨", "Toggle Theme", "Switch dark/light", ""),
            ("action:clear", "🗑", "Clear Workspace", "Clear current tool input", "Ctrl+Shift+X"),
            ("action:copy_result", "📋", "Copy Result", "Copy output to clipboard", "Ctrl+Shift+C"),
        ]

        self._setup_ui()

    def _setup_ui(self):
        # Container with border
        self.container = QFrame(self)
        self.container.setObjectName("palette_container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tools and actions…")
        self.search_input.setObjectName("palette_search")
        self.search_input.setFixedHeight(48)
        self.search_input.textChanged.connect(self._on_search)
        self.search_input.installEventFilter(self)
        container_layout.addWidget(self.search_input)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setObjectName("palette_sep")
        container_layout.addWidget(sep)

        # Results list
        self.results_list = QListWidget()
        self.results_list.setObjectName("palette_results")
        self.results_list.setFrameShape(QFrame.Shape.NoFrame)
        self.results_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.results_list.itemClicked.connect(self._on_item_clicked)
        self.results_list.itemDoubleClicked.connect(self._on_item_clicked)
        container_layout.addWidget(self.results_list)

        self._populate_results("")

    def _populate_results(self, query: str):
        self.results_list.clear()
        registry = ToolRegistry()

        # Tools
        tools = registry.search(query)
        for tool in tools:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, f"tool:{tool.tool_id}")
            widget = CommandPaletteItem(
                tool.icon, tool.name, tool.description,
                tool.shortcut or ""
            )
            item.setSizeHint(widget.sizeHint())
            self.results_list.addItem(item)
            self.results_list.setItemWidget(item, widget)

        # Actions
        q = query.lower()
        for action_id, icon, name, desc, shortcut in self._actions:
            if q and q not in name.lower() and q not in desc.lower():
                continue
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, action_id)
            widget = CommandPaletteItem(icon, name, desc, shortcut)
            item.setSizeHint(widget.sizeHint())
            self.results_list.addItem(item)
            self.results_list.setItemWidget(item, widget)

        if self.results_list.count() > 0:
            self.results_list.setCurrentRow(0)

        # Adjust height
        total_height = 50  # search bar + separator
        for i in range(min(self.results_list.count(), 8)):
            total_height += self.results_list.sizeHintForRow(i)
        total_height = min(total_height + 10, 440)
        self.setFixedHeight(total_height)

    def _on_search(self, text: str):
        self._populate_results(text)

    def _on_item_clicked(self, item: QListWidgetItem):
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            if data.startswith("tool:"):
                self.tool_selected.emit(data.replace("tool:", ""))
            elif data.startswith("action:"):
                self.action_triggered.emit(data.replace("action:", ""))
            self.close()

    def eventFilter(self, obj, event):
        if obj == self.search_input and isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_Down:
                self.results_list.setFocus()
                if self.results_list.count() > 0:
                    row = self.results_list.currentRow()
                    self.results_list.setCurrentRow(min(row + 1, self.results_list.count() - 1))
                return True
            elif event.key() == Qt.Key.Key_Up:
                self.results_list.setFocus()
                if self.results_list.count() > 0:
                    row = self.results_list.currentRow()
                    self.results_list.setCurrentRow(max(row - 1, 0))
                return True
            elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                current = self.results_list.currentItem()
                if current:
                    self._on_item_clicked(current)
                return True
            elif event.key() == Qt.Key.Key_Escape:
                self.close()
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            return
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            current = self.results_list.currentItem()
            if current:
                self._on_item_clicked(current)
            return
        # Forward typing to search
        if event.text() and event.text().isprintable():
            self.search_input.setFocus()
            self.search_input.setText(self.search_input.text() + event.text())
            return
        super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.search_input.clear()
        self.search_input.setFocus()
        self._populate_results("")

        # Center on parent
        if self.parent():
            parent = self.parent()
            pw = parent.width()
            x = (pw - self.width()) // 2
            y = max(parent.height() // 5, 60)
            global_pos = parent.mapToGlobal(parent.rect().topLeft())
            self.move(global_pos.x() + x, global_pos.y() + y)

    def apply_theme(self, tokens: ThemeTokens) -> None:
        self.container.setStyleSheet(f"""
            #palette_container {{
                background-color: {tokens.palette_bg};
                border: 1px solid {tokens.palette_border};
                border-radius: 10px;
            }}
            #palette_search {{
                background: transparent;
                color: {tokens.text_primary};
                border: none;
                padding: 0 18px;
                font-size: 15px;
            }}
            #palette_search::placeholder {{
                color: {tokens.text_tertiary};
            }}
            #palette_sep {{
                background-color: {tokens.border_subtle};
                border: none;
            }}
            #palette_results {{
                background: transparent;
                border: none;
                padding: 6px;
            }}
            #palette_results::item {{
                border-radius: 6px;
                padding: 0;
            }}
            #palette_results::item:selected {{
                background-color: {tokens.palette_item_hover};
            }}
            #palette_results::item:hover {{
                background-color: {tokens.palette_item_hover};
            }}
            #palette_name {{
                color: {tokens.text_primary};
                font-size: 13px;
                font-weight: 500;
                background: transparent;
            }}
            #palette_desc {{
                color: {tokens.text_secondary};
                font-size: 11px;
                background: transparent;
            }}
            #palette_shortcut {{
                color: {tokens.text_tertiary};
                font-size: 11px;
                font-family: {tokens.font_mono};
                background: transparent;
            }}
            QLabel {{
                background: transparent;
            }}
        """)
