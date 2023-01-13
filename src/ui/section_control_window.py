import customtkinter as ctk
from tkinter.filedialog import askopenfilename

from db import TextbookSection
from import_export import import_csv_sections


class SectionControllWindow(ctk.CTkToplevel):
    section_boxes = []
    section_list = None

    def __make_on_remove(self, section):
        def on_remove():
            section.delete_instance()
            self.draw_section_list()
            self.on_update()

        return on_remove

    def __make_on_save(self, section, var):
        def on_save():
            nval = var.get().strip()
            if nval == '':
                return
            section.section_id = section.section_id
            section.caption = nval
            section.save()
            self.draw_section_list()
            self.on_update()

        return on_save

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

                entry = ctk.CTkEntry(frame, textvariable=var, font=self.defaultFont)

                save_btn = ctk.CTkButton(frame, width=100, text='Сохранить', command=self.__make_on_save(section, var), fg_color='#FFAD33', hover_color='#C88A2F', font=self.defaultFont)
                remove_btn = ctk.CTkButton(frame, width=100, text='Удалить', command=self.__make_on_remove(section), fg_color='#D7324C', hover_color='#FF516D', font=self.defaultFont)

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

    def __on_import_click(self):
        filename = askopenfilename(filetypes=[('CSV', '*.csv')])
        if import_csv_sections(filename):
            self.draw_section_list()
            if self.on_update:
                self.on_update()

    def __init__(self, master, on_update, geometry = '700x600'):
        super().__init__(master)
        self.defaultFont = getattr(master, 'defaultFont', None)
        self.title('Termer - Окно управления разделами')
        self.geometry(geometry)

        self.on_update = on_update

        self.draw_section_list()

        self.import_btn = ctk.CTkButton(self, text='Импортировать CSV', command=self.__on_import_click, font=self.defaultFont)
        self.import_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

        self.add_btn = ctk.CTkButton(self, text='Добавить новый раздел', command=self.__add_new_category, font=self.defaultFont)
        self.add_btn.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=0)
