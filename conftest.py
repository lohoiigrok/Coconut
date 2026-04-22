import pytest
from requests import Session
from clients.api_manager import ApiManager
from roles import User
from config import SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from roles import Roles
from utils.data_generator import DataGenerator


@pytest.fixture
def user_session():
    session_pool = []

    def _create_user_session():
        http_session = Session()
        session_pool.append(http_session)
        return ApiManager(http_session)

    yield _create_user_session

    for session in session_pool:
        session.close()

@pytest.fixture(scope="session")
def api_manager() -> ApiManager:
    """
    Фикстура для тестов без необходимости авторизации
    """
    http_session = Session()
    manager = ApiManager(http_session)
    manager.clear_auth()

    yield manager

    http_session.close()


@pytest.fixture(scope="function")
def authorized_admin() -> ApiManager:
    """
    Фикстура для авторизации и возращает ApiManager с токеном админа.
    """
    admin_creds = [SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD]
    http_session = Session()
    manager = ApiManager(http_session)
    manager.auth_api.authenticate(admin_creds)

    yield manager

    manager.clear_auth()
    http_session.close()

@pytest.fixture
def super_admin(user_session) -> User:
    """Объект SUPER_ADMIN с авторизованной сессией."""
    admin_manager = user_session()
    super_admin = User(
        SUPER_ADMIN_EMAIL,
        SUPER_ADMIN_PASSWORD,
        [Roles.SUPER_ADMIN.value],
        admin_manager
    )
    super_admin.api_manager.auth_api.authenticate(super_admin.creds)
    yield super_admin

@pytest.fixture(scope="function")
def test_user() -> dict:
    return DataGenerator.user_data()

@pytest.fixture(scope="function")
def creation_user_data(test_user) -> dict:
    updated_data = test_user.copy()
    updated_data["fullName"] = DataGenerator.generate_random_name()
    return updated_data

@pytest.fixture
def authorized_user(authorized_admin: ApiManager, creation_user_data: dict) -> ApiManager:
    """
    Обычный пользователь: создаётся админом и затем авторизуется.
    Возвращаем именно ApiManager с токеном USER.
    """
    authorized_admin.user_api.create_user(creation_user_data)

    http_session = Session()
    manager = ApiManager(http_session)

    manager.auth_api.authenticate((creation_user_data["email"], creation_user_data["password"]))

    yield manager

    manager.clear_auth()
    http_session.close()
