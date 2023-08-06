from threading import Thread

import obd
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel

from components import DashboardWindow, DashboardWidget, InitialScreen
from config import Config
from indicators import IndicatorBox, Limits
from toolbar import Toolbar

config = Config()
app = QApplication([])
main_window = DashboardWindow(config)
main_widget = DashboardWidget()
toolbar = Toolbar(config)

speed = IndicatorBox('Speed', 'km/h', config, True, Limits(50, 90, 140))
main_widget.layout().addWidget(speed, 0, 0)

rpm = IndicatorBox('RPM', 'rpm', config, True, Limits(2500, 3500, 5500))
main_widget.layout().addWidget(rpm, 0, 1)

coolant_temp = IndicatorBox('Coolant', '°C', config, True, Limits(45, 85, 100))
main_widget.layout().addWidget(coolant_temp, 0, 2)

engine_load = IndicatorBox('Engine', '%', config, True, Limits(40, 60, 80))
main_widget.layout().addWidget(engine_load, 1, 0)

intake_temp = IndicatorBox('Intake', '°C', config, True)
main_widget.layout().addWidget(intake_temp, 1, 1)

intake_press = IndicatorBox('Intake', 'kPa', config, True)
main_widget.layout().addWidget(intake_press, 1, 2)


@pyqtSlot()
def night_mode_toggled():
    config.set('MODE', 'night_mode_on', '0' if config.night_mode_on else '1')
    main_window.handle_mode()
    toolbar.handle_mode()
    speed.handle_mode()
    rpm.handle_mode()
    coolant_temp.handle_mode()
    engine_load.handle_mode()
    intake_temp.handle_mode()
    intake_press.handle_mode()


toolbar.toggle_night_mode.triggered.connect(night_mode_toggled)

main_window.addToolBar(Qt.RightToolBarArea, toolbar)
main_window.show()


def connection_init():
    connection = obd.Async('/dev/pts/1')

    if connection.is_connected():
        main_window.setCentralWidget(main_widget)

    connection.watch(obd.commands.SPEED, callback=speed.update_value)
    connection.watch(obd.commands.RPM, callback=rpm.update_value)
    connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp.update_value)
    connection.watch(obd.commands.ENGINE_LOAD, callback=engine_load.update_value)
    connection.watch(obd.commands.INTAKE_TEMP, callback=intake_temp.update_value)
    connection.watch(obd.commands.INTAKE_PRESSURE, callback=intake_press.update_value)
    connection.start()


if __name__ == '__main__':
    initial_screen = InitialScreen()
    main_window.setCentralWidget(initial_screen)
    initial_screen.show()

    conn_thread = Thread(target=connection_init)
    conn_thread.start()

    app.exec()

