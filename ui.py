import customtkinter as ctk
from tkinter.messagebox import showwarning
from tkinter.filedialog import askopenfile
from typing import List, Tuple
from peewee import fn
from PIL import Image, ImageTk
from io import BytesIO

from config import Config
from db import TextbookSection, Term


def blob_to_image(blob):
    if not blob:
        return None
    img = Image.open(BytesIO(blob))
    img = ImageTk.PhotoImage(img)
    return img


class ResultWindow(ctk.CTkToplevel):
    def __init__(self, master, terms: List[Term], mode):
        super().__init__(master)
        self.defaultFont = ctk.CTkFont('JetBrains Mono', 20)
        self.title('Выборка терминов')
        width, item_height = 600, 95
        match mode:
            case 1: item_height = 150
            case 2: item_height = 200
            case _: width = 500
        self.geometry(f'{width}x{max(len(terms)*item_height, 500)}')

        for i, term in enumerate(terms):
            frame = ctk.CTkFrame(self)
            label = ctk.CTkLabel(frame, text=f'№{i+1}:', font=self.defaultFont)
            value = None
            match mode:
                case 2: value = ctk.CTkLabel(frame, image=blob_to_image(term.image), text='')
                case 1: value = ctk.CTkLabel(frame, font=self.defaultFont, text=str(term.description).rstrip(), justify=ctk.LEFT, wraplength=True)
                case _: value = ctk.CTkLabel(frame, font=self.defaultFont, text=term.caption)

            label.pack(side=ctk.TOP, anchor=ctk.NW, padx=10, pady=(5, 15))
            if value:
                value.pack(side=ctk.BOTTOM, anchor=ctk.SW, padx=(50, 10), pady=(0, 5))
            frame.pack(padx=10, pady=10, fill=ctk.X)


class SectionControllWindow(ctk.CTkToplevel):
    section_boxes = []
    section_list = None

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
            self.section_boxes.clear()
            for section in sections:
                frame = ctk.CTkFrame(self.section_list)
                var = ctk.StringVar(frame, section.caption)

                def save():
                    nval = var.get().strip()
                    if nval == '':
                        return
                    section.section_id = section.section_id
                    section.caption = nval
                    section.save()
                    self.draw_section_list()
                    self.on_update()

                def remove():
                    section.delete_instance()
                    self.draw_section_list()
                    self.on_update()

                entry = ctk.CTkEntry(frame, textvariable=var, font=self.defaultFont)

                save_btn = ctk.CTkButton(frame, width=100, text='Сохранить', command=save, fg_color='#FFAD33', hover_color='#C88A2F', font=self.defaultFont)
                remove_btn = ctk.CTkButton(frame, width=100, text='Удалить', command=remove, fg_color='#D7324C', hover_color='#FF516D', font=self.defaultFont)

                self.section_boxes.append((section.section_id, var, entry))

                entry.pack(fill=ctk.X, side=ctk.LEFT, padx=5, pady=5, expand=True)
                remove_btn.pack(side=ctk.RIGHT)
                save_btn.pack(side=ctk.RIGHT, padx=5)
                frame.pack(fill=ctk.X, padx=5, pady=5)

        self.section_list.pack(fill=ctk.BOTH, expand=True, side=ctk.TOP, pady=10, padx=10)

    def __add_new_category(self):
        caption = ctk.CTkInputDialog(text='Введите название нового раздела:', title='Добавление раздела')
        val = caption.get_input()
        if not val or val.strip() == '':
            return
        TextbookSection.create(caption=val.strip())
        self.draw_section_list()
        self.on_update()

    def __init__(self, master, on_update, geometry = '700x600'):
        super().__init__(master)
        self.defaultFont = master.defaultFont
        self.title('Termer - Окно управления разделами')
        self.geometry(geometry)

        self.on_update = on_update

        self.draw_section_list()

        self.add_btn = ctk.CTkButton(self, text='Добавить новый раздел', command=self.__add_new_category, font=self.defaultFont)
        self.add_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=(0, 10))


class TermList(ctk.CTkFrame):
    __item_boxes: List[ctk.CTkFrame] = []

    def __first_draw(self, terms: List[Term]):
        if not terms or len(terms) <= 0:
            label = ctk.CTkLabel(self, text='Терминов нет!', font=self.defaultFont)
            label.pack(expand=True)
        else:
            for term in terms:
                item_frame = ctk.CTkFrame(self)

                term_label = ctk.CTkLabel(item_frame, text=term.caption, font=self.defaultFont)
                term_label.bind('<Button-1>', self.make_on_select(term))

                delete_btn = ctk.CTkButton(item_frame,
                    text='Удалить',
                    command=self.make_on_remove_click(term),
                    fg_color='#D7324C',
                    hover_color='#FF516D',
                    font=self.defaultFont
                )

                term_label.pack(side=ctk.LEFT, fill=ctk.X, padx=5, pady=5, expand=True)
                delete_btn.pack(side=ctk.RIGHT, padx=5, pady=5)
                item_frame.pack(fill=ctk.X, padx=5, pady=5)

                self.__item_boxes.append(item_frame)

    def update(self, terms: List[Term], selected_id: int = None):
        while len(self.__item_boxes) > 0:
            self.__item_boxes.pop().destroy()
        if not terms or len(terms) <= 0:
            label = ctk.CTkLabel(self, text='Терминов нет!', font=self.defaultFont)
            label.pack(expand=True)
        else:
            for term in terms:
                item_frame = ctk.CTkFrame(self)
                if term.term_id == selected_id:
                    item_frame.configure(True, bg_color='green')

                term_label = ctk.CTkLabel(item_frame, text=term.caption, font=self.defaultFont)
                term_label.bind('<Button-1>', self.make_on_select(term))

                delete_btn = ctk.CTkButton(item_frame,
                    text='Удалить',
                    command=self.make_on_remove_click(term),
                    fg_color='#D7324C',
                    hover_color='#FF516D',
                    font=self.defaultFont
                )

                term_label.pack(side=ctk.LEFT, fill=ctk.X, padx=5, pady=5, expand=True)
                delete_btn.pack(side=ctk.RIGHT, padx=5, pady=5)
                item_frame.pack(fill=ctk.X, padx=5, pady=5)

                self.__item_boxes.append(item_frame)

    def __init__(self, master, terms: List[Term], on_select = None, on_remove_click = None, font = None, **kwargs):
        super().__init__(master, **kwargs)
        self.defaultFont = font
        def make_on_select(term):
            def __on_select(_):
                on_select(term)
            return __on_select

        def make_on_remove(term):
            def __on_remove():
                on_remove_click(term)
            return __on_remove
        self.make_on_select = make_on_select
        self.make_on_remove_click = make_on_remove
        self.__first_draw(terms)


