import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Импортируем классы для каждой из наших будущих вкладок
from src.view.tabs.main_tab import MainTab
from src.view.tabs.settings_tab import SettingsTab
from src.view.tabs.results_tab import ResultsTab

class MainView(ttk.Window):
    """
    Главное окно приложения.
    Наследуется от ttkbootstrap.Window для применения современных тем.
    Создает и управляет основными вкладками интерфейса.
    """
    def __init__(self, theme='flatly'):
        # Инициализируем окно с выбранной темой
        super().__init__(themename=theme)

        # --- Базовые настройки окна ---
        self.title("Парсер Индикаторов Компрометации")
        self.geometry("1100x800")
        self.minsize(800, 600) # Устанавливаем минимальный размер окна

        # --- Создание системы вкладок (Notebook) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # --- Создание экземпляров каждой вкладки ---
        # Мы передаем self.notebook в каждую вкладку, чтобы она знала, где ей размещаться
        self.main_tab = MainTab(self.notebook)
        self.settings_tab = SettingsTab(self.notebook)
        self.results_tab = ResultsTab(self.notebook)

        # --- Добавление вкладок в Notebook ---
        self.notebook.add(self.main_tab, text="Главная")
        self.notebook.add(self.settings_tab, text="Настройка IOC")
        self.notebook.add(self.results_tab, text="Результаты запросов")

    def log(self, message):
        """
        Прокси-метод для удобного доступа к логу из контроллера.
        Перенаправляет вызов в соответствующий метод на главной вкладке.
        """
        self.main_tab.log(message)

    def switch_to_results_tab(self):
        """
        Метод для программного переключения на вкладку с результатами.
        """
        self.notebook.select(self.results_tab)