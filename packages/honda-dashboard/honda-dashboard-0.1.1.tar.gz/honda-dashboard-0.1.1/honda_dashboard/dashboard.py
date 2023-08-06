#!/usr/bin/env python

import sys
from threading import Thread

import obd
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication

from components import DashboardWindow, DashboardWidget, InitialScreen
from config import Config
from indicators import IndicatorBox, Limits
from toolbar import Toolbar


class Dashboard:

    def __init__(self):
        self.__config = Config()
        self.__app = QApplication([])
        self.__main_window = DashboardWindow(self.__config)
        self.__toolbar = Toolbar(self.__config)
        self.__main_widget = DashboardWidget()

        self.__build_indicators()

    def run(self):
        self.__toolbar.toggle_night_mode.triggered.connect(self.__night_mode_toggled)
        self.__main_window.addToolBar(Qt.RightToolBarArea, self.__toolbar)
        self.__main_window.show()

        initial_screen = InitialScreen()
        self.__main_window.setCentralWidget(initial_screen)
        initial_screen.show()

        conn_thread = Thread(target=self.__connection_init)
        conn_thread.start()

        sys.exit(self.__app.exec())

    def __build_indicators(self):
        self.__speed = IndicatorBox('Speed', 'km/h', self.__config, True, Limits(50, 90, 140))
        self.__main_widget.layout().addWidget(self.__speed, 0, 0)

        self.__rpm = IndicatorBox('RPM', 'rpm', self.__config, True, Limits(2500, 3500, 5500))
        self.__main_widget.layout().addWidget(self.__rpm, 0, 1)

        self.__coolant_temp = IndicatorBox('Coolant', '°C', self.__config, True, Limits(45, 85, 100))
        self.__main_widget.layout().addWidget(self.__coolant_temp, 0, 2)

        self.__engine_load = IndicatorBox('Engine', '%', self.__config, True, Limits(40, 60, 80))
        self.__main_widget.layout().addWidget(self.__engine_load, 1, 0)

        self.__intake_temp = IndicatorBox('Intake', '°C', self.__config, True)
        self.__main_widget.layout().addWidget(self.__intake_temp, 1, 1)

        self.__intake_press = IndicatorBox('Intake', 'kPa', self.__config, True)
        self.__main_widget.layout().addWidget(self.__intake_press, 1, 2)

    def __night_mode_toggled(self):
        self.__config.set('MODE', 'night_mode_on', '0' if self.__config.night_mode_on else '1')
        self.__main_window.handle_mode()
        self.__toolbar.handle_mode()
        self.__speed.handle_mode()
        self.__rpm.handle_mode()
        self.__coolant_temp.handle_mode()
        self.__engine_load.handle_mode()
        self.__intake_temp.handle_mode()
        self.__intake_press.handle_mode()

    def __connection_init(self):
        connection = obd.Async(self.__config.device)

        if connection.is_connected():
            self.__main_window.setCentralWidget(self.__main_widget)

        connection.watch(obd.commands.SPEED, callback=self.__speed.update_value)
        connection.watch(obd.commands.RPM, callback=self.__rpm.update_value)
        connection.watch(obd.commands.COOLANT_TEMP, callback=self.__coolant_temp.update_value)
        connection.watch(obd.commands.ENGINE_LOAD, callback=self.__engine_load.update_value)
        connection.watch(obd.commands.INTAKE_TEMP, callback=self.__intake_temp.update_value)
        connection.watch(obd.commands.INTAKE_PRESSURE, callback=self.__intake_press.update_value)
        connection.start()

