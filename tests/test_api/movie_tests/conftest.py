import pytest
import requests
from testsam.constants import BASE_URL, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from testsam.customer_requester.custom_requester import CustomRequester
from testsam.utils.data_generator import DataGenerator
from testsam.clients.api_manager import ApiManager

# Фикстуры по данным фильма
@pytest.fixture
def movie_data():
    """ Валидный фильм"""
    return DataGenerator.movie_data()

@pytest.fixture
def invalid_movie_data():
    """ Валидный фильм"""
    return DataGenerator.movie_data()

@pytest.fixture
def movie_query_params():
    """ Валидный фильм"""
    return DataGenerator.movie_query_params()

@pytest.fixture
def genre_data():
    return DataGenerator.genre_data()
# Фикстуры для пользователей

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture(scope="function")
def authorized_admin(api_manager):
    """
    Фикстура для авторизации и возращает ApiManager с токеном админа.
    """
    admin_creds = [SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD]
    # Авторизуемся под админом
    response = api_manager.auth_api.authenticate(admin_creds)

    # Используем yield
    yield api_manager

    # Чистим токен
    api_manager.session.headers.update({"Authorization": None})


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

