import customtkinter as ctk
from typing import List
from tkinter.filedialog import askopenfile

from db import Term, TextbookSection
from import_export import import_csv_terms
from utils import blob_to_image, find

from .term_list import TermList
from .components.import_message_box import ImportMessageBox


class TermControllWindow(ctk.CTkToplevel):
    term_list_frame = None
    selected_id: int = None
    term_items: List[ctk.CTkFrame] = [] # Массив элементов списка
    image_data = None

    def __get_term_from_fields(self) -> Term:
        caption = self.term_caption_field.get()
        description = self.description_field.get('0.0', 'end')
        section_caption = self.section_box.get()

        section = None

        try:
            section = TextbookSection.get(TextbookSection.caption == section_caption)
        except:
            pass

        return Term(
            caption=caption,
            description=description,
            section_id=section.section_id if section else None,
            image=self.image_data
        )

    def __on_add_click(self):
        term = self.__get_term_from_fields()
        term.save()
        self.selected_id = term.id if term else None
        self.redraw()

    def __on_edit_click(self):
        term = self.__get_term_from_fields()
        term.term_id = self.selected_id
        term.save()
        self.redraw()

    def __on_item_removed(self, term: Term):
        if term.term_id == self.selected_id:
            self.selected_id = None
        term.delete_instance()
        self.on_update()
        self.redraw()

    def __on_item_selected(self, term: Term):
        self.selected_id = term.term_id
        self.redraw()

    def redraw_image(self):
        if not self.image_data:
            self.image_box.configure(image='', text='Нет изображения!')
        else:
            img = blob_to_image(self.image_data)
            self.image_box.configure(image=img, text='')

    def redraw(self):
        terms: List[Term] = Term.select().order_by(Term.caption.desc()).execute()
        selected_term = None
        if terms and self.selected_id is not None:
            selected_term = find(terms, lambda elm, i, _: elm.term_id == self.selected_id)
            if not selected_term:
                self.selected_id = None

        self.term_caption_field.delete(0, 'end')
        self.description_field.delete('0.0', 'end')

        self.term_list.update(terms, self.selected_id)

        if not selected_term:
            self.section_box.set('')
            self.image_data = None
        else:
            self.image_data = selected_term.image
            self.term_caption_field.insert(0, selected_term.caption)
            self.description_field.insert('0.0', str(selected_term.description or '').rstrip())
            try:
                section = TextbookSection.get_by_id(selected_term.section_id)
                self.section_box.set(section.caption)
            except:
                self.section_box.set('')

        self.redraw_image()

    def __draw_term_list(self):
        term_list_frame = ctk.CTkFrame(self)

        self.search_field = ctk.CTkEntry(term_list_frame, placeholder_text='Введите текст для поиска...', font=self.defaultFont, state='disabled')

        terms = Term.select().order_by(Term.caption.desc()).execute()

        self.term_list = TermList(term_list_frame, terms, self.__on_item_selected, self.__on_item_removed, font=self.defaultFont)

        self.term_list.pack(side=ctk.BOTTOM, fill=ctk.BOTH, padx=10, pady=10, expand=True)
        self.search_field.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        term_list_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    def __on_image_click(self, _):
        file = askopenfile('rb')
        if not file: return
        try:
            self.image_data = file.read()
        finally:
            file.close()
        self.redraw_image()

    def __on_import_click(self):
        def on_ok(filename, encoding):
            if import_csv_terms(filename, encoding):
                self.redraw()
                if self.on_update:
                    self.on_update()

        if hasattr(self, '__import_box') and self.__import_box:
            self.__import_box.destroy()
        self.__import_box = ImportMessageBox(self, on_ok)

    def __draw_term_info(self):
        frame = ctk.CTkFrame(self)

        self.term_caption_field = ctk.CTkEntry(frame, placeholder_text='Название термина...', font=self.defaultFont)

        bottom_frame = ctk.CTkFrame(frame)
        self.description_field = ctk.CTkTextbox(bottom_frame, font=self.defaultFont)
        right_frame = ctk.CTkFrame(bottom_frame)

        sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute() or []
        values = [section.caption for section in sections]

        self.section_box = ctk.CTkComboBox(right_frame, values=values, font=self.defaultFont)
        self.image_box = ctk.CTkLabel(right_frame, text='Нет изображения!', font=self.defaultFont)
        self.image_box.bind('<Button-1>', self.__on_image_click)
        add_btn = ctk.CTkButton(right_frame, text='Добавить', font=self.defaultFont, command=self.__on_add_click)
        edit_btn = ctk.CTkButton(right_frame, text='Обновить', font=self.defaultFont, command=self.__on_edit_click)
        import_btn = ctk.CTkButton(right_frame, text='Импорт CSV', font=self.defaultFont, command=self.__on_import_click)

        self.description_field.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.image_box.pack(side=ctk.TOP, fill=ctk.Y, padx=10, pady=10, expand=True)
        add_btn.pack(side=ctk.BOTTOM, padx=10, pady=(10, 0))
        edit_btn.pack(side=ctk.BOTTOM, padx=10, pady=(10, 0))
        import_btn.pack(side=ctk.BOTTOM, padx=10, pady=0)
        self.section_box.pack(side=ctk.BOTTOM, padx=10, pady=10)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=(10, 0))

        self.term_caption_field.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.BOTH, padx=10, pady=10, expand=True)
        frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

    def __init__(self, master, on_update, geometry = '1000x600'):
        super().__init__(master)
        self.defaultFont = getattr(master, 'defaultFont', None)
        self.title('Termer - Окно управления разделами')
        self.geometry(geometry)

        self.on_update = on_update

        self.__draw_term_info()
        self.__draw_term_list()
