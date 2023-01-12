from config import Config, PROG_DIR, CFG_PATH, DB_PATH
from db import prepare_db
from ui import prepare_app


PROG_DIR.mkdir(parents=True, exist_ok=True) # Создаём директории если не существуют


def main():
    config = Config(CFG_PATH, DB_PATH) # Читаем конфиг

    prepare_db(config.db_path) # Инициализируем классы для работы с базой

    app = prepare_app(config)

    app.mainloop()


if __name__ == '__main__':
    main()
