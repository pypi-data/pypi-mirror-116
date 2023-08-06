import configparser


class Config:
    night_mode_on = None
    device = None
    day_colors = []
    night_colors = []

    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__read()

    def __read(self):
        self.__config.read('./config.ini')
        self.night_mode_on = self.__config['MODE']['night_mode_on'] != '0'
        self.night_colors = self.__config['NIGHT_COLORS']
        self.day_colors = self.__config['DAY_COLORS']
        self.device = self.__config['CONNECTION']['device']

    def set(self, section, option, value):
        self.__config.set(section, option, value)
        self.__config['MODE']['night_mode_on'] = value

        with open("config.ini", 'w') as configfile:
            self.__config.write(configfile)

        self.__read()
