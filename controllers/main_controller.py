import asyncio
import flet as ft
from models.parser_model import TargetSiteParser
from models.storage_manager import StorageManager

class MainController:
    """Контролер, що керує взаємодією між View та Model."""
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = None  # Встановлюється при ініціалізації View

    def set_view(self, view):
        self.view = view

    def load_initial_settings(self):
        """Завантажує налаштування та відображає їх у полях введення."""
        config = StorageManager.load_config()
        self.view.urls_input.value = config.get("urls", "")
        self.view.timeout_input.value = config.get("timeout", "10")
        self.page.update()

    def start_parsing_process(self, e):
        """Тригер кнопки 'Старт'. Запускає асинхронний таск, щоб не блокувати UI."""
        # Блокуємо елементи інтерфейсу під час роботи
        self.view.btn_start.disabled = True
        self.view.urls_input.disabled = True
        self.view.timeout_input.disabled = True
        self.view.progress_bar.value = 0
        self.view.log_box.controls.clear()
        self.view.append_log("Ініціалізація парсингу...")
        self.page.update()

        # Зберігаємо налаштування перед запуском
        current_config = {
            "timeout": self.view.timeout_input.value,
            "urls": self.view.urls_input.value
        }
        StorageManager.save_config(current_config)

        # Запускаємо довготривалу задачу в асинхронному пулі задач Flet
        self.page.run_task(self._async_parsing_task, current_config)

    async def _async_parsing_task(self, config: dict):
        """Приватний асинхронний метод виконання самого парсингу."""
        urls = [url.strip() for url in config.get("urls", "").split("\n") if url.strip()]
        
        if not urls:
            self.view.append_log("Помилка: Список URL-адрес порожній!")
            self._reset_ui_state()
            return

        parser = TargetSiteParser(config)
        
        # Функція зворотного зв'язку, яку викликає модель для оновлення GUI
        async def progress_callback(progress_value: float, message: str):
            self.view.progress_bar.value = progress_value
            self.view.append_log(message)
            self.page.update()

        # Запуск бізнес логіки збору даних
        results = await parser.start_parsing(urls, on_progress=progress_callback)

        if results:
            self.view.append_log(f"Збір завершено. Запис {len(results)} елементів у JSON...")
            path = StorageManager.save_results_to_json(results)
            self.view.append_log(f"Результати збережено за шляхом: {path}")
        else:
            self.view.append_log("Процес завершився. Жодного елемента не було зібрано.")

        self._reset_ui_state()

    def _reset_ui_state(self):
        """Повертає елементи UI в активний стан."""
        self.view.btn_start.disabled = False
        self.view.urls_input.disabled = False
        self.view.timeout_input.disabled = False
        self.page.update()
