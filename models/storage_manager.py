import os
import json
from dataclasses import asdict
from models.parser_model import ItemModel

class StorageManager:
    """Відповідає виключно за операції з файловою системою."""
    
    @staticmethod
    def save_results_to_json(data: list[ItemModel], filepath: str = "results.json") -> str:
        """Перетворює об'єкти моделей у JSON-масив та зберігає на диск."""
        dict_data = [asdict(item) for item in data]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dict_data, f, ensure_ascii=False, indent=4)
        return os.path.abspath(filepath)

    @staticmethod
    def load_config(filepath: str = "config/settings.json") -> dict:
        """Зчитує конфіг програми. Повертає дефолтні значення у разі відсутності."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "timeout": "10",
                "urls": "https://ycombinator.com\nhttps://pypi.org"
            }

    @staticmethod
    def save_config(config_data: dict, filepath: str = "config/settings.json"):
        """Зберігає поточні налаштування з GUI у файл конфігурації."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
