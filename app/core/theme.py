"""
DevTools Desktop — Theme System

Centralized design tokens and theme management.
Supports Dark, Light, and extensible branded themes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class ThemeMode(Enum):
    DARK = "dark"
    LIGHT = "light"
    SYSTEM = "system"


@dataclass
class ThemeTokens:
    """Complete set of design tokens for a theme."""
    # Backgrounds
    bg_primary: str = "#0A0A0A"
    bg_surface: str = "#111315"
    bg_elevated: str = "#181B1F"
    bg_hover: str = "#1E2227"
    bg_active: str = "#252A30"
    bg_input: str = "#0E1012"

    # Borders
    border_default: str = "#282C31"
    border_subtle: str = "#1E2227"
    border_strong: str = "#3A3F46"
    border_focus: str = "#4FC6E0"

    # Text
    text_primary: str = "#F5F7FA"
    text_secondary: str = "#9AA3AD"
    text_tertiary: str = "#6B7380"
    text_disabled: str = "#4A4F56"
    text_inverse: str = "#0A0A0A"

    # Accent
    accent: str = "#4FC6E0"
    accent_hover: str = "#6DD3E8"
    accent_muted: str = "#1A3A44"
    accent_text: str = "#4FC6E0"

    # Status
    status_success: str = "#34D399"
    status_success_bg: str = "#0D2B1F"
    status_warning: str = "#FBBF24"
    status_warning_bg: str = "#2B2410"
    status_error: str = "#F87171"
    status_error_bg: str = "#2B1010"
    status_info: str = "#60A5FA"
    status_info_bg: str = "#0F1B2B"

    # Scrollbar
    scrollbar_bg: str = "transparent"
    scrollbar_handle: str = "#282C31"
    scrollbar_handle_hover: str = "#3A3F46"

    # Sidebar
    sidebar_bg: str = "#0D0F11"
    sidebar_item_hover: str = "#181B1F"
    sidebar_item_active: str = "#1A2830"
    sidebar_separator: str = "#1E2227"

    # Command palette
    palette_bg: str = "#151719"
    palette_border: str = "#282C31"
    palette_item_hover: str = "#1E2227"

    # Toolbar
    toolbar_bg: str = "#111315"

    # Code / monospace areas
    code_bg: str = "#0C0E10"
    code_text: str = "#E2E8F0"
    code_keyword: str = "#7DD3FC"
    code_string: str = "#86EFAC"
    code_number: str = "#FDE68A"
    code_comment: str = "#6B7380"

    # Button
    btn_primary_bg: str = "#4FC6E0"
    btn_primary_text: str = "#0A0A0A"
    btn_primary_hover: str = "#6DD3E8"
    btn_secondary_bg: str = "#181B1F"
    btn_secondary_text: str = "#F5F7FA"
    btn_secondary_hover: str = "#252A30"
    btn_secondary_border: str = "#282C31"
    btn_danger_bg: str = "#7F1D1D"
    btn_danger_text: str = "#FCA5A5"
    btn_danger_hover: str = "#991B1B"

    # Link
    link_color: str = "#4FC6E0"
    link_hover: str = "#6DD3E8"

    # Notice / Alert
    notice_bg: str = "#141618"
    notice_border: str = "#282C31"
    notice_text: str = "#9AA3AD"

    # Radius
    radius_sm: str = "4px"
    radius_md: str = "6px"
    radius_lg: str = "10px"

    # Shadows
    shadow_sm: str = "0 1px 2px rgba(0,0,0,0.3)"
    shadow_md: str = "0 2px 8px rgba(0,0,0,0.4)"
    shadow_lg: str = "0 4px 16px rgba(0,0,0,0.5)"

    # Spacing
    spacing_xs: str = "4px"
    spacing_sm: str = "8px"
    spacing_md: str = "12px"
    spacing_lg: str = "16px"
    spacing_xl: str = "24px"
    spacing_xxl: str = "32px"

    # Typography
    font_family: str = "'Segoe UI', -apple-system, sans-serif"
    font_mono: str = "'Cascadia Code', 'JetBrains Mono', 'Consolas', 'Courier New', monospace"
    font_size_xs: str = "11px"
    font_size_sm: str = "12px"
    font_size_md: str = "13px"
    font_size_lg: str = "15px"
    font_size_xl: str = "18px"
    font_size_xxl: str = "24px"
    font_weight_normal: str = "400"
    font_weight_medium: str = "500"
    font_weight_semibold: str = "600"


DARK_THEME = ThemeTokens()

LIGHT_THEME = ThemeTokens(
    bg_primary="#F5F6F8",
    bg_surface="#FFFFFF",
    bg_elevated="#FFFFFF",
    bg_hover="#EBEDF0",
    bg_active="#E2E4E8",
    bg_input="#FFFFFF",

    border_default="#D1D5DB",
    border_subtle="#E5E7EB",
    border_strong="#B0B5BD",
    border_focus="#0E94AB",

    text_primary="#111827",
    text_secondary="#4B5563",
    text_tertiary="#9CA3AF",
    text_disabled="#D1D5DB",
    text_inverse="#FFFFFF",

    accent="#0E94AB",
    accent_hover="#0C7F94",
    accent_muted="#E0F4F8",
    accent_text="#0A7A8E",

    status_success="#059669",
    status_success_bg="#ECFDF5",
    status_warning="#D97706",
    status_warning_bg="#FFFBEB",
    status_error="#DC2626",
    status_error_bg="#FEF2F2",
    status_info="#2563EB",
    status_info_bg="#EFF6FF",

    scrollbar_bg="transparent",
    scrollbar_handle="#D1D5DB",
    scrollbar_handle_hover="#B0B5BD",

    sidebar_bg="#EBEDF0",
    sidebar_item_hover="#E2E4E8",
    sidebar_item_active="#D2EDF3",
    sidebar_separator="#D1D5DB",

    palette_bg="#FFFFFF",
    palette_border="#D1D5DB",
    palette_item_hover="#F3F4F6",

    toolbar_bg="#FFFFFF",

    code_bg="#F3F4F6",
    code_text="#111827",
    code_keyword="#0E94AB",
    code_string="#059669",
    code_number="#D97706",
    code_comment="#9CA3AF",

    btn_primary_bg="#0E94AB",
    btn_primary_text="#FFFFFF",
    btn_primary_hover="#0C7F94",
    btn_secondary_bg="#EBEDF0",
    btn_secondary_text="#111827",
    btn_secondary_hover="#E2E4E8",
    btn_secondary_border="#D1D5DB",
    btn_danger_bg="#FEE2E2",
    btn_danger_text="#DC2626",
    btn_danger_hover="#FECACA",

    link_color="#0A7A8E",
    link_hover="#0C7F94",

    notice_bg="#F3F4F6",
    notice_border="#E5E7EB",
    notice_text="#4B5563",

    shadow_sm="0 1px 2px rgba(0,0,0,0.05)",
    shadow_md="0 2px 8px rgba(0,0,0,0.07)",
    shadow_lg="0 4px 16px rgba(0,0,0,0.10)",
)

THEMES: Dict[str, ThemeTokens] = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
}


def get_theme(mode: str) -> ThemeTokens:
    """Get theme tokens by mode name."""
    return THEMES.get(mode, DARK_THEME)


def generate_stylesheet(tokens: ThemeTokens) -> str:
    """Generate the complete application stylesheet from theme tokens."""
    return f"""
    /* ═══════════════════════════════════════════════════════════
       DevTools Desktop — Generated Theme Stylesheet
       ═══════════════════════════════════════════════════════════ */

    * {{
        font-family: {tokens.font_family};
        outline: none;
    }}

    QMainWindow {{
        background-color: {tokens.bg_primary};
    }}

    /* ─── Scroll Bars ─── */
    QScrollBar:vertical {{
        background: {tokens.scrollbar_bg};
        width: 8px;
        margin: 0;
        border: none;
    }}
    QScrollBar::handle:vertical {{
        background: {tokens.scrollbar_handle};
        min-height: 30px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {tokens.scrollbar_handle_hover};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
        border: none;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
    QScrollBar:horizontal {{
        background: {tokens.scrollbar_bg};
        height: 8px;
        margin: 0;
        border: none;
    }}
    QScrollBar::handle:horizontal {{
        background: {tokens.scrollbar_handle};
        min-width: 30px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {tokens.scrollbar_handle_hover};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
        border: none;
    }}

    /* ─── Labels ─── */
    QLabel {{
        color: {tokens.text_primary};
        font-size: {tokens.font_size_md};
        background: transparent;
        border: none;
    }}
    QLabel[class="secondary"] {{
        color: {tokens.text_secondary};
        font-size: {tokens.font_size_sm};
    }}
    QLabel[class="heading"] {{
        font-size: {tokens.font_size_lg};
        font-weight: {tokens.font_weight_semibold};
    }}
    QLabel[class="title"] {{
        font-size: {tokens.font_size_xl};
        font-weight: {tokens.font_weight_semibold};
    }}
    QLabel[class="hero"] {{
        font-size: {tokens.font_size_xxl};
        font-weight: {tokens.font_weight_semibold};
    }}
    QLabel[class="notice"] {{
        color: {tokens.notice_text};
        font-size: {tokens.font_size_xs};
        padding: 8px 12px;
        background-color: {tokens.notice_bg};
        border: 1px solid {tokens.notice_border};
        border-radius: {tokens.radius_md};
    }}

    /* ─── Text Inputs ─── */
    QLineEdit {{
        background-color: {tokens.bg_input};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        padding: 7px 12px;
        font-size: {tokens.font_size_md};
        selection-background-color: {tokens.accent_muted};
        selection-color: {tokens.text_primary};
    }}
    QLineEdit:focus {{
        border-color: {tokens.border_focus};
    }}
    QLineEdit:disabled {{
        color: {tokens.text_disabled};
        background-color: {tokens.bg_surface};
    }}
    QLineEdit::placeholder {{
        color: {tokens.text_tertiary};
    }}

    /* ─── Text Areas ─── */
    QPlainTextEdit, QTextEdit {{
        background-color: {tokens.code_bg};
        color: {tokens.code_text};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        padding: 10px;
        font-family: {tokens.font_mono};
        font-size: {tokens.font_size_sm};
        selection-background-color: {tokens.accent_muted};
        selection-color: {tokens.text_primary};
    }}
    QPlainTextEdit:focus, QTextEdit:focus {{
        border-color: {tokens.border_focus};
    }}

    /* ─── Buttons ─── */
    QPushButton {{
        background-color: {tokens.btn_secondary_bg};
        color: {tokens.btn_secondary_text};
        border: 1px solid {tokens.btn_secondary_border};
        border-radius: {tokens.radius_md};
        padding: 6px 16px;
        font-size: {tokens.font_size_sm};
        font-weight: {tokens.font_weight_medium};
        min-height: 30px;
    }}
    QPushButton:hover {{
        background-color: {tokens.btn_secondary_hover};
    }}
    QPushButton:pressed {{
        background-color: {tokens.bg_active};
    }}
    QPushButton:disabled {{
        color: {tokens.text_disabled};
        background-color: {tokens.bg_surface};
        border-color: {tokens.border_subtle};
    }}
    QPushButton[class="primary"] {{
        background-color: {tokens.btn_primary_bg};
        color: {tokens.btn_primary_text};
        border: none;
        font-weight: {tokens.font_weight_semibold};
    }}
    QPushButton[class="primary"]:hover {{
        background-color: {tokens.btn_primary_hover};
    }}
    QPushButton[class="danger"] {{
        background-color: {tokens.btn_danger_bg};
        color: {tokens.btn_danger_text};
        border: none;
    }}
    QPushButton[class="danger"]:hover {{
        background-color: {tokens.btn_danger_hover};
    }}
    QPushButton[class="ghost"] {{
        background-color: transparent;
        border: none;
        color: {tokens.text_secondary};
        padding: 6px 10px;
    }}
    QPushButton[class="ghost"]:hover {{
        background-color: {tokens.bg_hover};
        color: {tokens.text_primary};
    }}
    QPushButton[class="icon"] {{
        background: transparent;
        border: none;
        padding: 4px;
        min-height: 24px;
        min-width: 24px;
        border-radius: {tokens.radius_sm};
    }}
    QPushButton[class="icon"]:hover {{
        background-color: {tokens.bg_hover};
    }}

    /* ─── Combo Box ─── */
    QComboBox {{
        background-color: {tokens.bg_input};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        padding: 6px 12px;
        font-size: {tokens.font_size_sm};
        min-height: 30px;
    }}
    QComboBox:hover {{
        border-color: {tokens.border_strong};
    }}
    QComboBox:focus {{
        border-color: {tokens.border_focus};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {tokens.text_secondary};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {tokens.bg_elevated};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        selection-background-color: {tokens.accent_muted};
        selection-color: {tokens.text_primary};
        padding: 4px;
    }}

    /* ─── Spin Box ─── */
    QSpinBox {{
        background-color: {tokens.bg_input};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        padding: 6px 8px;
        font-size: {tokens.font_size_sm};
    }}
    QSpinBox:focus {{
        border-color: {tokens.border_focus};
    }}

    /* ─── Check Box ─── */
    QCheckBox {{
        color: {tokens.text_primary};
        font-size: {tokens.font_size_sm};
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {tokens.border_default};
        border-radius: 4px;
        background-color: {tokens.bg_input};
    }}
    QCheckBox::indicator:checked {{
        background-color: {tokens.accent};
        border-color: {tokens.accent};
    }}
    QCheckBox::indicator:hover {{
        border-color: {tokens.border_strong};
    }}

    /* ─── Radio Button ─── */
    QRadioButton {{
        color: {tokens.text_primary};
        font-size: {tokens.font_size_sm};
        spacing: 8px;
    }}
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {tokens.border_default};
        border-radius: 8px;
        background-color: {tokens.bg_input};
    }}
    QRadioButton::indicator:checked {{
        background-color: {tokens.accent};
        border-color: {tokens.accent};
    }}

    /* ─── Tab Widget ─── */
    QTabWidget::pane {{
        border: 1px solid {tokens.border_default};
        background-color: {tokens.bg_surface};
        border-radius: {tokens.radius_md};
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: transparent;
        color: {tokens.text_secondary};
        padding: 8px 16px;
        font-size: {tokens.font_size_sm};
        font-weight: {tokens.font_weight_medium};
        border: none;
        border-bottom: 2px solid transparent;
    }}
    QTabBar::tab:selected {{
        color: {tokens.accent_text};
        border-bottom-color: {tokens.accent};
    }}
    QTabBar::tab:hover:!selected {{
        color: {tokens.text_primary};
    }}

    /* ─── Group Box ─── */
    QGroupBox {{
        color: {tokens.text_primary};
        font-size: {tokens.font_size_sm};
        font-weight: {tokens.font_weight_semibold};
        border: 1px solid {tokens.border_subtle};
        border-radius: {tokens.radius_lg};
        margin-top: 14px;
        padding: 20px 16px 16px 16px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        padding: 0 8px;
    }}

    /* ─── Table ─── */
    QTableWidget, QTableView {{
        background-color: {tokens.bg_surface};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        gridline-color: {tokens.border_subtle};
        font-size: {tokens.font_size_sm};
        selection-background-color: {tokens.accent_muted};
        selection-color: {tokens.text_primary};
    }}
    QHeaderView::section {{
        background-color: {tokens.bg_elevated};
        color: {tokens.text_secondary};
        font-size: {tokens.font_size_xs};
        font-weight: {tokens.font_weight_semibold};
        text-transform: uppercase;
        border: none;
        border-bottom: 1px solid {tokens.border_default};
        padding: 8px 12px;
    }}

    /* ─── Tree Widget ─── */
    QTreeWidget, QTreeView {{
        background-color: {tokens.bg_surface};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        font-size: {tokens.font_size_sm};
        selection-background-color: {tokens.accent_muted};
        selection-color: {tokens.text_primary};
        alternate-background-color: {tokens.bg_elevated};
    }}
    QTreeWidget::item, QTreeView::item {{
        padding: 4px 6px;
    }}
    QTreeWidget::item:selected, QTreeView::item:selected {{
        background-color: {tokens.accent_muted};
    }}
    QTreeWidget QHeaderView::section {{
        background-color: {tokens.bg_elevated};
        color: {tokens.text_secondary};
        font-size: {tokens.font_size_xs};
        font-weight: {tokens.font_weight_semibold};
        border: none;
        border-bottom: 1px solid {tokens.border_default};
        padding: 6px 10px;
    }}

    /* ─── Splitter ─── */
    QSplitter::handle {{
        background-color: {tokens.border_subtle};
    }}
    QSplitter::handle:horizontal {{
        width: 1px;
    }}
    QSplitter::handle:vertical {{
        height: 1px;
    }}
    QSplitter::handle:hover {{
        background-color: {tokens.accent};
    }}

    /* ─── ToolTip ─── */
    QToolTip {{
        background-color: {tokens.bg_elevated};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_sm};
        padding: 6px 10px;
        font-size: {tokens.font_size_xs};
    }}

    /* ─── Menu ─── */
    QMenu {{
        background-color: {tokens.bg_elevated};
        color: {tokens.text_primary};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_md};
        padding: 6px;
    }}
    QMenu::item {{
        padding: 8px 24px 8px 14px;
        border-radius: {tokens.radius_sm};
    }}
    QMenu::item:selected {{
        background-color: {tokens.accent_muted};
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {tokens.border_subtle};
        margin: 4px 8px;
    }}

    /* ─── Status Bar ─── */
    QStatusBar {{
        background-color: {tokens.bg_surface};
        color: {tokens.text_secondary};
        font-size: {tokens.font_size_xs};
        border-top: 1px solid {tokens.border_subtle};
    }}

    /* ─── Progress Bar ─── */
    QProgressBar {{
        background-color: {tokens.bg_elevated};
        border: none;
        border-radius: 3px;
        height: 4px;
        text-align: center;
        font-size: 0px;
    }}
    QProgressBar::chunk {{
        background-color: {tokens.accent};
        border-radius: 3px;
    }}

    /* ─── Frame ─── */
    QFrame[class="card"] {{
        background-color: {tokens.bg_surface};
        border: 1px solid {tokens.border_default};
        border-radius: {tokens.radius_lg};
    }}
    QFrame[class="card"]:hover {{
        border-color: {tokens.border_strong};
    }}
    QFrame[class="separator"] {{
        background-color: {tokens.border_subtle};
        max-height: 1px;
    }}

    /* ─── Dialog ─── */
    QDialog {{
        background-color: {tokens.bg_primary};
        color: {tokens.text_primary};
    }}

    /* ─── Message Box ─── */
    QMessageBox {{
        background-color: {tokens.bg_surface};
        color: {tokens.text_primary};
    }}
    QMessageBox QLabel {{
        color: {tokens.text_primary};
    }}

    /* ─── Scroll Area ─── */
    QScrollArea {{
        background: transparent;
        border: none;
    }}
    QScrollArea > QWidget > QWidget {{
        background: transparent;
    }}

    /* ─── Stacked Widget ─── */
    QStackedWidget {{
        background: transparent;
    }}
    """
