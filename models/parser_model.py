import asyncio
from dataclasses import dataclass, asdict
from typing import Callable, Coroutine, Any
import httpx
from bs4 import BeautifulSoup

@dataclass
class ItemModel:
    """Модель даних для одного спарсеного елемента."""
    title: str
    price: str
    link: str

class TargetSiteParser:
    """Основний двигун парсингу, ізольований від UI логіки."""
    def __init__(self, config: dict):
        self.config = config
        # Створюємо асинхронний клієнт з налаштуваннями таймауту
        timeout = float(config.get("timeout", 10))
        self.client = httpx.AsyncClient(timeout=timeout, follow_redirects=True)

    async def fetch_page(self, url: str) -> str:
        """Асинхронне завантаження HTML контенту."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = await self.client.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def extract_data(self, html: str) -> list[ItemModel]:
        """Чиста логіка парсингу HTML. Не містить асинхронних викликів."""
        soup = BeautifulSoup(html, "html.parser")
        parsed_items = []
        
        # Демонстраційний пошук карток товарів чи новин.
        # Для тесту можна передавати посилання на сайти з тегами <a> або статтями.
        # Тут прописана гнучка логіка фоллбеку, якщо парсимо довільний сайт.
        items_html = soup.find_all(["div", "article", "li"], class_=True) or soup.find_all("a")
        
        for index, element in enumerate(items_html[:5]):  # Беремо до 5 елементів з кожної сторінки
            title = element.get_text(strip=True) or f"Елемент #{index}"
            # Імітуємо ціну або беремо атрибут
            price = "Не вказано" 
            link = element.get("href") or element.find("a").get("href") if element.find("a") else "#"
            
            if len(title) > 50:
                title = title[:47] + "..."
                
            parsed_items.append(ItemModel(title=title, price=price, link=link))
            
        return parsed_items

    async def start_parsing(
        self, 
        urls: list[str], 
        on_progress: Callable[[float, str], Coroutine[Any, Any, None]]
    ) -> list[ItemModel]:
        """Головний керуючий цикл парсера. Приймає асинхронний callback для прогресу."""
        all_results = []
        total_urls = len(urls)

        for index, url in enumerate(urls, start=1):
            if not url.strip():
                continue
            try:
                progress_percentage = index / total_urls
                await on_progress(progress_percentage, f"Завантаження сторінки: {url}")
                
                html = await self.fetch_page(url)
                items = self.extract_data(html)
                all_results.extend(items)
                
                await on_progress(progress_percentage, f"Успішно спарсено елементів: {len(items)}")
                # Пауза між запитами, щоб уникнути блокувань
                await asyncio.sleep(1.5)
                
            except Exception as e:
                await on_progress(index / total_urls, f"Помилка під час обробки {url}: {str(e)}")
                await asyncio.sleep(1)

        await self.client.aclose()
        return all_results
