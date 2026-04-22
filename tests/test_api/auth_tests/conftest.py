import pytest
from utils.data_generator import DataGenerator
from types.common_types import UserData


@pytest.fixture(scope="function")
def auth_user_data() -> UserData:
    """
    Данные нового пользователя в формате /auth/register.
    Отдельная фикстура — не конфликтует с глобальной test_user.
    """
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"],
    }

@pytest.fixture(scope="function")
def admin_user_data(auth_user_data) -> dict:
    data = auth_user_data.copy()
    data.update({
        "verified": True,
        "banned": False,
    })
    return data

@pytest.fixture(scope="function")
def registered_user(api_manager, auth_user_data) -> UserData:
    """
    Регистрирует пользователя через /auth/register.
    После теста удаляет его через admin user_api.
    """
    response = api_manager.user_api.create_user(auth_user_data)
    response_data = response.json()

    registered = auth_user_data.copy()
    registered["id"] = response_data["id"]

    yield registered

    try:
        api_manager.user_api.clean_up_user(registered["id"])
    except ValueError:
        # Пользователь уже удалён / нет такого endpoint — не падаем
        pass
