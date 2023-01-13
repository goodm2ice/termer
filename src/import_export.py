from shutil import make_archive
from typing import List
import csv
from os.path import exists

from config import PROG_DIR
from db import Term, TextbookSection
from utils import find


def export_data(path: str) -> None:
    if not path or path == '': return
    if path.endswith('.zip'):
        path = path[:-4]
    make_archive(path, 'zip', PROG_DIR)


def import_csv_sections(path: str) -> bool:
    if not path or path == '': return False
    data = None
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        data = [{ 'caption': x[0] } for x in reader]
    if not data: return False
    TextbookSection.insert_many(data).on_conflict_ignore().execute()
    return True


def import_csv_terms(path: str) -> bool:
    if not path or path == '': return False
    data = None
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        data = [tuple(x) for x in reader if len(x) > 0]

    if not data: return False
    sections = [{ 'caption': x[0] } for x in data]
    TextbookSection.insert_many(sections).on_conflict_ignore().execute()

    sections: List[TextbookSection] = TextbookSection.select().execute()

    insert_data = []
    for row in data:
        if not row[1]: continue

        out = {
            'caption': row[1],
            'description': row[2],
        }

        if row[0]:
            section = find(sections, lambda e, i, _: e.caption == row[0])
            if section: out['section_id'] = section.section_id

        if row[3] and exists(row[3]):
            with open(row[3], 'rb') as f:
                out['image'] = f.read()

        insert_data.append(out)

    Term.insert_many(insert_data).on_conflict_ignore().execute()
    return True
