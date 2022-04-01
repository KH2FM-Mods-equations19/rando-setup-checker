import os
import sys

from PySide6 import QtGui
from PySide6.QtWidgets import QPushButton, QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel
from qt_material import apply_stylesheet

from pcconfig import PcConfigurationDialog
from pcsx2config import Pcsx2ConfigurationDialog


def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))[:])
    return os.path.join(base_path, relative_path)


class SetupCheckerWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Rando Setup Checker')
        self.setMinimumWidth(600)

        pc_button = QPushButton('PC')
        pc_button.clicked.connect(self._open_pc_checker)

        pcsx2_button = QPushButton('PCSX2')
        pcsx2_button.clicked.connect(self._open_pcsx2_checker)

        box = QVBoxLayout()
        box.addWidget(QLabel('Choose a platform'))
        box.addWidget(pc_button)
        box.addWidget(pcsx2_button)

        widget = QWidget()
        widget.setLayout(box)
        self.setCentralWidget(widget)

    def _open_pc_checker(self):
        dialog = PcConfigurationDialog()
        dialog.exec()

    def _open_pcsx2_checker(self):
        dialog = Pcsx2ConfigurationDialog()
        dialog.exec()


if __name__ == '__main__':
    app = QApplication([])

    QtGui.QFontDatabase.addApplicationFont(resource_path('resources/KHMenu.otf'))

    window = SetupCheckerWindow()

    apply_stylesheet(app, theme='dark_cyan.xml')
    stylesheet = app.styleSheet()
    with open(resource_path('resources/stylesheet.css')) as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window.show()

    sys.exit(app.exec())
