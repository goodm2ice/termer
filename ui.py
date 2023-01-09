import customtkinter as ct
from typing import List, Tuple
from peewee import fn

from config import Config
from db import TextbookSection, Term


class ResultWindow(ct.CTkToplevel):
    def __init__(self, master, terms: List[Term], mode):
        super().__init__(master)
        self.title('Выборка терминов')
        self.geometry(f'400x{len(terms)*50}')

        for i, term in enumerate(terms):
            label = ct.CTkLabel(self, text=f'{i+1}. {term.caption}')
            label.pack()


class SectionControllWindow(ct.CTkToplevel):
    section_boxes = []
    section_list = None

    def draw_section_list(self):
        if self.section_list:
            self.section_list.destroy()
        self.section_list = ct.CTkFrame(self)

        sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute()

        self.section_boxes.clear()

        if not sections or len(sections) <= 0:
            label = ct.CTkLabel(self.section_list, text='Разделов нет!')
            label.pack(expand=True)
        else:
            self.section_boxes.clear()
            for section in sections:
                frame = ct.CTkFrame(self.section_list)
                var = ct.StringVar(frame, section.caption)

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

                entry = ct.CTkEntry(frame, textvariable=var)

                save_btn = ct.CTkButton(frame, text='Сохранить', command=save, fg_color='#FFAD33', hover_color='#C88A2F')
                remove_btn = ct.CTkButton(frame, text='Удалить', command=remove, fg_color='#D7324C', hover_color='#FF516D')

                self.section_boxes.append((section.section_id, var, entry))

                entry.pack(fill=ct.X, side=ct.LEFT, padx=5, pady=5, expand=True)
                save_btn.pack(anchor=ct.CENTER)
                remove_btn.pack(side=ct.RIGHT, padx=5, pady=5)
                frame.pack(fill=ct.X, padx=5, pady=5)

        self.section_list.pack(fill=ct.BOTH, expand=True, side=ct.TOP, pady=10)

    def __add_new_category(self):
        caption = ct.CTkInputDialog(text='Введите название нового раздела:', title='Добавление раздела')
        val = caption.get_input()
        if not val or val.strip() == '':
            return
        TextbookSection.create(caption=val.strip())
        self.draw_section_list()
        self.on_update()

    def __init__(self, on_update):
        super().__init__()
        self.on_update = on_update
        self.title('Окно управления разделами')
        self.geometry('500x600')

        self.draw_section_list()

        self.add_btn = ct.CTkButton(self, text='Добавить новый раздел', command=self.__add_new_category)
        self.add_btn.pack(side=ct.BOTTOM, fill=ct.X, padx=5, pady=5)


