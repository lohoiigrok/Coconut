from testsam.clients.api_manager import ApiManager

class TestNegativeAuthAPI(ApiManager):

    def test_invalid_pass_auth(self, api_manager, test_user):
        # Отправка запроса на авторизацию
        invalid_login_data = {"email": test_user["email"], "password": "Dsdjods32d"}
        response = api_manager.auth_api.login_user(invalid_login_data)

        assert response.status_code in [401, 500], "Пропуск авторизации на неверном пароле"
        response_data = response.json()

        # Проверки
        assert response.status_code == 401, "Пропуск авторизации на неправильном email"
        assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"


    def test_invalid_email_auth(self, api_manager, test_user):
        # Отправка запроса на авторизацию
        invalid_login_data = {"email": "test_@mail.ru", "password": test_user["password"]}
        response = api_manager.auth_api.login_user(invalid_login_data)
        response_data = response.json()
        # Проверки
        assert response.status_code == 401, "Пропуск авторизации на неправильном email"
        assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"

    def test_empty_body_auth(self, api_manager, test_user):

        # Отправка запроса на авторизацию
        invalid_login_data = {}
        response = api_manager.auth_api.login_user(invalid_login_data)
        response_data = response.json()

        # Проверки
        assert response.status_code == 401, "Пропуск авторизации на пустом запросе в теле"
        assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"

