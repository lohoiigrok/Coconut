from customer_requester.custom_requester import CustomRequester
from requests import Response
from config import REGISTER_ENDPOINT
from types.common_types import UserData

class UserApi(CustomRequester):
    """
    Класс для работы с API пользователей.
    """
    def __init__(self, session):
        self.session = session
        super().__init__(session, "https://auth.dev-cinescope.coconutqa.ru/")

    def get_user_info(self, user_id: int, expected_status: int = 200) -> Response:
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method = "GET",
            endpoint = f"/users/{user_id}",
            expected_status = expected_status
        )

    def create_user(self, user_data: UserData, expected_status: int = 201) -> Response:
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method = "POST",
            endpoint = REGISTER_ENDPOINT,
            data = user_data,
            expected_status = expected_status
        )

    def delete_user(self, user_id: int, expected_status: int = 204) -> Response:
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method = "DELETE",
            endpoint = f"/user/{user_id}",
            expected_status = expected_status
        )

    def create_user_admin(self, user_data: UserData, expected_status: int = 201) -> Response:
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status,
        )

    def clean_up_user(self, user_id: int) -> Response | None:
        """"
        Очистка данных после тестов
        :param user_id: ID пользователя.
        """
        try:
            self.delete_user(user_id, expected_status=200)
        except ValueError:
            # Для ситуаций где пользователь уже удален или не найден (404)
            pass