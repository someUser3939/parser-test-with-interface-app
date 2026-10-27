import flet as ft
from controllers.main_controller import MainController
from views.main_view import MainView

def main(page: ft.Page):
    # 1. Ініціалізуємо контролер, передаючи йому контекст сторінки Flet
    controller = MainController(page)
    
    # 2. Створюємо View та передаємо йому контролер для зв'язку подій
    view = MainView(page, controller)
    
    # 3. Будуємо інтерфейс
    view.build_ui()

if __name__ == "__main__":
    # Запуск Flet додатка (як десктопне вікно)
    ft.app(target=main)
