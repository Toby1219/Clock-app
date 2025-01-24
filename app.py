"""
Time App
"""

import importlib.metadata
import sys

from PySide6 import QtWidgets

from .timeapp import Time



def main():
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])

    app = QtWidgets.QApplication(sys.argv)
    main_window = Time()
    main_window.show()
    sys.exit(app.exec())
