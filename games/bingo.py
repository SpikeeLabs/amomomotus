from collections import defaultdict
from math import cos, pi as π
from random import sample

from PyQt6.QtCore import QPointF, Qt, QThread
from PyQt6.QtGui import (
    QBrush,
    QFont,
    QLinearGradient,
    QPainter,
    QPaintEvent,
    QPen,
    QRadialGradient,
    QRegion,
)
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGridLayout, QLabel, QWidget

from glcore.application import MediaPlayer
from glcore.constants import Color
from glcore.widget import SquareWidget, Widget


class BingoGrid(Widget):
    GRID_SIZE = 5

    def __init__(self, i, parent: QWidget):
        super().__init__(parent)

        self.balls = frozenset({n + 1 for n in range(i % 2, 70, 2)})
        self.remaining_balls: dict[int, tuple[int, int]] = {}
        self.grid: dict[tuple[int, int], BingoTile] = {}
        self.minigrid = None

        layout = QGridLayout(self)
        layout.setSpacing(2)
        self.setLayout(layout)

        for k in range(self.GRID_SIZE * self.GRID_SIZE):
            i, j = k // self.GRID_SIZE, k % self.GRID_SIZE
            self.grid[(i, j)] = BingoTile(parent=self)
            layout.addWidget(self.grid[(i, j)], i, j)

    def init_grid_animation(self):
        for label in self.grid.values():
            label.lune = 0
            label.is_visible = False
            label.repaint()

        grid_balls = sample(list(self.balls), self.GRID_SIZE * self.GRID_SIZE)
        population = range(len(grid_balls)), 13
        free_indices = sample(*population)

        while not self.is_grid_valid(free_indices):
            free_indices = sample(*population)

        self.remaining_balls = {-k: None for k in range(1, 3)}
        sorted_indices = set()

        for k in range(len(grid_balls)):
            ij = k // self.GRID_SIZE, k % self.GRID_SIZE
            self.grid[ij].is_visible = True
            MediaPlayer.play("grille_creation")
            self.grid[ij].setText(str(grid_balls[k]))
            self.grid[ij].repaint()
            self.minigrid.repaint()
            QThread.msleep(150)

            if k in free_indices:
                sorted_indices.add(k)
            else:
                self.remaining_balls[grid_balls[k]] = ij

        for k in sorted_indices:
            ij = k // self.GRID_SIZE, k % self.GRID_SIZE

            for i in range(0, 91, 30):
                self.grid[ij].lune = i
                self.grid[ij].repaint()
                QThread.msleep(25)

            MediaPlayer.play("grille_numero")
            self.grid[ij].setText("")
            self.grid[ij].repaint()
            self.minigrid.repaint()
            QThread.msleep(150)

    def is_grid_valid(self, indices) -> bool:
        rows, cols, diags = defaultdict(int), defaultdict(int), defaultdict(int)

        for k in indices:
            i, j = k // self.GRID_SIZE, k % self.GRID_SIZE

            if i == j:
                diags[0] += 1
            if 4 - i == j:
                diags[1] += 1
            rows[i] += 1
            cols[j] += 1

            if self.GRID_SIZE - 1 in (rows[i], cols[j], diags[0], diags[1]):
                return False

        return True

    def ball_found_animation(self, ij):
        for i in range(6):
            self.grid[ij].ball_found = not self.grid[ij].ball_found
            self.grid[ij].repaint()
            QThread.msleep(150)

        for i in range(0, 181, 10):
            self.grid[ij].lune = i
            self.grid[ij].repaint()
            QThread.msleep(25)

        self.grid[ij].setText("")

    def get_bingo_cells(self, ij) -> list[(int, int)]:
        bingo = []

        if not any(self.grid[(ij[0], j)].text() and j != ij[1] for j in range(self.GRID_SIZE)):
            bingo = [(ij[0], j) for j in range(self.GRID_SIZE)]
        elif not any(self.grid[(i, ij[1])].text() and i != ij[0] for i in range(self.GRID_SIZE)):
            bingo = [(i, ij[1]) for i in range(self.GRID_SIZE)]
        elif ij[0] == ij[1] and not any(self.grid[(i, i)].text() and i != ij[0] for i in range(self.GRID_SIZE)):
            bingo = [(i, i) for i in range(self.GRID_SIZE)]
        elif 4 - ij[0] == ij[1] and not any(
            self.grid[(i, 4 - i)].text() and 4 - i != ij[1] for i in range(self.GRID_SIZE)
        ):
            bingo = [(4 - i, i) for i in range(self.GRID_SIZE)]

        return bingo

    def bingo_found_animimation(self, bingo):
        for i, ij in enumerate(bingo):
            self.grid[ij].setText("MOTUS"[i])

        for ij in bingo:
            for i in range(0, 181, 20):
                self.grid[ij].lune = 180 - i
                self.grid[ij].repaint()
                QThread.msleep(25)


