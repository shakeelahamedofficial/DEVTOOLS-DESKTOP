"""
DevTools Desktop — Settings Manager

Persistent local settings using QSettings.
No telemetry, no cloud sync. Purely local preferences.
"""

import json
from typing import Any, List, Optional

from PySide6.QtCore import QSettings

from app.core.branding import APPLICATION_ID, PRODUCT_NAME


class SettingsManager:
    """Manages application settings with QSettings backend."""

    _instance: Optional["SettingsManager"] = None

    def __new__(cls) -> "SettingsManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = QSettings(APPLICATION_ID, PRODUCT_NAME)
        return cls._instance

    @property
    def settings(self) -> QSettings:
        return self._settings

    # ─── Theme ───
    def get_theme(self) -> str:
        return self._settings.value("appearance/theme", "dark")

    def set_theme(self, theme: str) -> None:
        self._settings.setValue("appearance/theme", theme)

    # ─── Behavior ───
    def get_start_page(self) -> str:
        return self._settings.value("behavior/start_page", "home")

    def set_start_page(self, page: str) -> None:
        self._settings.setValue("behavior/start_page", page)

    def get_remember_last_tool(self) -> bool:
        return self._settings.value("behavior/remember_last_tool", False, type=bool)

    def set_remember_last_tool(self, val: bool) -> None:
        self._settings.setValue("behavior/remember_last_tool", val)

    def get_confirm_clear(self) -> bool:
        return self._settings.value("behavior/confirm_clear", True, type=bool)

    def set_confirm_clear(self, val: bool) -> None:
        self._settings.setValue("behavior/confirm_clear", val)

    # ─── Last Tool ───
    def get_last_tool(self) -> str:
        return self._settings.value("state/last_tool", "home")

    def set_last_tool(self, tool_id: str) -> None:
        self._settings.setValue("state/last_tool", tool_id)

    # ─── Recent Tools ───
    def get_recent_tools(self) -> List[str]:
        raw = self._settings.value("state/recent_tools", "[]")
        if isinstance(raw, list):
            return raw
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return []

    def add_recent_tool(self, tool_id: str) -> None:
        recents = self.get_recent_tools()
        if tool_id in recents:
            recents.remove(tool_id)
        recents.insert(0, tool_id)
        recents = recents[:10]
        self._settings.setValue("state/recent_tools", json.dumps(recents))

    # ─── Window Geometry ───
    def get_window_geometry(self) -> Optional[bytes]:
        return self._settings.value("ui/window_geometry")

    def set_window_geometry(self, geometry: bytes) -> None:
        self._settings.setValue("ui/window_geometry", geometry)

    def get_window_state(self) -> Optional[bytes]:
        return self._settings.value("ui/window_state")

    def set_window_state(self, state: bytes) -> None:
        self._settings.setValue("ui/window_state", state)

    def get_sidebar_width(self) -> int:
        return self._settings.value("ui/sidebar_width", 200, type=int)

    def set_sidebar_width(self, width: int) -> None:
        self._settings.setValue("ui/sidebar_width", width)

    # ─── Generic ───
    def get(self, key: str, default: Any = None, value_type: type = None) -> Any:
        if value_type:
            return self._settings.value(key, default, type=value_type)
        return self._settings.value(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings.setValue(key, value)

    # ─── Data Management ───
    def reset_all(self) -> None:
        """Clear all settings."""
        self._settings.clear()

    def clear_history(self) -> None:
        """Clear usage history only."""
        self._settings.remove("state/recent_tools")
        self._settings.remove("state/last_tool")
