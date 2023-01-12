import customtkinter as ctk
from typing import List

from db import Term
from utils import blob_to_image


class ResultWindow(ctk.CTkToplevel):
    def __init__(self, master, terms: List[Term], mode):
        super().__init__(master)
        self.defaultFont = ctk.CTkFont('JetBrains Mono', 20)
        self.title('Выборка терминов')
        width, item_height = 600, 95
        if mode == 0:
            width = 500
        elif mode == 1:
            item_height = 150
        elif mode == 2:
            item_height = 270
        self.geometry(f'{width}x{max(len(terms) * item_height, 500)}')

        for i, term in enumerate(terms):
            frame = ctk.CTkFrame(self)
            label = ctk.CTkLabel(frame, text=f'№{i+1}:', font=self.defaultFont)
            value = None
            if mode == 0:
                value = ctk.CTkLabel(frame, font=self.defaultFont, text=term.caption)
            elif mode == 1:
                value = ctk.CTkLabel(frame, font=self.defaultFont, text=str(term.description).rstrip(), justify=ctk.LEFT, wraplength=520)
            elif mode == 2:
                if term.image:
                    value = ctk.CTkLabel(frame, image=blob_to_image(term.image, 520, 200), text='')
                else:
                    value = ctk.CTkLabel(frame, font=self.defaultFont, text='Нет изображения!')

            label.pack(side=ctk.TOP, anchor=ctk.NW, padx=10, pady=(5, 15))
            value.pack(side=ctk.BOTTOM, anchor=ctk.SW, padx=(50, 10), pady=(0, 10))
            frame.pack(padx=10, pady=(10 if i == 0 else 0, 10), fill=ctk.X)
