from pathlib import Path
from peewee import Model, AutoField, TextField, BlobField, ForeignKeyField, DatabaseProxy, SqliteDatabase


db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class TextbookSection(BaseModel):
    section_id = AutoField(column_name='SectionId') # ID секции
    caption = TextField(column_name='Caption', null=False, unique=True) # Название секции
    class Meta:
        db_table = 'sections'


class Term(BaseModel):
    term_id = AutoField(column_name='TermId') # ID термина
    section_id = ForeignKeyField(TextbookSection, null=True) # ID секции термина
    caption = TextField(column_name='Caption', null=False) # Термин
    description = TextField(column_name='Description', null=True) # Описание термина
    image = BlobField(column_name='Image', null=True) # Изображение, связанное с термином

    class Meta:
        db_table = 'terms'
        indexes = (
            (('section_id', 'caption'), True),
        )


def prepare_db(db_path: str):
    path = Path(db_path)
    try:
        with open(db_path, 'a'): # Проверка на корректность имени файла
            pass
    except OSError:
        path = path.joinpath('termer_data.db') # Добавляем имя файла в конец, если его нет
    path.parent.mkdir(parents=True, exist_ok=True) # Создаём папку для базы если не существует

    db = SqliteDatabase(str(path))

    db_proxy.initialize(db)
    db.create_tables([TextbookSection, Term])
