import flet as ft
from controllers.main_controller import MainController

class MainView:
    """Рівень представлення. Описує графічні елементи вікна."""
    def __init__(self, page: ft.Page, controller: MainController):
        self.page = page
        self.controller = controller
        self.controller.set_view(self)
        
        # Ініціалізація UI компонентів
        self.urls_input = ft.TextField(
            label="Список посилань (кожне з нового рядка)",
            multiline=True,
            min_lines=4,
            max_lines=6,
            hint_text="https://example.com"
        )
        
        self.timeout_input = ft.TextField(
            label="Таймаут запиту (сек)",
            value="10",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200
        )
        
        self.btn_start = ft.Button(
            content="Запустити парсинг",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700),
            on_click=self.controller.start_parsing_process
        )
        
        self.progress_bar = ft.ProgressBar(value=0, width=None, color="blue")
        
        self.log_box = ft.ListView(
            expand=True,
            spacing=5,
            padding=10,
            auto_scroll=True
        )

    def build_ui(self):
        """Компонує вікно додатка та додає елементи на сторінку."""
        self.page.title = "Async JSON Parser (Flet Architectural Template)"
        self.page.window.width = 700
        self.page.window.height = 600
        self.page.theme_mode = ft.ThemeMode.DARK

        # Панель налаштувань
        config_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Налаштування парсера", size=18, weight=ft.FontWeight.BOLD),
                    self.urls_input,
                    self.timeout_input,
                    ft.Row([self.btn_start], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=15
            )
        )

        # Контейнер для логів
        log_card = ft.Card(
            expand=True,
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Логи виконання процесу", size=14, weight=ft.FontWeight.W_500),
                    self.progress_bar,
                    ft.Container(
                        content=self.log_box,
                        border=ft.Border.all(1, ft.Colors.GREY_700),
                        border_radius=5,
                        bgcolor=ft.Colors.BLACK_26,
                        expand=True
                    )
                ]),
                padding=15
            )
        )

        # Додавання на головний екран
        self.page.add(
            ft.Column([config_card, log_card], expand=True)
        )
        
        # Завантажуємо початкові дані через контролер
        self.controller.load_initial_settings()

    def append_log(self, text: str):
        """Метод безпечного додавання текстового логу в контейнер."""
        self.log_box.controls.append(ft.Text(f"• {text}", size=12, color=ft.Colors.GREY_300))
        # Обмежуємо кількість збережених UI елементів логу для уникнення витоку пам'яті
        if len(self.log_box.controls) > 150:
            self.log_box.controls.pop(0)
