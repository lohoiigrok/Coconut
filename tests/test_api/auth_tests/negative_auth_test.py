import pytest
import allure
from models.models import ErrorResponseModel

@allure.epic("Auth API")
@allure.feature("Negative scenarios")
class TestNegativeAuthAPI:
    @allure.story("Login with invalid pass")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_invalid_pass_auth(self, api_manager, registered_user):
        invalid_login_data = {"email": registered_user["email"], "password": registered_user["password"] + "Dsdjods32d"}

        with allure.step("Отправляем запрос на логин пользователя c неверным паролем"):
            response = api_manager.auth_api.login_user(invalid_login_data, expected_status = 401)
            response_data = response.json()

        with allure.step("Проверяем поля ошибки"):
            ErrorResponseModel(**response_data)
            assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"

    @allure.story("Login with invalid email")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_invalid_email_auth(self, api_manager, registered_user):
        invalid_login_data = {"email": "test_@mail.ru", "password": registered_user["password"]}

        with allure.step("Отправляем запрос на логин пользователя c неправильным email"):
            response = api_manager.auth_api.login_user(invalid_login_data, expected_status = 401)
            response_data = response.json()

        with allure.step("Проверяем поля полученной ошибки"):
            ErrorResponseModel(**response_data)
            assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"

    @allure.story("Register user with with empty fields (empty pass, empty email, empty body)")
    @pytest.mark.negative
    @pytest.mark.auth
    @pytest.mark.parametrize("bad_data,expected_status",
    [({"email": "test@test.com"}, 401),
     ({"password": "Valid1pass"}, 401),
     ({}, 401)
     ], ids= ["missing_password", "missing_email", "empty_body"])
    def test_register_missing_required_fields(self, api_manager, bad_data, expected_status):
        with allure.step("Отправляем запрос на логин пользователя c различными пустыми полями"):
            response = api_manager.auth_api.login_user(bad_data, expected_status)
            response_data = response.json()

        with allure.step("Проверяем поля полученной ошибки"):
            ErrorResponseModel(**response_data)
            assert "accessToken" not in response_data, "Токен доступа выдало при неправильных данных"
