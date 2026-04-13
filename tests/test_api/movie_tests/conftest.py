import pytest
import requests
from testsam.constants import SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from testsam.utils.data_generator import DataGenerator
from testsam.clients.api_manager import ApiManager
from typing import Any, Generator

MovieData = dict[str, Any]
MovieListData = list[dict[str, Any]]

# Фикстуры по данным фильма
@pytest.fixture
def movie_data() -> MovieData:
    """ Валидный фильм"""
    return DataGenerator.movie_data()

@pytest.fixture
def invalid_movie_data() -> MovieListData:
    """ Валидный фильм"""
    return DataGenerator.invalid_movie_data()

@pytest.fixture
def movie_query_params() -> MovieData:
    """ Валидный фильм"""
    return DataGenerator.movie_query_params()

@pytest.fixture
def genre_data() -> MovieData:
    return DataGenerator.genre_data()

@pytest.fixture
def created_movie(authorized_admin, movie_data) -> Generator[MovieData, None, None]:
    response = authorized_admin.movies_api.create_movie(movie_data, expected_status=201)

    data = response.json()
    yield data
    movie_id = data['id']
    authorized_admin.movies_api.clean_up_movie(movie_id)


# Фикстуры для пользователей

@pytest.fixture(scope="session")
def session() -> Generator[requests.Session, None, None]:
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session: requests.Session) -> ApiManager:
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture(scope="session")
def authorized_admin(api_manager: ApiManager) -> Generator[ApiManager, None, None]:
    """
    Фикстура для авторизации и возращает ApiManager с токеном админа.
    """
    admin_creds = [SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD]
    # Авторизуемся под админом
    api_manager.auth_api.authenticate(admin_creds)

    # Используем yield
    yield api_manager

    # Чистим токен (специальным методом)
    api_manager.clear_auth()



