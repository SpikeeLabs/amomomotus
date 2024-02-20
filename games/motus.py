from collections import defaultdict
from enum import IntEnum
from functools import lru_cache

from PyQt6.QtCore import QPointF, QRect, QRectF, Qt, QThread
from PyQt6.QtGui import (
    QFont,
    QLinearGradient,
    QPainter,
    QPaintEvent,
    QPen,
    QPolygonF,
    QRadialGradient,
    QResizeEvent,
)
from PyQt6.QtWidgets import QGridLayout, QWidget

from glcore.application import MediaPlayer
from glcore.constants import Color
from glcore.widget import ShadowText, Widget


class MotusGrid(Widget):
    """The grid of the Motus game."""

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.motus: list[list[MotusTile]] = []

        layout = QGridLayout(self)
        self.setLayout(layout)

        self.shining = None

    def clear_layout(self) -> QGridLayout:
        layout = self.layout()

        while layout.count():
            label = layout.takeAt(0).widget()
            label.setVisible(False)
            label.setParent(None)
            layout.removeWidget(label)

        return layout

    def setup(self, rows, cols):
        # tells which letters should stay displayed
        self.corrects = [True] + [False] * (cols - 1)

        # clears the grid tiles
        layout = self.clear_layout()

        margin = int((self.width() - self.height() * cols / rows) / 2)
        self.setContentsMargins(margin, 0, margin, 0)

        self.motus = []
        for i in range(rows):
            self.motus.append([])
            for j in range(cols):
                self.motus[i].append(MotusTile(parent=self))
                layout.addWidget(self.motus[i][j], i, j)

    def setup_line(self, i, w):
        self.motus[i][0].active = True
        for j, label in enumerate(self.motus[i]):
            label.text = w[j] if self.corrects[j] else "."

    def check_input(self, w, w2) -> list["MotusTile.Status"]:
        if w == w2:
            return [MotusTile.Status.CORRECT] * len(w)

        counter: dict[str, int] = defaultdict(int)
        result = [MotusTile.Status.INCORRECT] * len(w)

        for i, c1 in enumerate(w):
            if c1 != w2[i]:
                counter[c1] += 1

        for i, (c1, c2) in enumerate(zip(w, w2)):
            if c1 == c2:
                result[i] = MotusTile.Status.CORRECT
            elif counter[c2]:
                result[i] = MotusTile.Status.MISPLACED
                counter[c2] -= 1

        return result

    def shine(self, i):
        tiles = self.motus[i]
        for pos in range(-100, self.width() + 300, 30):
            self.shining = pos
            for tile in tiles:
                tile.repaint()
            QThread.msleep(30)
        self.shining = None

    def update_line(self, i, di, w, w2=None):
        QThread.msleep(500)

        statuses = self.check_input(w, w2 or w)

        for j, label in enumerate(self.motus[i]):
            label.status = statuses[j]
            self.corrects[j] |= label.status == MotusTile.Status.CORRECT

            if w2:
                if j >= di:
                    label.text = " "
            else:
                label.text = w[j]

            label.repaint()
            MediaPlayer.play(str(label.status))
            QThread.msleep(200)


