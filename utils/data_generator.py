import random
import uuid
import string
from faker import Faker
from typing import List, Any

faker = Faker()


class DataGenerator:


    # ========== REGISTER API ==========


    @staticmethod
    def generate_random_email() -> str:
        """Генерация случайного email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name() -> str:
        """Генерация случайного имени"""
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password() -> str:
        """
        Генерация пароля, соответствующего требованиям документации
        """
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    # ========== MOVIES API ==========

    @staticmethod
    def movie_data(name: str = None) -> dict[str, Any]:
        """Валидные данные для POST/PATCH"""
        return {
            "name": name or f"Movie_{uuid.uuid4().hex[:12]}",
            "description": faker.sentence(),
            "price": random.randint(1, 999999999),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 9)
        }

    @staticmethod
    def invalid_movie_data() -> List[dict[str, Any]]:
        """Невалидные данные для негативных тестов"""
        return [
            # Без name (обязательное)
            {"price": 150, "location": "MSK", "published": True, "genreId": 1},

            # Отрицательная цена
            {"name": "Test", "price": -10, "location": "MSK", "published": True, "genreId": 1},

            # Невалидная локация
            {"name": "Test", "price": 150, "location": "NYC", "published": True, "genreId": 1},

            # genreId не integer
            {"name": "Test", "price": 150, "location": "MSK", "published": True, "genreId": "abc"},

            # imageUrl не URL
            {"name": "Test", "price": 150, "imageUrl": "not-a-url", "location": "MSK", "published": True, "genreId": 1},

            # Пустые строки в имени
            {"name": "", "price": 150, "location": "MSK", "published": True, "genreId": 1}
        ]

    @staticmethod
    def movie_query_params() -> dict[str, Any]:
        """Query параметры для GET /movies"""
        min_price = random.randint(1, 999999999)
        max_price = random.randint(min_price, 999999999)

        return {
            "pageSize": random.randint(1, 20),
            "page": random.randint(1, 10),
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 9)
        }
    # ========== AUTH API ==========

    @staticmethod
    def user_data(email: str = None) -> dict[str, Any]:
        """Данные для регистрации/создания пользователя"""
        return {
            "email": email or DataGenerator.generate_random_email(),
            "name": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password()
        }