class TermControllWindow(ct.CTkToplevel):
    term_list_frame = None
    selected_id = None

    def draw_term_list(self):
        if self.term_list_frame:
            self.term_list_frame.destroy()
        self.term_list_frame = ct.CTkFrame(self)

        search_box = ct.CTkEntry(self.term_list_frame, placeholder_text='Введите текст для поиска', textvariable=self.search)

        term_list = ct.CTkFrame(self.term_list_frame)

        search_text = self.search.get().strip()
        terms = Term.select().where(Term.caption.concat(Term.description).contains(search_text)).order_by(Term.caption.desc()).execute()

        if not terms or len(terms) <= 0:
            label = ct.CTkLabel(term_list, text='Терминов нет!')
            label.pack(expand=True)
        else:
            for term in terms:
                item_frame = ct.CTkFrame(term_list)
                label = ct.CTkLabel(item_frame, text=term.caption)

                def select():
                    self.selected_id = term.term_id

                def remove():
                    if term.term_id == self.selected_id:
                        self.selected_id = None
                        self.draw_term_info()
                    term.delete_instance()
                    self.on_update()
                    self.draw_term_list()

                label.bind('<Button-1>', select)
                delete_btn = ct.CTkButton(item_frame, text='Удалить', command=remove, fg_color='#D7324C', hover_color='#FF516D')

                label.pack(side=ct.TOP, fill=ct.X, padx=5, pady=5, expand=True)
                delete_btn.pack(side=ct.BOTTOM, padx=5, pady=5)
                item_frame.pack(fill=ct.X, padx=5, pady=5)

        term_list.pack(side=ct.BOTTOM, fill=ct.BOTH, padx=10, pady=10, expand=True)
        search_box.pack(side=ct.TOP, fill=ct.X, padx=10, pady=10)
        self.term_list_frame.pack(side=ct.LEFT, fill=ct.BOTH, expand=True)

    def draw_term_info(self):
        frame = ct.CTkFrame(self)

        caption = ct.CTkEntry(frame)

        bottom_frame = ct.CTkFrame(frame)
        description = ct.CTkTextbox(bottom_frame)
        right_frame = ct.CTkFrame(bottom_frame)

        image = ct.CTkButton(right_frame, text='Нет изображения!')
        sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute()
        values = [] if not sections or len(sections) <= 0 else [section.caption for section in sections]
        section_box = ct.CTkComboBox(right_frame, values=values, variable=self.selected_section)

        description.pack(side=ct.LEFT, fill=ct.BOTH, padx=10, pady=10, expand=True)
        image.pack(side=ct.TOP, fill=ct.Y, padx=10, pady=10)
        section_box.pack(side=ct.BOTTOM, padx=10, pady=10)
        right_frame.pack(side=ct.RIGHT, fill=ct.Y, padx=10, pady=10)

        caption.pack(side=ct.TOP, fill=ct.X, padx=10, pady=10)
        bottom_frame.pack(side=ct.BOTTOM, fill=ct.BOTH, padx=10, pady=10, expand=True)
        frame.pack(side=ct.RIGHT, fill=ct.BOTH, expand=True)

    def __init__(self, on_update):
        super().__init__()
        self.search = ct.StringVar(self, None)
        self.selected_section = ct.StringVar(self, None)
        self.on_update = on_update

        self.draw_term_info()
        self.draw_term_list()


class SectionFrame(ct.CTkFrame):
    section_boxes: Tuple[int, ct.CTkCheckBox] = []
    section_list = None

    def get_selected_sections(self):
        return [id for (id,_) in self.section_boxes]

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
        self.section_list = ct.CTkFrame(self)

        sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute()

        self.section_boxes.clear()

        if not sections or len(sections) <= 0:
            label = ct.CTkLabel(self.section_list, text='Разделов нет!')
            label.pack(expand=True)
        else:
            for section in sections:
                box = ct.CTkCheckBox(self.section_list, text=section.caption, command=self.action_handler)
                self.section_boxes.append((section.section_id, box))
                box.pack(anchor='w', padx=10, pady=5)

        self.section_list.pack(fill=ct.BOTH, expand=True, side=ct.BOTTOM, pady=10)

    def __draw_section_btns(self):
        section_btns = ct.CTkFrame(self)
        select_all = ct.CTkButton(section_btns, text='Выделить всё', command=self.__select_all)
        deselect_all = ct.CTkButton(section_btns, text='Снять выделение', command=self.__deselect_all)
        select_all.pack(fill=ct.X, side=ct.LEFT, padx=5, pady=5, expand=True)
        deselect_all.pack(fill=ct.X, side=ct.RIGHT, padx=5, pady=5, expand=True)
        section_btns.pack(side=ct.TOP, fill=ct.X)

    def __init__(self, master, action_handler):
        super().__init__(master)
        self.action_handler = action_handler

        label = ct.CTkLabel(self, text='Выбор разделов')
        label.pack(fill=ct.X, side=ct.TOP)
        self.draw_section_list()
        self.__draw_section_btns()


