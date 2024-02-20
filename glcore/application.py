import logging
import os
import sys

from PyQt6.QtCore import QEventLoop, Qt, QThread, QUrl
from PyQt6.QtGui import QFontDatabase, QKeyEvent
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QWidget

from glcore.window import Window

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class FontLoader:
    SOURCE_DIR: str = "./font"

    @staticmethod
    def load_fonts(path: str = SOURCE_DIR):
        loaded_fonts: list[str] = []

        if path and os.path.exists(path) and os.path.isdir(path):
            for file in os.listdir(path):
                if file.endswith((".ttf", ".otf")):
                    font_id = QFontDatabase.addApplicationFont(os.path.join(path, file))
                    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                    loaded_fonts.append(font_family)

        LOGGER.info(
            "Loaded fonts families (src:%s): %s",
            path,
            ", ".join(f"'{font}'" for font in loaded_fonts) if loaded_fonts else [],
        )

    @staticmethod
    def get_fonts() -> list[str]:
        return QFontDatabase.families()


class MediaPlayer:
    SOURCE_DIR: str = "./media"
    threads: set[QThread] = set()

    @classmethod
    def play(cls, name: str):
        for thread in set(cls.threads):
            if thread.isFinished():
                cls.threads.remove(thread)

        thread = QThread()
        cls.threads.add(thread)

        def run():
            effect = QSoundEffect()
            effect.setSource(QUrl.fromLocalFile(f"{cls.SOURCE_DIR}/{name}.wav"))
            effect.play()
            loop = QEventLoop()
            effect.playingChanged.connect(loop.quit)
            loop.exec()

        thread.run = run
        thread.start()


class Application(QApplication):
    def __init__(self, name: str | None = None):
        super().__init__(sys.argv)

        self.window = Window(name)

        screens = self.screens()
        self.window.setGeometry(screens[-1].geometry())
        self.window.container.setFixedSize(screens[-1].size())

        cursor = Qt.CursorShape.BlankCursor
        self.setOverrideCursor(cursor)
        self.changeOverrideCursor(cursor)
        self.window.container.setCursor(cursor)

        FontLoader.load_fonts()

        self.init(self.window.container)
        self.window.container.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.quit()
            sys.exit(0)

    def init(self, container: QWidget):
        raise NotImplementedError("init method is abstract, must be implemented in subclass")

    def launch(self):
        self.window.showFullScreen()
        self.window.raise_()
        sys.exit(self.exec())
