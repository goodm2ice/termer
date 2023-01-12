from configparser import ConfigParser
from pathlib import Path

VERSION = 'v0.1.0'


PROG_DIR = Path.home().joinpath('Documents/goodmice/Termer')
DB_PATH = str(PROG_DIR.joinpath('termer_data.db'))
CFG_PATH = str(PROG_DIR.joinpath('config.ini'))


class Config:
    def __init__(self, path: str, default_db_path: str) -> None:
        self.__edit_password = '6437' # Пароль по-умолчанию
        self.__appearance_mode = 'System'
        self.__color_theme = 'blue'
        self.__db_path = default_db_path

        self.path = path

        if not Path(self.path).exists():
            self.__save()
        else:
            self.reload()

    def reload(self):
        config = ConfigParser()
        config.read(self.path)
        self.__edit_password = config.get('DEFAULT', 'EditPassword', fallback=self.__edit_password)
        self.__db_path = config.get('DEFAULT', 'DbPath', fallback=self.__db_path)
        self.__appearance_mode = config.get('Appearance', 'Mode', fallback=self.__appearance_mode)
        self.__color_theme = config.get('Appearance', 'ColorTheme', fallback=self.__color_theme)

    def __save(self):
        config = ConfigParser()
        config['DEFAULT'] = {
            'EditPassword': self.__edit_password,
            'DbPath': self.__db_path,
        }
        config['Appearance'] = {
            'Mode': self.__appearance_mode,
            'ColorTheme': self.__color_theme,
        }

        with open(self.path, 'w') as file:
            config.write(file)

    @property
    def edit_password(self):
        return self.__edit_password

    @property
    def appearance_mode(self):
        return self.__appearance_mode

    @property
    def color_theme(self):
        return self.__color_theme

    @property
    def db_path(self):
        return self.__db_path