class MiniTile(QWidget):
    def __init__(self, parent: QWidget, labelref):
        super().__init__(parent)
        self.reftile = labelref

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.WHITE, 0, Qt.PenStyle.NoPen))

        painter.setBrush(QBrush(Color.TRANSPARENT_BLACK))
        if self.reftile.is_visible:
            if not self.reftile.text():
                painter.setBrush(QBrush(Color.NEON_YELLOW))
            elif self.reftile.text().isalpha():
                painter.setBrush(QBrush(Color.NEON_RED))
        painter.drawEllipse(self.rect())
        painter.end()


class MiniGrid(SquareWidget):
    def __init__(self, parent: QWidget, refgrid: BingoGrid):
        super().__init__(parent)
        self.refgrid = refgrid

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(Color.TRANSPARENT_BLACK)
        shadow_effect.setOffset(3, 3)
        self.setGraphicsEffect(shadow_effect)

        layout = QGridLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        self.setLayout(layout)

        self.tiles = []
        for ij, label in self.refgrid.grid.items():
            minilab = MiniTile(self, label)
            self.tiles.append(minilab)
            layout.addWidget(minilab, *ij)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.WHITE, 0, Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(Color.LIGHT_BLUE))
        painter.drawRoundedRect(self.rect(), 10, 10)
        painter.end()

        super().paintEvent(event)


class BingoTile(QLabel, SquareWidget):
    """The tile class of the Bingo grid."""

    def __init__(self, txt: str | None = None, parent: QWidget | None = None):
        super().__init__(parent)
        self.setText(txt)
        self.is_visible = False
        self.ball_found = False
        self.bingo_found = False
        self.lune = 0

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = self.rect()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.WHITE, 0, Qt.PenStyle.NoPen))

        # draws the blue background
        gradient = QLinearGradient(rect.topLeft().toPointF(), rect.bottomRight().toPointF())
        gradient.setColorAt(0, Color.DARK_BLUE)
        gradient.setColorAt(1, Color.BLUE)
        painter.setBrush(gradient)
        painter.drawRect(rect)

        if self.is_visible:
            if not self.ball_found:
                circle_rect = rect.adjusted(
                    self.width() // 10, self.height() // 10, -self.width() // 10, -self.height() // 10
                )
                circle_size = circle_rect.width()

                # draws the shadow of the circle
                shadow_factor = 1.2
                gradient = QRadialGradient(rect.center().toPointF(), rect.width() / 2)
                gradient.setColorAt(1 / shadow_factor, Color.TRANSPARENT_BLACK)
                gradient.setColorAt(1, Color.TRANSPARENT)
                painter.setBrush(gradient)
                painter.drawRect(rect)

                # draws the yellow circle and text
                if not self.text():
                    self.lune = 180

                width_factor = abs(cos(self.lune * π / 180))

                if self.text() and self.lune < 90:
                    painter.translate((1 - width_factor) * rect.width() / 2, 0)
                    painter.scale(width_factor, 1)

                    painter.setBrush(QBrush(Color.NEON_RED if self.text().isalpha() else Color.NEON_YELLOW))
                    painter.drawEllipse(circle_rect)

                    painter.setPen(QPen(Color.WHITE if self.text().isalpha() else Color.BLACK, 1))
                    painter.setFont(QFont("Gotham Bold", circle_rect.width() // 2, QFont.Weight.Bold))
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

                painter.end()
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setPen(QPen(Color.BLACK, 0, Qt.PenStyle.NoPen))

                if self.lune > 0:
                    ajustment = int(circle_size * (1 - width_factor) / 2)
                    croissant = QRegion(circle_rect, QRegion.RegionType.Ellipse).intersected(
                        QRegion(circle_rect.adjusted(circle_size // 2, 0, 0, 0))
                    )
                    ellipse = QRegion(circle_rect.adjusted(ajustment, 0, -ajustment, 0), QRegion.RegionType.Ellipse)
                    if self.lune < 90:
                        croissant = croissant.subtracted(ellipse)
                    else:
                        croissant = croissant.united(ellipse)

                    painter.setClipRegion(croissant)

                    gradient = QRadialGradient(
                        rect.center().toPointF() + QPointF(circle_size / 6, -circle_size / 5), circle_size / 1.5
                    )
                    gradient.setColorAt(0, Color.WHITE)
                    gradient.setColorAt(0.3, Color.YELLOW)
                    gradient.setColorAt(1, Color.DARK_YELLOW)
                    painter.setBrush(gradient)
                    painter.drawEllipse(circle_rect)
                    painter.setClipping(False)

            if self.bingo_found:
                painter.setPen(QPen(Color.WHITE, 3))
                painter.setBrush(QBrush(Color.TRANSPARENT_WHITE))
                painter.drawRect(rect)

        painter.end()
