from pathlib import Path

from config import Config
from db import prepare_db
from ui import prepare_app

PROG_DIR = Path.home().joinpath('Documents/goodmice/Termer')
PROG_DIR.mkdir(parents=True, exist_ok=True) # Создаём директории если не существуют
DB_PATH = str(PROG_DIR.joinpath('termer_data.db'))
CFG_PATH = str(PROG_DIR.joinpath('config.ini'))


def main():
    config = Config(CFG_PATH, DB_PATH) # Читаем конфиг

    prepare_db(config.db_path) # Инициализируем классы для работы с базой

    app = prepare_app(config)

    app.mainloop()


if __name__ == '__main__':
    main()
