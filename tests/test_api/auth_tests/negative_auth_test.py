from testsam.clients.api_manager import ApiManager

class TestNegativeAuthAPI:

    def test_invalid_pass_auth(self, api_manager, test_user):
        invalid_login_data = {"email": test_user["email"], "password": "Dsdjods32d"}
        response = api_manager.auth_api.login_user(invalid_login_data, expected_status=401)
        response_data = response.json()
        # Проверки
        assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"


    def test_invalid_email_auth(self, api_manager, test_user):
        invalid_login_data = {"email": "test_@mail.ru", "password": test_user["password"]}
        response = api_manager.auth_api.login_user(invalid_login_data, expected_status=401)
        response_data = response.json()
        # Проверки
        assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"

    def test_empty_body_auth(self, api_manager, test_user):
        invalid_login_data = {}
        response = api_manager.auth_api.login_user(invalid_login_data, expected_status=401)
        response_data = response.json()
        # Проверки
        assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"

