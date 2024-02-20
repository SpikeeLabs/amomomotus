from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow

from glcore.widget import Widget


class Window(QMainWindow):
    """Window class for the application."""

    def __init__(self, title: str | None = None):
        super().__init__()

        self.setWindowTitle(title)

        self.container = Widget(self)
        self.container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCentralWidget(self.container)