class TermControllWindow(ctk.CTkToplevel):
    term_list_frame = None
    selected_id: int = None
    terms: List[Term] = []
    sections: List[TextbookSection] = []
    term_items: List[ctk.CTkFrame] = [] # Массив элементов списка

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
            self.image_box.configure(True, image=None, text='Нет изображения!')
        else:
            self.image_box.configure(True, image=blob_to_image(self.image_data), text='')

    def redraw(self):
        terms: List[Term] = Term.select().order_by(Term.caption.desc()).execute()
        selected_term = None
        if terms and self.selected_id is not None:
            selected_term = next((term for term in terms if term.term_id == self.selected_id), None)
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
            self.description_field.insert('0.0', selected_term.description)
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

    def __draw_term_info(self):
        frame = ctk.CTkFrame(self)

        self.term_caption_field = ctk.CTkEntry(frame, placeholder_text='Название термина...', font=self.defaultFont)

        bottom_frame = ctk.CTkFrame(frame)
        self.description_field = ctk.CTkTextbox(bottom_frame, font=self.defaultFont, )
        right_frame = ctk.CTkFrame(bottom_frame)


        values = [section.caption for section in self.sections]

        self.section_box = ctk.CTkComboBox(right_frame, values=values, font=self.defaultFont)
        self.image_box = ctk.CTkLabel(right_frame, text='Нет изображения!', font=self.defaultFont)
        self.image_box.bind('<Button-1>', self.__on_image_click)
        add_btn = ctk.CTkButton(right_frame, text='Добавить', font=self.defaultFont, command=self.__on_add_click)
        edit_btn = ctk.CTkButton(right_frame, text='Обновить', font=self.defaultFont, command=self.__on_edit_click)

        self.description_field.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=10, pady=10, expand=True)
        self.image_box.pack(side=ctk.TOP, fill=ctk.Y, padx=10, pady=10, expand=True)
        add_btn.pack(side=ctk.BOTTOM, padx=10, pady=10)
        edit_btn.pack(side=ctk.BOTTOM, padx=10)
        self.section_box.pack(side=ctk.BOTTOM, padx=10, pady=10)
        right_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10, pady=10)

        self.term_caption_field.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
        bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.BOTH, padx=10, pady=10, expand=True)
        frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

    def __init__(self, master, on_update, geometry = '1000x600'):
        super().__init__(master)
        self.sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute() or []
        self.defaultFont = master.defaultFont
        self.title('Termer - Окно управления разделами')
        self.geometry(geometry)

        self.on_update = on_update

        self.__draw_term_info()
        self.__draw_term_list()


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
            self.defaultFont = master.defaultFont
            self.action_handler = action_handler

            label = ctk.CTkLabel(self, text='Выбор разделов', font=master.headerFont)
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

        def __draw_control_btns(self, make_open_toplevel):

            section_control_btn = ctk.CTkButton(self, text='База категорий', command=make_open_toplevel('section_control'), font=self.defaultFont)
            term_control_btn = ctk.CTkButton(self, text='База терминов', command=make_open_toplevel('term_control'), font=self.defaultFont)

            # section_control_btn.grid(row=0, column=0, padx=10, pady=(0, 5))
            # term_control_btn.grid(row=1, column=0, padx=10, pady=(5, 0))
            section_control_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=(0, 10))
            term_control_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)
            # frame.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

        def __init__(self, master, make_open_toplevel):
            super().__init__(master)
            self.defaultFont = master.defaultFont
            self.__mode = ctk.IntVar(master, 0)
            self.__count = ctk.StringVar(master, '5')

            label = ctk.CTkLabel(self, text='Настройка выборки', font=master.headerFont) # TODO: Сделать заголовки крупнее
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
        match name:
            case 'result': return self.__calculate_result
            case 'section_control': return self.__open_section_control
            case 'term_control': return self.__open_term_control
            case _: return None

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
        self.section_control = SectionControllWindow(self, self.__on_data_changed)

    def __open_term_control(self):
        if self.term_control:
            self.term_control.destroy()
        self.term_control = TermControllWindow(self, self.__on_data_changed)

    def __calculate_result(self):
        section_ids = self.left_part.get_selected_sections()
        count = self.right_part.get_count()
        mode = self.right_part.get_mode()

        if not count or count <= 0:
            showwarning('Termer - Операция невозможна!', 'Указано неверное кол-во терминов!')
            return

        terms: List[Term] = Term.select().where(
            (Term.section_id << section_ids) & Term.image.is_null(False)
        ).order_by(fn.random()).limit(count).execute()

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

        self.title('Termer - основное окно')
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
