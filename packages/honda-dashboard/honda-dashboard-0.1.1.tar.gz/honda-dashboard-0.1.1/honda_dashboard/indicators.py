import string

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from obd import OBDResponse

from config import Config


class Limits:

    def __init__(self, minimum: int, maximum: int, critical: int):
        self.min = minimum
        self.max = maximum
        self.critical = critical


class IndicatorBox(QWidget):

    def __init__(self, title: string, unit: string, cfg: Config, rounding=False, limits: Limits = None):
        super().__init__()

        self.__title = _Title(title, cfg)
        self.__value = _Value(unit, cfg, rounding, limits)
        self.__config = cfg

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__title)
        self.layout().addWidget(self.__value)

        self.handle_mode()

    def update_value(self, value: OBDResponse):
        self.__value.update_value(value)

    def handle_mode(self):
        self.__title.handle_mode()
        self.__value.handle_mode()


class _Value(QLabel):

    __color = None
    __value = None

    def __init__(self, unit: string, cfg: Config, rounding=False, limits: Limits = None):
        super().__init__()

        self.__config = cfg
        self.__unit = unit
        self.__rounding = rounding
        self.__limits = limits
        self.__limits_color_processor = _LimitsColorProcessor(limits, cfg)

        font = QFont('Arial', 20)
        font.setBold(True)
        self.setFont(font)

    def update_value(self, value: OBDResponse):
        if self.__should_update(value) is False:
            return

        self.__value = value.value
        val = self.__process_value(value)
        self.setText(val + ' ' + self.__unit)

        if self.__limits is None:
            return

        self.__update_color(val)

    def __should_update(self, value: OBDResponse) -> bool:
        if value.value != self.__value:
            self.__value = value.value

            return True

        return False

    def __update_color(self, val):
        color = self.__limits_color_processor.process(val)

        if self.__color != color:
            self.__color = color
            self.setStyleSheet('color: #' + color + ';')

    def handle_mode(self):
        if self.__config.night_mode_on:
            color = self.__config.night_colors['text']
        else:
            color = self.__config.day_colors['text']

        self.setStyleSheet('color: #' + color + ';')

    def __process_value(self, value: OBDResponse) -> string:
        val = str(value.value).split(' ')[0]

        if self.__rounding:
            val = round(float(val))

        return str(val)


class _Title(QLabel):

    def __init__(self, text: string, cfg: Config):
        super().__init__()

        self.__config = cfg
        self.setText(text)
        self.setFont(QFont('Arial', 14))

    def handle_mode(self):
        if self.__config.night_mode_on:
            color = self.__config.night_colors['text']
        else:
            color = self.__config.day_colors['text']

        self.setStyleSheet('color: #' + color + ';')


class _LimitsColorProcessor:
    __MIN_COLOR_KEY = 'min'
    __NORMAL_COLOR_KEY = 'normal'
    __MAX_COLOR_KEY = 'max'
    __CRITICAL_COLOR_KEY = 'critical'

    def __init__(self, limits: Limits, cfg: Config):
        self.__limits = limits
        self.__config = cfg

    def process(self, value: string) -> string:
        color_key = self.__color_key(value)

        if self.__config.night_mode_on:
            return self.__config.night_colors[color_key]

        return self.__config.day_colors[color_key]

    def __color_key(self, value: string) -> string:
        val = int(value)

        if val <= self.__limits.min:
            return self.__MIN_COLOR_KEY

        if self.__limits.min < val <= self.__limits.max:
            return self.__NORMAL_COLOR_KEY

        if self.__limits.max < val <= self.__limits.critical:
            return self.__MAX_COLOR_KEY

        return self.__CRITICAL_COLOR_KEY
