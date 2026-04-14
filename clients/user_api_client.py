from testsam.customer_requester.custom_requester import CustomRequester
from requests import Response, Session

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")
        self.session = session

    def get_user_info(self, user_id: int, expected_status: int = 200) -> Response:
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )


    def delete_user(self, user_id: int, expected_status = 204) -> Response:
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )



    def clean_up_user(self, user_id: int) -> Response | None:
        """"
        Очистка данных после тестов
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=None # НЕ проверяем ответ
        )