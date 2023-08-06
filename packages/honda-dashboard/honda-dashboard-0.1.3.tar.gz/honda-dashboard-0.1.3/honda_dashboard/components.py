import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout

from honda_dashboard.config import Config


class DashboardWindow(QMainWindow):

    def __init__(self, cfg: Config):
        super().__init__()

        self.__config = cfg
        self.setWindowTitle('Dashboard')
        self.handle_mode()

    def handle_mode(self):
        if self.__config.night_mode_on:
            color = self.__config.night_colors['bg']
        else:
            color = self.__config.day_colors['bg']

        self.setStyleSheet('background-color: #' + color + ';')


class DashboardWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setLayout(QGridLayout())


class InitialScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.setLayout(QVBoxLayout())
        loading = QLabel('LOADING...')
        font = QFont('Arial', 32)
        font.setBold(True)
        loading.setFont(font)
        loading.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(loading)
        self.setMinimumSize(480, 320)
        path = os.path.dirname(os.path.abspath(__file__))
        self.setStyleSheet('background-image: url(' + path + '/honda.png); background-position: center; '
                           'background-repeat: no-repeat;')
        loading.setStyleSheet('color: #ed323e;')

