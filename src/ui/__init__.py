import customtkinter as ctk
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfilename
from typing import List, Tuple
from peewee import fn

from config import Config, VERSION
from db import TextbookSection, Term
from import_export import export_data
from .result_window import ResultWindow
from .section_control_window import SectionControlWindow
from .term_control_window import TermControlWindow


class TermerApp(ctk.CTk):
    class SectionFrame(ctk.CTkFrame):
        section_boxes: List[Tuple[int, ctk.CTkCheckBox]] = []
        section_list = None

        def get_selected_sections(self):
            return [id for (id, box) in self.section_boxes if box.get()]

        def __select_all(self):
            for (_, box) in self.section_boxes:
                box.select()
            self.action_handler()

        def __deselect_all(self):
            for (_, box) in self.section_boxes:
                box.deselect()
            self.action_handler()

        def draw_section_list(self):
            if self.section_list:
                self.section_list.destroy()
            self.section_list = ctk.CTkFrame(self)

            sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute()

            self.section_boxes.clear()

            if not sections or len(sections) <= 0:
                label = ctk.CTkLabel(self.section_list, text='Разделов нет!', font=self.defaultFont)
                label.pack(expand=True)
            else:
                for section in sections:
                    box = ctk.CTkCheckBox(self.section_list, text=section.caption, command=self.action_handler, font=self.defaultFont)
                    self.section_boxes.append((section.section_id, box))
                    box.pack(anchor='w', padx=10, pady=5)

            self.section_list.pack(fill=ctk.BOTH, expand=True, side=ctk.BOTTOM, pady=10)

        def __draw_section_btns(self):
            section_btns = ctk.CTkFrame(self)
            select_all = ctk.CTkButton(section_btns, text='Выделить всё', command=self.__select_all, font=self.defaultFont)
            deselect_all = ctk.CTkButton(section_btns, text='Снять выделение', command=self.__deselect_all, font=self.defaultFont)
            select_all.pack(fill=ctk.X, side=ctk.LEFT, padx=5, pady=5, expand=True)
            deselect_all.pack(fill=ctk.X, side=ctk.RIGHT, padx=5, pady=5, expand=True)
            section_btns.pack(side=ctk.TOP, fill=ctk.X)

        def __init__(self, master, action_handler):
            super().__init__(master)
            self.defaultFont = getattr(master, 'defaultFont', None)
            self.action_handler = action_handler

            label = ctk.CTkLabel(self, text='Выбор разделов', font=getattr(master, 'headerFont', None))
            label.pack(fill=ctk.X, side=ctk.TOP)
            self.draw_section_list()
            self.__draw_section_btns()

    class OptionsFrame(ctk.CTkFrame):
        def get_mode(self):
            return self.__mode.get()

        def get_count(self):
            val = self.__count.get()
            if not val.isdigit():
                return None
            return int(val)

        def __draw_mode_selector(self):
            frame = ctk.CTkFrame(self)

            label = ctk.CTkLabel(frame, text='Выберите отображаемую часть термина', font=self.defaultFont)

            m1 = ctk.CTkRadioButton(frame, text='Термин', variable=self.__mode, value=0, font=self.defaultFont)
            m2 = ctk.CTkRadioButton(frame, text='Определение', variable=self.__mode, value=1, font=self.defaultFont)
            m3 = ctk.CTkRadioButton(frame, text='Изображение', variable=self.__mode, value=2, font=self.defaultFont)

            label.pack(fill=ctk.X, pady=5, padx=10)
            m1.pack(fill=ctk.X, pady=2.5, padx=5)
            m2.pack(fill=ctk.X, pady=2.5, padx=5)
            m3.pack(fill=ctk.X, pady=2.5, padx=5)
            frame.pack(fill=ctk.X, padx=10, ipady=5)

        def __draw_count_input(self):
            frame = ctk.CTkFrame(self)

            label = ctk.CTkLabel(frame, text='Укажите размер выборки (шт.):', font=self.defaultFont)
            self.count_input = ctk.CTkEntry(frame, textvariable=self.__count, font=self.defaultFont) # TODO: Добавить отображение валидации
            # TODO: Добавить вызов action_handler при изменении текста

            label.pack(side=ctk.LEFT, pady=5, padx=5)
            self.count_input.pack(side=ctk.RIGHT, padx=5)
            frame.pack(fill=ctk.X, padx=10, pady=10)

        def __on_export_click(self):
            newfile = asksaveasfilename(filetypes=[('Архив данных', '*.zip')], initialfile='termer_data')
            export_data(newfile)

        def __draw_control_btns(self, make_open_toplevel):

            section_control_btn = ctk.CTkButton(self, text='База категорий', command=make_open_toplevel('section_control'), font=self.defaultFont)
            term_control_btn = ctk.CTkButton(self, text='База терминов', command=make_open_toplevel('term_control'), font=self.defaultFont)
            export_btn = ctk.CTkButton(self, text='Экспорт базы', command=self.__on_export_click, font=self.defaultFont)

            section_control_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=(0, 10))
            term_control_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=(0, 10))
            export_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

        def __init__(self, master, make_open_toplevel):
            super().__init__(master)
            self.defaultFont = getattr(master, 'defaultFont', None)
            self.__mode = ctk.IntVar(master, 0)
            self.__count = ctk.StringVar(master, '5')

            label = ctk.CTkLabel(self, text='Настройка выборки', font=getattr(master, 'headerFont', None))
            label.pack(fill=ctk.X)

            self.__draw_mode_selector()
            self.__draw_count_input()
            self.__draw_control_btns(make_open_toplevel)

            self.result_btn = ctk.CTkButton(self, text='Создать выборку', command=make_open_toplevel('result'), state='disabled', font=self.defaultFont)
            self.result_btn.pack(fill=ctk.X, padx = 10)

    term_control = None
    section_control = None
    result_window = None

    def make_open_toplevel(self, name: str):
        if name == 'result':
            return self.__calculate_result
        elif name == 'section_control':
            return self.__open_section_control
        elif name == 'term_control':
            return self.__open_term_control

    def __on_data_changed(self):
        section_ids = self.left_part.get_selected_sections()
        count = self.right_part.get_count()

        state = 'disabled' if len(section_ids) <= 0 or not count or count <= 0 else 'normal'
        self.right_part.result_btn.configure(state=state)

        self.left_part.draw_section_list()

    def __on_options_changed(self):
        section_ids = self.left_part.get_selected_sections()
        count = self.right_part.get_count()

        state = 'disabled' if len(section_ids) <= 0 or not count or count <= 0 else 'normal'
        self.right_part.result_btn.configure(state=state)

    def __open_section_control(self):
        if self.section_control:
            self.section_control.destroy()
        self.section_control = SectionControlWindow(self, self.__on_data_changed)

    def __open_term_control(self):
        if self.term_control:
            self.term_control.destroy()
        self.term_control = TermControlWindow(self, self.__on_data_changed)

    def __calculate_result(self):
        section_ids = self.left_part.get_selected_sections()
        count = self.right_part.get_count()
        mode = self.right_part.get_mode()

        if not count or count <= 0:
            showwarning('Termer - Операция невозможна!', 'Указано неверное кол-во терминов!')
            return

        where = Term.section_id << section_ids

        if mode == 1:
            where &= Term.description.is_null(False)
        elif mode == 2:
            where &= Term.image.is_null(False)

        terms: List[Term] = Term.select().where(where).order_by(fn.random()).limit(count).execute()

        if not terms or len(terms) <= 0:
            showwarning('Termer - Операция невозможна!', 'По заданым критериям терминов не найдено!')
            return

        if self.result_window:
            self.result_window.destroy()
        self.result_window = ResultWindow(self, terms, mode)

    def __init__(self):
        super().__init__()
        self.defaultFont = ctk.CTkFont(family='JetBrains Mono', size=13)
        self.headerFont = ctk.CTkFont(family='JetBrains Mono', size=15)

        self.title(f'Termer {VERSION} - основное окно')
        self.geometry('800x600')

        self.left_part = TermerApp.SectionFrame(self, self.__on_options_changed)
        self.left_part.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        self.right_part = TermerApp.OptionsFrame(self, self.make_open_toplevel)
        self.right_part.pack(side=ctk.RIGHT, fill=ctk.BOTH)


def prepare_app(config: Config):
    ctk.set_appearance_mode(config.appearance_mode)
    ctk.set_default_color_theme(config.color_theme)

    app = TermerApp()

    return app
