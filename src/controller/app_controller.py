from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime
import collections
from pathlib import Path

class AppController:
    """
    Класс-контроллер. Связывает View (интерфейс) и Model (логику).
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._init_view()
        self._bind_events()

    def _init_view(self):
        """
        Первоначальная загрузка данных из модели в представление.
        """
        ioc_config = self.model['config'].get_ioc_types()
        self.view.settings_tab.populate_settings(ioc_config)
        self._bind_settings_tab_events()
        self.view.log("Приложение готово к работе.")

    def _bind_events(self):
        """
        Привязывает основные обработчики событий к статическим виджетам.
        """
        # --- Вкладка "Главная" ---
        self.view.main_tab.browse_button.config(command=self._handle_browse_files)
        self.view.main_tab.clear_button.config(command=self._handle_clear_files)
        self.view.main_tab.run_button.config(command=self._handle_run_analysis)
        
        # --- Вкладка "Настройка IOC" ---
        self.view.settings_tab.save_button.config(command=self._handle_save_config)
        self.view.settings_tab.add_button.config(command=self._handle_add_ioc)

    def _bind_settings_tab_events(self):
        """
        Привязывает события к динамически созданным кнопкам на вкладке настроек.
        """
        for button, name in self.view.settings_tab.move_up_buttons:
            button.config(command=lambda n=name: self._handle_move_ioc(n, direction=-1))
        
        for button, name in self.view.settings_tab.move_down_buttons:
            button.config(command=lambda n=name: self._handle_move_ioc(n, direction=1))

    # --- Обработчики событий (Handlers) ---

    def _handle_browse_files(self):
        """
        Обрабатывает нажатие кнопки "Добавить файлы...".
        """
        filepaths = filedialog.askopenfilenames(
            title="Выберите один или несколько .docx файлов",
            filetypes=(("Документы Word", "*.docx"), ("Все файлы", "*.*"))
        )
        if filepaths:
            listbox = self.view.main_tab.file_listbox
            current_files = set(listbox.get(0, "end"))
            for path in filepaths:
                if path not in current_files:
                    listbox.insert("end", path)
                    self.view.log(f"Добавлен файл: {Path(path).name}")

    def _handle_clear_files(self):
        """
        Обрабатывает нажатие кнопки "Очистить список".
        """
        self.view.main_tab.file_listbox.delete(0, "end")
        self.view.log("Список файлов очищен.")

    def _handle_run_analysis(self):
        """
        Обрабатывает нажатие кнопки "Сформировать отчеты".
        """
        filepaths = self.view.main_tab.file_listbox.get(0, "end")
        if not filepaths:
            messagebox.showerror("Ошибка", "Пожалуйста, добавьте хотя бы один файл для анализа.")
            return

        # --- Диалог сохранения файла ---
        output_xlsx_path = filedialog.asksaveasfilename(
            title="Сохранить отчет Excel как...",
            defaultextension=".xlsx",
            initialfile=f"итог_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx",
            filetypes=[("Excel-файл", "*.xlsx"), ("Все файлы", "*.*")]
        )
        if not output_xlsx_path:
            self.view.log("Операция сохранения отменена пользователем.")
            return

        output_path = Path(output_xlsx_path)
        txt_filepath = output_path.with_name(f"{output_path.stem}_queries.txt")

        self.view.log("Начало анализа...")
        
        ioc_config = self.model['config'].get_ioc_types()
        found_iocs = self.model['parser'].extract_all_iocs(filepaths, ioc_config)
        
        if not found_iocs:
            self.view.log("Анализ завершен. Индикаторы не найдены.")
            messagebox.showinfo("Завершено", "Индикаторы компрометации в файлах не найдены.")
            return
            
        self.view.log(f"Найдено {sum(len(v) for v in found_iocs.values())} уникальных индикаторов.")

        reporter = self.model['reporter']
        query_data = reporter.generate_query_data(found_iocs, ioc_config)
        
        self.view.results_tab.populate_results(query_data, ioc_config)
        for button, entry, var in self.view.results_tab.copy_buttons:
            button.config(command=lambda e=entry, v=var: self._handle_copy_to_clipboard(e, v))
            
        success_xlsx, msg_xlsx = reporter.create_xlsx_report(output_xlsx_path, found_iocs, ioc_config)
        self.view.log(msg_xlsx)
        
        success_txt, msg_txt = reporter.create_query_file(txt_filepath, query_data, ioc_config)
        self.view.log(msg_txt)
        
        self.view.log("Анализ успешно завершен.")
        messagebox.showinfo("Готово", f"Отчеты успешно сохранены:\n{output_xlsx_path}\n{txt_filepath}")
        
        self.view.switch_to_results_tab()

    def _handle_save_config(self):
        """
        Обрабатывает нажатие кнопки "Сохранить все настройки".
        """
        gui_order = [name for _, name in self.view.settings_tab.move_up_buttons]
        updated_config_data = collections.OrderedDict()
        
        for name in gui_order:
            widgets = self.view.settings_tab.ioc_widgets[name]
            updated_config_data[name] = {
                "enabled": widgets["enabled"].get(),
                "regex": widgets["regex"].get(),
                "report_template": {
                    "Тип Индикатора": widgets["type"].get(),
                    "Статус Активности NTA": widgets["nta"].get(),
                    "Статус Активности SIEM (MP)": widgets["siem_mp"].get()
                },
                "query_templates": {
                    "MP10": [line for line in widgets["mp10_queries"].get("1.0", "end-1c").strip().split('\n') if line],
                    "NAD": [line for line in widgets["nad_queries"].get("1.0", "end-1c").strip().split('\n') if line]
                }
            }
        
        self.model['config'].update_ioc_types(updated_config_data)
        self.model['config'].save()
        self.view.log("Конфигурация успешно сохранена.")
        messagebox.showinfo("Сохранено", "Настройки успешно сохранены в файл config.txt.")
        
        self.view.settings_tab.populate_settings(updated_config_data)
        self._bind_settings_tab_events()

    def _handle_add_ioc(self):
        """
        Обрабатывает нажатие кнопки "Добавить новый IOC".
        """
        name = simpledialog.askstring("Новый IOC", "Введите системное имя нового IOC (например, Mutex):", parent=self.view)
        
        config = self.model['config'].get_ioc_types()
        
        if name and name not in config:
            new_ioc_data = {
                "enabled": True,
                "regex": "Your Regex Here",
                "report_template": {"Тип Индикатора": name, "Статус Активности NTA": "", "Статус Активности SIEM (MP)": ""},
                "query_templates": {"MP10": [], "NAD": []}
            }
            config[name] = new_ioc_data
            self.model['config'].update_ioc_types(config)
            
            self.view.settings_tab.populate_settings(config)
            self._bind_settings_tab_events()
            self.view.log(f"Добавлен новый тип IOC: {name}. Не забудьте настроить и сохранить.")
        elif name:
            messagebox.showerror("Ошибка", "IOC с таким системным именем уже существует.", parent=self.view)

    def _handle_copy_to_clipboard(self, entry, var):
        """
        Обрабатывает нажатие кнопок "Копировать" на вкладке результатов.
        """
        self.view.clipboard_clear()
        self.view.clipboard_append(entry.get())
        self.view.log(f"Скопировано: \"{entry.get()[:70]}...\"")
        var.set(False)

    def _handle_move_ioc(self, ioc_name, direction):
        """
        Обрабатывает перемещение блока IOC вверх (direction=-1) или вниз (direction=1).
        """
        config_dict = self.model['config'].get_ioc_types()
        keys = list(config_dict.keys())
        
        try:
            current_index = keys.index(ioc_name)
        except ValueError:
            return

        new_index = current_index + direction
        
        if 0 <= new_index < len(keys):
            keys.insert(new_index, keys.pop(current_index))
            
            new_ordered_dict = collections.OrderedDict()
            for key in keys:
                new_ordered_dict[key] = config_dict[key]
            
            self.model['config'].update_ioc_types(new_ordered_dict)
            
            self.view.settings_tab.populate_settings(new_ordered_dict)
            self._bind_settings_tab_events()