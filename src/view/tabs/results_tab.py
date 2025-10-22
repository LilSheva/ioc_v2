import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ResultsTab(ttk.Frame):
    """
    Класс для вкладки "Результаты запросов".
    Отображает интерактивную таблицу со сгенерированными запросами.
    """
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        
        # --- Прокручиваемая область для результатов ---
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Переменные для хранения виджетов, к которым нужен доступ
        self.copy_buttons = []
        self.checkbox_vars = []

    def populate_results(self, query_data, ioc_config):
        """
        Очищает и заново строит таблицу с результатами.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.copy_buttons.clear()
        self.checkbox_vars.clear()

        # Заголовки таблицы
        headers = ["Имя", "Система", "Инфо", "-", "Выполнено"]
        for i, header in enumerate(headers):
            ttk.Label(self.scrollable_frame, text=header, font=('Helvetica', 10, 'bold')).grid(row=0, column=i, sticky='w', padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)
        
        row_idx = 1
        sorted_keys = sorted(query_data.keys(), key=lambda k: ioc_config.get(k, {}).get("priority", 999))

        for name in sorted_keys:
            items = query_data.get(name, [])
            if not items:
                continue

            # Объединенная ячейка с названием IOC
            name_label = ttk.Label(self.scrollable_frame, text=name, font=('Helvetica', 10, 'bold'))
            name_label.grid(row=row_idx, column=0, rowspan=len(items), sticky='ns', padx=5, pady=5)
            
            for i, item in enumerate(items):
                ttk.Label(self.scrollable_frame, text=item['system']).grid(row=row_idx + i, column=1, sticky='w', padx=5)
                
                info_entry = ttk.Entry(self.scrollable_frame, width=100)
                info_entry.insert(0, item['query'])
                info_entry.config(state='readonly')
                info_entry.grid(row=row_idx + i, column=2, sticky='ew', padx=5, pady=2)
                
                checkbox_var = tk.BooleanVar(value=True)
                
                copy_button = ttk.Button(self.scrollable_frame, text="Копировать")
                # Здесь мы сохраняем entry и checkbox_var для использования в контроллере
                self.copy_buttons.append((copy_button, info_entry, checkbox_var))
                copy_button.grid(row=row_idx + i, column=3, padx=5)
                
                ttk.Checkbutton(self.scrollable_frame, variable=checkbox_var).grid(row=row_idx + i, column=4, padx=5)
            
            row_idx += len(items)
            ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=row_idx, column=0, columnspan=5, sticky='ew', pady=10)
            row_idx += 1