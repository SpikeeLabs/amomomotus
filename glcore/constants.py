from PyQt6.QtGui import QColor


class Color:
    BLACK = QColor("black")
    WHITE = QColor("white")

    TRANSPARENT = QColor(0, 0, 0, 0)
    TRANSPARENT_BLACK = QColor(0, 0, 0, 75)
    TRANSPARENT_WHITE = QColor(255, 255, 255, 75)

    DARK_YELLOW = QColor(216, 162, 51)
    NEON_YELLOW = QColor(237, 225, 85)
    YELLOW = QColor(230, 224, 99)
    LIGHT_YELLOW = QColor(240, 229, 171)

    DARK_BLUE = QColor(63, 182, 237)
    BLUE = QColor(6, 102, 185)
    LIGHT_BLUE = QColor(20, 196, 255)

    DARK_RED = QColor(166, 54, 57)
    NEON_RED = QColor(195, 48, 0)
    RED = QColor(233, 75, 80)
    LIGHT_RED = QColor(255, 83, 89)

    DARK_GREEN = QColor(51, 153, 102)
    GREEN = QColor(102, 255, 102)
    LIGHT_GREEN = QColor(171, 240, 208)

    DARK_VIOLET = QColor(153, 51, 204)
    VIOLET = QColor(196, 99, 247)
    LIGHT_VIOLET = QColor(221, 171, 240)

    DARK_ORANGE = QColor(255, 140, 0)
    ORANGE = QColor(255, 165, 0)
    LIGHT_ORANGE = QColor(255, 215, 0)
