from random import choice

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import (
    QBrush,
    QFont,
    QPainter,
    QPaintEvent,
    QPen,
    QRadialGradient,
    QResizeEvent,
)
from PyQt6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QWidget,
)

from games.bingo import MiniGrid
from glcore.application import MediaPlayer
from glcore.constants import Color
from glcore.widget import ShadowText, SquareWidget


class DrawBallWidget(QLabel, SquareWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(Color.TRANSPARENT_BLACK)
        shadow_effect.setOffset(3, 3)

        self.setGraphicsEffect(shadow_effect)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        if not self.text():
            return

        rect = self.rect().adjusted(10, 10, -10, -10)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Color.WHITE, 0, Qt.PenStyle.NoPen))

        # draws the circle
        painter.setBrush(QBrush(Color.BLACK if self.text()[0] == "-" else Color.NEON_YELLOW))
        painter.drawEllipse(rect)

        # draws the text
        if self.text()[0] != "-":
            painter.setPen(QPen(Color.BLACK, 1))
            painter.setFont(QFont("Gotham Bold", rect.width() // 2, QFont.Weight.Bold))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

        painter.end()


# TODO editable label
class TeamLabel(QLineEdit, ShadowText):
    pass
    # def eventFilter(self, source: QObject, event: QEvent) -> bool:
    #     if event.type() == QEvent.Type.KeyPress:
    #         print(event.text().isnumeric())
    #         if event.text().isnumeric():
    #             return super().eventFilter(source, event)
    #     return False


class MotusTeam(QWidget):
    """The score widget for Motus team."""

    def __init__(self, i, parent: QWidget | None = None):
        super().__init__(parent)
        self.setMaximumHeight(int(parent.height() // 3.5))

        layout = QHBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        self.bingoref = parent.widget(i)
        self.minigrid = MiniGrid(self, self.bingoref)
        self.bingoref.minigrid = self.minigrid
        layout.addWidget(self.minigrid)

        self.drawer = DrawBallWidget(self)
        self.drawer.setStyleSheet("QLabel: {background-color: transparent;}")
        layout.addWidget(self.drawer)

        self._stext = ShadowText(parent=self)
        self._stext.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self._stext)

        self.index, self.score = i, 0
        self.active = i == 0

    @property
    def score(self) -> int:
        return int(self._stext.text())

    @score.setter
    def score(self, score: int):
        self._stext.setText(f"{score:03}")

    def resizeEvent(self, event: QResizeEvent):
        self._stext.setFont(QFont("TT Chocolates Trl DemiBold", int(self.height() / 1.75)))
        self._stext.resize(event.size())

    def draw_balls(self, n=1):
        ball, balls = None, set(self.bingoref.remaining_balls)

        # TODO bezier cubic

        for i in range(-30, 5):
            ball = choice(list(balls - {ball}))
            self.drawer.setText(str(ball))
            self.drawer.repaint()

            if i <= 0:
                QThread.msleep(100)
            else:
                QThread.msleep(i * 100)

        self.drawer.repaint()
        ij = self.bingoref.remaining_balls.pop(ball)

        if ball < 0:
            MediaPlayer.play("grille_boule_noire")
            MediaPlayer.play("ting-2")
            self.score -= 20
            self.repaint()
            QThread.msleep(1000)
        else:
            bingo = self.bingoref.get_bingo_cells(ij)

            if bingo:
                MediaPlayer.play("motus")
            else:
                MediaPlayer.play("present")

            self.bingoref.ball_found_animation(ij)
            self.minigrid.repaint()

            if bingo:
                self.bingoref.bingo_found_animimation(bingo)
                self.bingoref.remaining_balls = {}

                self.score += 100
            elif n > 0:
                self.draw_balls(n - 1)

        self.drawer.setText("")

    def paintEvent(self, event: QPaintEvent):
        rect = self.rect()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        match self.index % 5:
            case 0:
                color = (Color.LIGHT_ORANGE, Color.ORANGE, Color.DARK_ORANGE)
            case 1:
                color = (Color.LIGHT_VIOLET, Color.VIOLET, Color.DARK_VIOLET)
            case 2:
                color = (Color.LIGHT_RED, Color.RED, Color.DARK_RED)
            case 3:
                color = (Color.LIGHT_GREEN, Color.GREEN, Color.DARK_GREEN)
            case 4:
                color = (Color.LIGHT_YELLOW, Color.YELLOW, Color.DARK_YELLOW)

        gradient = QRadialGradient(rect.topLeft().toPointF(), rect.width() * 0.8)

        if self.active:
            painter.setPen(QPen(Color.WHITE, self.height() // 10))
            gradient.setColorAt(0, color[0])
            gradient.setColorAt(0.3, color[1])
            gradient.setColorAt(1, color[2])
        else:
            painter.setPen(QPen(Color.WHITE, 0, Qt.PenStyle.NoPen))
            start = color[1].darker(100)
            start.setAlpha(170)
            gradient.setColorAt(0, start)

            end = color[2].darker(120)
            end.setAlpha(190)
            gradient.setColorAt(1, end)

        # draws background color and active border
        painter.setBrush(gradient)
        painter.drawRect(rect)
        painter.end()
