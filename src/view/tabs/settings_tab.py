import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class SettingsTab(ttk.Frame):
    """
    Класс для вкладки "Настройка IOC".
    Динамически создает виджеты для управления каждым типом IOC с возможностью сортировки.
    """
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        
        top_button_frame = ttk.Frame(self)
        top_button_frame.pack(side=TOP, fill=X, pady=5)
        
        self.save_button = ttk.Button(top_button_frame, text="Сохранить все настройки", bootstyle=SUCCESS)
        self.save_button.pack(side=RIGHT)
        
        self.add_button = ttk.Button(top_button_frame, text="Добавить новый IOC", bootstyle=INFO)
        self.add_button.pack(side=LEFT)
        
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.ioc_widgets = {}
        # Списки для кнопок сортировки, которые будет использовать контроллер
        self.move_up_buttons = []
        self.move_down_buttons = []

    def populate_settings(self, ioc_config_dict):
        """
        Очищает и заново строит все виджеты настроек на основе словаря конфига.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.ioc_widgets = {}
        self.move_up_buttons.clear()
        self.move_down_buttons.clear()
        
        # Теперь порядок блоков определяется порядком элементов в словаре
        for name, data in ioc_config_dict.items():
            self._add_ioc_widget(name, data)

    def _add_ioc_widget(self, name, data):
        """
        Создает блок виджетов для одного типа IOC, включая кнопки сортировки.
        """
        frame = ttk.LabelFrame(self.scrollable_frame, text=name, padding=10)
        frame.pack(fill=X, padx=5, pady=5, expand=True)
        
        widgets = {}
        
        # --- Панель управления (Вкл/Выкл и стрелки) ---
        control_frame = ttk.Frame(frame)
        control_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)

        widgets["enabled"] = tk.BooleanVar(value=data.get("enabled", True))
        ttk.Checkbutton(control_frame, text="Включено", variable=widgets["enabled"]).pack(side=LEFT)
        
        # --- Кнопки-стрелки для сортировки ---
        sort_frame = ttk.Frame(control_frame)
        sort_frame.pack(side=RIGHT)

        move_up_btn = ttk.Button(sort_frame, text="▲", width=3)
        move_up_btn.pack(side=LEFT, padx=(0, 2))
        self.move_up_buttons.append((move_up_btn, name)) # Сохраняем кнопку и имя IOC

        move_down_btn = ttk.Button(sort_frame, text="▼", width=3)
        move_down_btn.pack(side=LEFT)
        self.move_down_buttons.append((move_down_btn, name)) # Сохраняем кнопку и имя IOC
        
        # --- Остальные поля ---
        ttk.Label(frame, text="Регулярное выражение:").grid(row=1, column=0, sticky='w')
        widgets["regex"] = tk.StringVar(value=data.get("regex", "")); 
        ttk.Entry(frame, textvariable=widgets["regex"], width=80).grid(row=1, column=1, sticky='ew', pady=2)
        
        rt = data.get("report_template", {})
        ttk.Label(frame, text="Тип в отчете:").grid(row=2, column=0, sticky='w')
        widgets["type"] = tk.StringVar(value=rt.get("Тип Индикатора", "")); 
        ttk.Entry(frame, textvariable=widgets["type"]).grid(row=2, column=1, sticky='ew', pady=2)
        
        ttk.Label(frame, text="Статус NTA:").grid(row=3, column=0, sticky='w')
        widgets["nta"] = tk.StringVar(value=rt.get("Статус Активности NTA", "")); 
        ttk.Entry(frame, textvariable=widgets["nta"]).grid(row=3, column=1, sticky='ew', pady=2)
        
        ttk.Label(frame, text="Статус SIEM (MP):").grid(row=4, column=0, sticky='w')
        widgets["siem_mp"] = tk.StringVar(value=rt.get("Статус Активности SIEM (MP)", "")); 
        ttk.Entry(frame, textvariable=widgets["siem_mp"]).grid(row=4, column=1, sticky='ew', pady=2)
        
        qt = data.get("query_templates", {"MP10": [], "NAD": []})
        ttk.Label(frame, text="Шаблоны MP10:").grid(row=5, column=0, sticky='nw', pady=5)
        widgets["mp10_queries"] = tk.Text(frame, height=3, width=80, font=("Courier New", 9))
        widgets["mp10_queries"].grid(row=5, column=1, sticky='ew', pady=2)
        widgets["mp10_queries"].insert("1.0", "\n".join(qt.get("MP10", [])))
        
        ttk.Label(frame, text="Шаблоны NAD:").grid(row=6, column=0, sticky='nw', pady=5)
        widgets["nad_queries"] = tk.Text(frame, height=3, width=80, font=("Courier New", 9))
        widgets["nad_queries"].grid(row=6, column=1, sticky='ew', pady=2)
        widgets["nad_queries"].insert("1.0", "\n".join(qt.get("NAD", [])))
        
        frame.grid_columnconfigure(1, weight=1)
        self.ioc_widgets[name] = widgets