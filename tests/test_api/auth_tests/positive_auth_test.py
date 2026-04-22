
class TestPositiveAuthAPI:
    def test_register_user(self, api_manager, auth_user_data):
        """"
        Тест на регистрацию нового пользователя.
        """
        response = api_manager.user_api.create_user(auth_user_data)
        response_data = response.json()

        assert response_data["email"] == auth_user_data["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсустсвуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

        api_manager.user_api.clean_up_user(response_data["id"])

    def test_register_and_login_user(self, api_manager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя
        """
        login_data = {"email": registered_user["email"], "password": registered_user["password"]}
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data, "Токен доступа отсустсвует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"
        assert isinstance(response_data["accessToken"], str)
        assert len(response_data["accessToken"]) > 0

    def test_login_returns_valid_token_structure(self, api_manager, registered_user):
        """
        Проверяем структуру успешного ответа логина.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        response = api_manager.auth_api.login_user(login_data)
        data = response.json()

        assert "accessToken" in data, "Нет accessToken в ответе"
        assert isinstance(data["accessToken"], str), "accessToken должен быть строкой"
        assert data["accessToken"], "accessToken пустой"

        assert "refreshToken" in data
        assert isinstance(data["refreshToken"], str)

        assert "expiresIn" in data
        assert isinstance(data["expiresIn"], int)

        assert "user" in data, "Нет поля user в ответе"
        assert data["user"]["email"] == registered_user["email"], "Email в user не совпадает"


