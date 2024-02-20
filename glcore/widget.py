from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPen, QResizeEvent
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QLabel, QWidget

from glcore.constants import Color


class Widget(QWidget):
    """The base canvas of the application."""

    # pylint: disable=unused-argument
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.WHITE, 0, Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(Color.LIGHT_BLUE))
        painter.drawRect(self.rect())
        painter.end()


class SquareWidget(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

    # pylint: disable=unused-argument
    def resizeEvent(self, event: QResizeEvent):
        size = min(self.width(), self.height())
        self.resize(size, size)


class ShadowText(QLabel):
    """Text label with a shadow effect."""

    def __init__(self, txt: str | None = None, parent: QWidget | None = None):
        super().__init__(txt, parent)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(10)
        shadow_effect.setColor(Color.TRANSPARENT_BLACK)
        shadow_effect.setOffset(6, 10)

        self.setGraphicsEffect(shadow_effect)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # pylint: disable=unused-argument
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.WHITE, 1))
        painter.drawText(self.rect(), self.alignment(), self.text())
        painter.end()
