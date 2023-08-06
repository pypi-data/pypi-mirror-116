import qtawesome as qta
from PyQt5.QtWidgets import QToolButton, QToolBar, QAction

from honda_dashboard.config import Config


class Toolbar(QToolBar):

    def __init__(self, cfg: Config):
        super().__init__()

        self.__config = cfg
        self.toggle_night_mode = QAction()

        # Add night mode button.
        self.__night_mode_btn = _NightModeBtn(cfg)
        self.__night_mode_btn.clicked.connect(self.__night_mode_toggle)
        self.addWidget(self.__night_mode_btn)

        self.handle_mode()

    def handle_mode(self):
        if self.__config.night_mode_on:
            text_color = self.__config.night_colors['text']
            bg = self.__config.night_colors['bg']
        else:
            text_color = self.__config.day_colors['text']
            bg = self.__config.day_colors['bg']

        self.setStyleSheet('background-color: #' + bg + '; color: #' + text_color + ';')
        self.__night_mode_btn.handle_mode()

    def __night_mode_toggle(self):
        self.toggle_night_mode.trigger()


class _NightModeBtn(QToolButton):

    __icon_color = None

    def __init__(self, cfg: Config):
        super().__init__()

        self.__config = cfg

        self.setIcon(qta.icon('ei.adjust'))
        self.setToolTip('Toggle night/day mode.')
        self.setBaseSize(32, 32)
        self.isCheckable()

    def handle_mode(self):
        if self.__config.night_mode_on:
            text_color = self.__config.night_colors['text']
            bg = self.__config.night_colors['bg']
            hover = self.__config.night_colors['hover']
        else:
            text_color = self.__config.day_colors['text']
            bg = self.__config.day_colors['bg']
            hover = self.__config.day_colors['hover']

        self.setStyleSheet('_NightModeBtn {background-color: #' + bg + ';}'
                           + '_NightModeBth:hover {background-color: #' + hover + ';}')
        self.setIcon(qta.icon('ei.adjust', color='#' + text_color))


