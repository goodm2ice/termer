import customtkinter as ctk
from typing import List

from db import Term


class TermList(ctk.CTkFrame):
    __item_boxes: List[ctk.CTkFrame] = []
    no_term_label = None

    def __first_draw(self, terms: List[Term]):
        if not terms or len(terms) <= 0:
            self.no_term_label = ctk.CTkLabel(self, text='Терминов нет!', font=self.defaultFont)
            self.no_term_label.pack(expand=True)
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
            self.no_term_label = ctk.CTkLabel(self, text='Терминов нет!', font=self.defaultFont)
            self.no_term_label.pack(expand=True)
        else:
            if self.no_term_label:
                self.no_term_label.destroy()
                self.no_term_label = None
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
                if on_select: on_select(term)
            return __on_select

        def make_on_remove(term):
            def __on_remove():
                if on_remove_click: on_remove_click(term)
            return __on_remove

        self.make_on_select = make_on_select
        self.make_on_remove_click = make_on_remove

        self.__first_draw(terms)
