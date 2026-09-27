"""
DevTools Desktop — Application Entry Point
"""

import sys
import os

# Ensure the app package is in the Python path when running directly
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from app.core.branding import APPLICATION_ID, PRODUCT_NAME, COMPANY_NAME, VERSION_STRING
from app.core.tool_registry import register_all_tools
from app.ui.main_window import MainWindow

def main():
    # Set application metadata for OS integration
    QApplication.setApplicationName(PRODUCT_NAME)
    QApplication.setApplicationVersion(VERSION_STRING)
    QApplication.setOrganizationName(COMPANY_NAME)
    QApplication.setOrganizationDomain(APPLICATION_ID)
    
    # Required for Windows taskbar icon grouping
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPLICATION_ID)
    except Exception:
        pass

    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), "public", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Register all tools before creating the main window
    register_all_tools()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
