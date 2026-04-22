from testsam.clients.api_manager import ApiManager
from enum import Enum

class Roles(Enum):
    USER = "USER"
    PUBLIC = "PUBLIC"
    SUPER_ADMIN = "SUPER_ADMIN"

class User:
    def __init__(
            self,
            email: str,
            password: str,
            roles: list,
            api_manager: ApiManager
    ) -> None:
        self.email = email
        self.password = password
        self.roles = roles
        self.api_manager = api_manager # Сюда передаем экземпляр API Manager для запросов

    @property
    def creds(self):
        """Возвращает кортеж (email, password)"""
        return self.email, self.password