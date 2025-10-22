import sys
from pathlib import Path

# Класс-заглушка для перенаправления вывода в бесконсольном режиме
class Redirect:
    def __init__(self):
        pass

    def write(self, *args, **kwargs):
        # Просто игнорируем все попытки записи
        pass

    def flush(self, *args, **kwargs):
        # Игнорируем попытки "сбросить буфер"
        pass

# Проверяем, существуют ли стандартные потоки вывода.
# В скомпилированном .exe без консоли (`--windowed`) они могут быть None.
if sys.stdout is None:
    sys.stdout = Redirect()
if sys.stderr is None:
    sys.stderr = Redirect()


# Добавляем корневую папку проекта в путь, чтобы можно было импортировать из src
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# --- Основные импорты из модулей ---
from src.model.config_manager import ConfigManager
from src.model.ioc_parser import IOCParser
from src.model.report_generator import ReportGenerator
from src.view.main_view import MainView
from src.controller.app_controller import AppController

def main():
    """
    Главная функция для инициализации и запуска приложения.
    """
    # 1. Создаем экземпляры всех компонентов Модели (Model)
    config_manager = ConfigManager()
    ioc_parser = IOCParser()
    report_generator = ReportGenerator()
    
    # Собираем все части модели в один словарь для удобства передачи
    model = {
        "config": config_manager,
        "parser": ioc_parser,
        "reporter": report_generator
    }

    # 2. Создаем экземпляр главного окна (View)
    # Тема 'flatly' - одна из многих красивых тем ttkbootstrap.
    # Другие варианты: 'darkly', 'superhero', 'cyborg', 'vapor' и т.д.
    view = MainView(theme="superhero")

    # 3. Создаем экземпляр Контроллера и связываем его с Моделью и Представлением
    controller = AppController(model, view)

    # 4. Запускаем главный цикл приложения
    view.mainloop()

if __name__ == "__main__":
    main()