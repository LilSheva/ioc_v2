import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime

class MainTab(ttk.Frame):
    """
    Класс для вкладки "Главная".
    Отвечает за выбор НЕСКОЛЬКИХ файлов, запуск анализа и отображение логов.
    """
    def __init__(self, parent):
        super().__init__(parent, padding="10")

        # --- 1. Секция выбора файлов ---
        file_frame = ttk.LabelFrame(self, text="1. Файлы для анализа")
        file_frame.pack(fill=X, padx=5, pady=5)
        
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=X, expand=True, padx=5, pady=5)
        
        self.file_listbox = tk.Listbox(list_frame, height=5, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=LEFT, fill=X, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill=X, padx=5, pady=(0, 5))
        
        self.browse_button = ttk.Button(button_frame, text="Добавить файлы...")
        self.browse_button.pack(side=LEFT)
        
        self.clear_button = ttk.Button(button_frame, text="Очистить список", bootstyle=DANGER)
        self.clear_button.pack(side=LEFT, padx=10)

        # --- 2. Секция запуска ---
        action_frame = ttk.LabelFrame(self, text="2. Запуск анализа")
        action_frame.pack(fill=X, padx=5, pady=5)
        
        self.run_button = ttk.Button(action_frame, text="Сформировать отчеты", bootstyle=SUCCESS)
        self.run_button.pack(pady=10)
        
        # --- 3. Секция логов ---
        log_frame = ttk.LabelFrame(self, text="Лог выполнения")
        log_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, wrap='word', font=("Courier New", 9))
        self.log_text.pack(fill=BOTH, expand=True, padx=5, pady=5)

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(END, full_message)
        self.log_text.see(END)
        self.update_idletasks()