class OptionsFrame(ct.CTkFrame):
    def get_mode(self):
        return self.__mode.get()

    def get_count(self):
        val = self.__count.get()
        if not val.isdigit():
            return None
        return int(val)

    def __draw_mode_selector(self):
        frame = ct.CTkFrame(self)

        label = ct.CTkLabel(frame, text='Выберите отображаемую часть термина')

        m1 = ct.CTkRadioButton(frame, text='Термин', variable=self.__mode, value=0)
        m2 = ct.CTkRadioButton(frame, text='Определение', variable=self.__mode, value=1)
        m3 = ct.CTkRadioButton(frame, text='Изображение', variable=self.__mode, value=2)

        label.pack(fill=ct.X, pady=5, padx=10)
        m1.pack(fill=ct.X, pady=2.5, padx=5)
        m2.pack(fill=ct.X, pady=2.5, padx=5)
        m3.pack(fill=ct.X, pady=2.5, padx=5)
        frame.pack(fill=ct.X, padx=10, ipady=5)

    def __draw_count_input(self):
        frame = ct.CTkFrame(self)

        label = ct.CTkLabel(frame, text='Укажите размер выборки (шт.)')
        self.count_input = ct.CTkEntry(frame, textvariable=self.__count) # TODO: Добавить отображение валидации
        # TODO: Добавить вызов action_handler при изменении текста

        label.pack(fill=ct.X, pady=5, padx=10)
        self.count_input.pack(fill=ct.X, padx=10)
        frame.pack(fill=ct.X, padx=10, ipady=5, pady=10)

    def __draw_control_btns(self, make_open_toplevel):
        frame = ct.CTkFrame(self)

        section_control_btn = ct.CTkButton(frame, text='База категорий', command=make_open_toplevel('section_control'))
        term_control_btn = ct.CTkButton(frame, text='База терминов', command=make_open_toplevel('term_control'))

        section_control_btn.pack(fill=ct.X, padx=10, pady=10)
        term_control_btn.pack(fill=ct.X, padx=10, pady=10)
        frame.pack(side=ct.BOTTOM, fill=ct.X, padx=10, pady=10)

    def __init__(self, master, make_open_toplevel):
        super().__init__(master)
        self.__mode = ct.IntVar(master, 0)
        self.__count = ct.StringVar(master, '5')

        label = ct.CTkLabel(self, text='Настройка выборки') # TODO: Сделать заголовки крупнее
        label.pack(fill=ct.X)

        self.__draw_mode_selector()
        self.__draw_count_input()
        self.__draw_control_btns(make_open_toplevel)
        
        self.result_btn = ct.CTkButton(self, text='Создать выборку', command=make_open_toplevel('result'), state='disabled')
        self.result_btn.pack(fill=ct.X, pady=5, padx = 10)



class TermerApp(ct.CTk):
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

    def __init__(self):
        super().__init__()

        self.title('Termer')
        self.geometry('800x600')

        self.left_part = SectionFrame(self, self.__on_options_changed)
        self.left_part.pack(side=ct.LEFT, fill=ct.BOTH, expand=True)

        self.right_part = OptionsFrame(self, self.make_open_toplevel, )
        self.right_part.pack(side=ct.RIGHT, fill=ct.BOTH)

    def __open_section_control(self):
        if self.section_control:
            self.section_control.destroy()
        self.section_control = SectionControllWindow(self.__on_data_changed)

    def __open_term_control(self):
        if self.term_control:
            self.term_control.destroy()
        self.term_control = TermControllWindow(self.__on_data_changed)

    def __calculate_result(self):
        section_ids = self.left_part.get_selected_sections()
        count = self.right_part.get_count()
        mode = self.right_part.get_mode()

        if not count or count <= 0:
            return

        terms: List[Term] = Term.select().where(Term.section_id in section_ids).order_by(fn.random()).limit(count).execute()

        if not terms or len(terms) <= 0:
            return

        if self.result_window:
            self.result_window.destroy()
        self.result_window = ResultWindow(self, terms, mode)


def prepare_app(config: Config):
    ct.set_appearance_mode(config.appearance_mode)
    ct.set_default_color_theme(config.color_theme)

    app = TermerApp()

    return app
