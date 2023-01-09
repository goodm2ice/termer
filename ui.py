import customtkinter as ct
from typing import List, Tuple
from random import randint

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


class SectionFrame(ct.CTkFrame):
    section_boxes: Tuple[int, ct.CTkCheckBox] = []

    def get_selected_sections(self):
        return [id for (id,) in self.section_boxes]

    def __select_all(self):
        for (_, box) in self.section_boxes:
            box.select()

    def __deselect_all(self):
        for (_, box) in self.section_boxes:
            box.deselect()

    def __draw_section_list(self):
        section_list = ct.CTkFrame(self)

        sections = TextbookSection.select().order_by(TextbookSection.caption.desc()).execute()

        self.section_boxes.clear()

        for section in sections:
            box = ct.CTkCheckBox(section_list, text=section.caption)
            self.section_boxes.append((section.section_id, box))
            box.pack(anchor='w', padx=10, pady=5)

        section_list.pack(fill=ct.BOTH, expand=True, side=ct.BOTTOM)

    def __draw_section_btns(self):
        section_btns = ct.CTkFrame(self)
        select_all = ct.CTkButton(section_btns, text='Выделить всё', command=self.__select_all)
        deselect_all = ct.CTkButton(section_btns, text='Снять выделение', command=self.__deselect_all)
        select_all.pack(fill=ct.X, side=ct.LEFT, padx=5, pady=5, expand=True)
        deselect_all.pack(fill=ct.X, side=ct.RIGHT, padx=5, pady=5, expand=True)
        section_btns.pack(side=ct.TOP, fill=ct.X)

    def __init__(self, master):
        super().__init__(master)

        label = ct.CTkLabel(self, text='Выбор разделов')
        label.pack(fill=ct.X, side=ct.TOP)
        self.__draw_section_list()
        self.__draw_section_btns()


class OptionsFrame(ct.CTkFrame):
    def get_mode():
        pass

    def get_count():
        pass

    def __init__(self, master):
        super().__init__(master)

        label = ct.CTkLabel(self, text='Настройка выборки')
        label.pack(fill=ct.X, side=ct.TOP)



class TermerApp(ct.CTk):
    def __init__(self):
        super().__init__()

        self.title('Termer')
        self.geometry('800x600')

        def add_section():
            TextbookSection(caption=f'Секция #{randint(0, 1000)}').save()

        self.left_part = SectionFrame(self)
        self.left_part.pack(side=ct.LEFT, fill=ct.BOTH, expand=True)

        self.right_part = ct.CTkFrame(self)

        self.right_part.pack(side=ct.RIGHT, fill=ct.BOTH)

        # self.result_btn = ct.CTkButton(self, text="Создать выборку", command=self.calculate_result)
        # self.result_btn.pack()

    def __calculate_result(self):
        section_ids = self.left_part.get_selected_sections()
        ResultWindow(self, [
            Term(term_id=1, caption="Термин 1"),
            Term(term_id=2, caption="Термин 2"),
            Term(term_id=3, caption="Термин 3"),
        ], 'caption')
        


def prepare_app(config: Config):
    ct.set_appearance_mode(config.appearance_mode)
    ct.set_default_color_theme(config.color_theme)

    app = TermerApp()

    return app
