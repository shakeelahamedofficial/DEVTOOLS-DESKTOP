"""
DevTools Desktop — Tool Registry

Defines the tool metadata and provides a registry for all tools.
New tools are added by registering them here.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Type

from PySide6.QtWidgets import QWidget


@dataclass
class ToolInfo:
    """Metadata for a registered tool."""
    tool_id: str
    name: str
    short_name: str
    description: str
    icon: str  # Unicode emoji/symbol as icon
    shortcut: Optional[str] = None
    category: str = "tools"
    widget_class: Optional[Type[QWidget]] = None


class ToolRegistry:
    """Central registry of all available tools."""

    _instance: Optional["ToolRegistry"] = None

    def __new__(cls) -> "ToolRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: Dict[str, ToolInfo] = {}
            cls._instance._order: List[str] = []
        return cls._instance

    def register(self, info: ToolInfo) -> None:
        """Register a tool."""
        self._tools[info.tool_id] = info
        if info.tool_id not in self._order:
            self._order.append(info.tool_id)

    def get(self, tool_id: str) -> Optional[ToolInfo]:
        """Get tool info by ID."""
        return self._tools.get(tool_id)

    def all_tools(self) -> List[ToolInfo]:
        """Get all tools in registration order."""
        return [self._tools[tid] for tid in self._order if tid in self._tools]

    def search(self, query: str) -> List[ToolInfo]:
        """Search tools by name, description, or ID."""
        q = query.lower().strip()
        if not q:
            return self.all_tools()
        results = []
        for tool in self.all_tools():
            if (q in tool.name.lower()
                    or q in tool.short_name.lower()
                    or q in tool.description.lower()
                    or q in tool.tool_id.lower()):
                results.append(tool)
        return results

    def tool_ids(self) -> List[str]:
        """Get all tool IDs in order."""
        return list(self._order)


def register_all_tools() -> None:
    """Register all built-in tools."""
    registry = ToolRegistry()

    from app.tools.json_tool.widget import JsonToolWidget
    from app.tools.jwt_tool.widget import JwtToolWidget
    from app.tools.base64_tool.widget import Base64ToolWidget
    from app.tools.url_tool.widget import UrlToolWidget
    from app.tools.uuid_tool.widget import UuidToolWidget
    from app.tools.hash_tool.widget import HashToolWidget
    from app.tools.timestamp_tool.widget import TimestampToolWidget
    from app.tools.regex_tool.widget import RegexToolWidget
    from app.tools.sql_tool.widget import SqlToolWidget
    from app.tools.http_tool.widget import HttpToolWidget

    tools = [
        ToolInfo("json", "JSON Formatter", "JSON",
                 "Format, minify, and validate JSON",
                 "{ }", "Ctrl+1", widget_class=JsonToolWidget),
        ToolInfo("jwt", "JWT Decoder", "JWT",
                 "Decode and inspect JWT tokens",
                 "🔑", "Ctrl+2", widget_class=JwtToolWidget),
        ToolInfo("base64", "Base64 Encoder", "Base64",
                 "Encode and decode Base64",
                 "⇄", "Ctrl+3", widget_class=Base64ToolWidget),
        ToolInfo("url", "URL Encoder", "URL",
                 "URL encode and decode strings",
                 "🔗", "Ctrl+4", widget_class=UrlToolWidget),
        ToolInfo("uuid", "UUID Generator", "UUID",
                 "Generate UUIDs in bulk",
                 "⬡", "Ctrl+5", widget_class=UuidToolWidget),
        ToolInfo("hash", "Hash Generator", "Hash",
                 "Generate cryptographic hashes",
                 "#", "Ctrl+6", widget_class=HashToolWidget),
        ToolInfo("timestamp", "Timestamp Converter", "Time",
                 "Convert between Unix timestamps and dates",
                 "⏱", "Ctrl+7", widget_class=TimestampToolWidget),
        ToolInfo("regex", "Regex Tester", "Regex",
                 "Test and debug regular expressions",
                 ".*", "Ctrl+8", widget_class=RegexToolWidget),
        ToolInfo("sql", "SQL Formatter", "SQL",
                 "Format and minify SQL queries",
                 "⊞", "Ctrl+9", widget_class=SqlToolWidget),
        ToolInfo("http", "HTTP Client", "HTTP",
                 "Send HTTP requests and inspect responses",
                 "⇌", "Ctrl+0", widget_class=HttpToolWidget),
    ]

    for tool in tools:
        registry.register(tool)
