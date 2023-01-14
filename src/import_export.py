from shutil import make_archive
from typing import List
from os.path import exists
import pandas as pd

from config import PROG_DIR
from db import Term, TextbookSection
from utils import find


def export_data(path: str) -> None:
    if not path or path == '': return
    if path.endswith('.zip'):
        path = path[:-4]
    make_archive(path, 'zip', PROG_DIR)


def read_all(path: str, encoding: str) -> List[List[str]]:
    out = None
    with open(path, encoding=encoding) as f:
        if path.endswith('.csv'):
            out = pd.read_csv(f, dtype=str)
        else:
            out = pd.read_excel(f, dtype=str)
    if out is None:
        return None
    return [[None if y != y else y for y in x] for x in out.values.tolist()]


def import_csv_sections(path: str, encoding = 'utf-8') -> bool:
    if not path or path == '': return False
    data = read_all(path, encoding)
    if not data: return False

    TextbookSection.insert_many(data).on_conflict_ignore().execute()
    return True


def import_csv_terms(path: str, encoding = 'utf-8') -> bool:
    if not path or path == '': return False
    data = read_all(path, encoding)
    if not data: return False

    sections = [{ 'caption': x[0] } for x in data if len(x) > 0]
    TextbookSection.insert_many(sections).on_conflict_ignore().execute()

    sections: List[TextbookSection] = TextbookSection.select().execute()

    insert_data = []
    for row in data:
        if len(row) < 2 or not row[1]: continue

        out = {
            'caption': row[1],
            'description': row[2] if len(row) > 2 else '',
        }

        if row[0]:
            section = find(sections, lambda e, i, _: e.caption == row[0])
            if section: out['section_id'] = section.section_id

        if len(row) > 3 and row[3] and exists(row[3]):
            with open(row[3], 'rb') as f:
                out['image'] = f.read()

        insert_data.append(out)

    Term.insert_many(insert_data).on_conflict_ignore().execute()
    return True