class MotusTile(Widget):
    """A tile of the Motus grid."""

    class Status(IntEnum):
        CORRECT, MISPLACED, INCORRECT = range(3)

        def __str__(self):
            return self.name.lower()

    def __init__(self, txt: str | None = None, parent: QWidget | None = None):
        super().__init__(parent)

        self._stext = ShadowText(txt, self)
        self.status = MotusTile.Status.INCORRECT
        self.active = False

    @property
    def text(self) -> str:
        return self._stext.text()

    @text.setter
    def text(self, txt: str | None):
        self._stext.setText(txt)

    def resizeEvent(self, event: QResizeEvent):
        self._stext.setFont(QFont("Gotham", int(self.height() / 1.75), QFont.Weight.Bold))
        self._stext.resize(event.size())

    @lru_cache
    def get_bevels(self, r: QRect) -> list[tuple[QPolygonF, QLinearGradient]]:
        result = []

        inside = QRectF(
            (5 * r.topLeft() + r.center()).toPointF() / 6,
            (5 * r.bottomRight() + r.center()).toPointF() / 6,
        )
        rcoords = list(r.getCoords())
        rcoords[2:] = [x + 1 for x in rcoords[2:]]
        icoords = list(inside.getCoords())
        icoords[2:] = [x + 1 for x in icoords[2:]]

        for i in range(4):
            p = QPolygonF(
                [
                    QPointF(rcoords[2 * (i // 2)], rcoords[(2 * (i // 2) + 1) % 4]),
                    QPointF(icoords[2 * (i // 2)], icoords[(2 * (i // 2) + 1) % 4]),
                    QPointF(
                        icoords[(2 * (i // 2) + 2 * (i % 2 == 0)) % 4],
                        icoords[(2 * (i // 2) + 1 + 2 * (i % 2)) % 4],
                    ),
                    QPointF(
                        rcoords[(2 * (i // 2) + 2 * (i % 2 == 0)) % 4],
                        rcoords[(2 * (i // 2) + 1 + 2 * (i % 2)) % 4],
                    ),
                ]
            ).intersected(QPolygonF(r.toRectF()))

            g = QLinearGradient((p.at(0) + p.at(3)) / 2, (p.at(2) + p.at(1)) / 2)
            g.setColorAt(0.5, [Color.TRANSPARENT_WHITE, Color.TRANSPARENT_BLACK][i // 2])
            g.setColorAt(1, Color.TRANSPARENT)

            result.append((p, g))

        return result

    def paintEvent(self, event: QPaintEvent):
        rect = self.rect()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.BLACK, 0, Qt.PenStyle.NoPen))

        if self.status == MotusTile.Status.CORRECT:
            # draws red background
            gradient = QRadialGradient(rect.topLeft().toPointF(), rect.height() * 1.414)
            gradient.setColorAt(0, Color.LIGHT_RED)
            gradient.setColorAt(1, Color.DARK_RED)
            painter.setBrush(gradient)
            painter.drawRect(rect)

            # draws bevels
            for polygon, gradient in self.get_bevels(rect):
                painter.setBrush(gradient)
                painter.drawPolygon(polygon)
        else:
            # draws blue background and cursor
            gradient = QRadialGradient(rect.topLeft().toPointF(), rect.height() * 1.414)
            gradient.setColorAt(0, Color.DARK_BLUE)
            gradient.setColorAt(1, Color.BLUE.lighter(200 if self.active else 0))
            painter.setBrush(gradient)
            painter.drawRect(rect)

            if self.status == MotusTile.Status.MISPLACED:
                circle_size = min(self.width(), self.height()) - 10
                x, y = (self.width() - circle_size) // 2, (self.height() - circle_size) // 2

                # draws yellow circle
                gradient = QLinearGradient(rect.topLeft().toPointF(), rect.bottomRight().toPointF())
                gradient.setColorAt(0, Color.YELLOW)
                gradient.setColorAt(1, Color.DARK_YELLOW)
                painter.setBrush(gradient)
                painter.drawEllipse(x, y, circle_size, circle_size)

        shining = self.parent().shining
        if shining is not None:
            ar = self.geometry()
            painter.translate(-ar.topLeft())
            # light
            gradient = QRadialGradient(
                QPointF(shining, self.y() + self.height() * (2 / 3)),
                (1 - abs(shining / self.parent().width() - 0.5)) * rect.height() * 1.414,
            )
            gradient.setColorAt(0, Color.WHITE)
            gradient.setColorAt(0.5, Color.TRANSPARENT_WHITE)
            gradient.setColorAt(1, Color.TRANSPARENT)
            painter.setBrush(QRadialGradient(gradient))
            painter.drawRect(ar)
            # lens flare
            gradient = QRadialGradient(
                QPointF(200 + self.parent().width() - shining, self.y() + self.height() * (1 / 3)),
                (1 - abs(shining / self.parent().width() - 0.5)) * rect.height() / 2,
            )
            gradient.setColorAt(0.8, Color.TRANSPARENT_WHITE)
            gradient.setColorAt(1, Color.TRANSPARENT)
            painter.setBrush(QRadialGradient(gradient))
            painter.drawRect(ar)

        painter.end()
