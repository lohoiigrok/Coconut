from typing import Dict, Any
from testsam.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from testsam.customer_requester.custom_requester import CustomRequester
import requests

class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
      """

    def __init__(self, session: requests.Session) -> None:
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")

    def register_user(self, user_data: dict[str, Any], expected_status: int=201) -> requests.Response:
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data: dict[str, Any], expected_status: int=200) -> requests.Response:
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds: list[str] | tuple[str, str]) -> dict[str, Any]:
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()

        if "accessToken" not in response:
            raise KeyError("token is missing")
        token = response["accessToken"]
        self._update_session_headers(**{"Authorization": "Bearer " + token})

        return response
