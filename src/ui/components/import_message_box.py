from customtkinter import CTkButton, CTkFrame, CTkFont, CTkLabel, CTkOptionMenu, CTkToplevel, LEFT, RIGHT, X, CENTER, W
from tkinter.filedialog import askopenfilename

class ImportMessageBox(CTkToplevel):
    def __draw(self):
        self.__prompt_label = CTkLabel(self, anchor=W, text=self.prompt, font=self.defaultFont)
        self.__filename_label = CTkLabel(self, text='Файл не выбран!', font=self.defaultFont)
        self.__inputs_frame = CTkFrame(self)
        self.__encoding_selector = CTkOptionMenu(self.__inputs_frame, values=self.encodings, font=self.defaultFont)
        self.__encoding_selector.set(self.default_encoding)
        self.__select_file_btn = CTkButton(self.__inputs_frame, text='Выбрать файл', font=self.defaultFont, command=self.__on_select_file_click)
        self.__controls_frame = CTkFrame(self)
        self.__abort_btn = CTkButton(self.__controls_frame, text='Отмена', font=self.defaultFont, command=self.__on_abort_click)
        self.__ok_btn = CTkButton(self.__controls_frame, text='ОК', font=self.defaultFont, command=self.__on_ok_click, state='disabled')

        self.__prompt_label.pack(padx=10, pady=10)
        self.__encoding_selector.pack(side=RIGHT, fill=X)
        self.__select_file_btn.pack(side=LEFT, padx=(0, 10))
        self.__inputs_frame.pack(padx = 10, fill=X)
        self.__filename_label.pack(padx=10, pady=10)
        self.__ok_btn.pack(side=LEFT, padx=(0, 10))
        self.__abort_btn.pack(side=RIGHT, padx=10)
        self.__controls_frame.pack(anchor=CENTER)

    def __init__(
            self,
            master,
            on_ok,
            title = 'Импорт файла',
            prompt = 'Выберите файл и кодировку для импорта',
            filetypes = [('CSV', '*.csv')],
            encodings = ['utf-8', 'cp1252'],
            default_encoding = 'cp1252'
        ) -> None:
        super().__init__(master)
        self.on_ok = on_ok
        self.prompt = prompt
        self.encodings = encodings
        self.default_encoding = default_encoding
        self.filetypes = filetypes
        self.defaultFont = CTkFont('JetBrains Mono', 13)
        self.resizable(False, False)
        self.geometry('400x150+100+100')
        self.title(title)
        self.filename = None

        self.__draw()

    def __on_select_file_click(self):
        self.filename = askopenfilename(filetypes=self.filetypes)
        self.__filename_label.configure(text=self.filename if self.filename else 'Файл не выбран!')
        self.__ok_btn.configure(state='normal' if self.filename else 'disabled')

    def __on_ok_click(self):
        encoding = self.__encoding_selector.get()
        self.on_ok(self.filename, encoding)
        self.destroy()

    def __on_abort_click(self):
        self.destroy()
