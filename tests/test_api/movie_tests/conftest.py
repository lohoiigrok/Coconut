import pytest
from requests import Session
from constants import SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from types.common_types import MovieListData, MovieData

# Фикстуры по данным фильма
@pytest.fixture
def movie_data() -> MovieData:
    """ Валидные данные для создания фильма """
    return DataGenerator.movie_data()

@pytest.fixture
def invalid_movie_data() -> MovieListData:
    """ Невалидные данные для создания фильма """
    return DataGenerator.invalid_movie_data()

@pytest.fixture
def movie_query_params() -> MovieData:
    """ Параметры выборки для GET-запроса """
    return DataGenerator.movie_query_params()

@pytest.fixture(scope="function")
def created_movie(authorized_admin, movie_data) -> Generator[MovieData, None, None]:
    response = authorized_admin.movies_api.create_movie(movie_data)

    data = response.json()
    yield data
    authorized_admin.movies_api.clean_up_movie(data['id'])


# Фикстуры для пользователей

@pytest.fixture(scope="session")
def api_manager() -> ApiManager:
    """
    Фикстура для тестов без необходимости авторизации
    """
    http_session = Session()
    manager = ApiManager(http_session)
    manager.clear_auth()

    yield ApiManager(http_session)
    http_session.close()

@pytest.fixture(scope="function")
def authorized_admin() -> ApiManager:
    """
    Фикстура для авторизации и возращает ApiManager с токеном админа.
    """
    admin_creds = [SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD]
    # Авторизуемся под админом
    http_session = Session()
    manager = ApiManager(http_session)
    manager.auth_api.authenticate(admin_creds)

    # Используем yield
    yield manager

    # Чистим токен (специальным методом)
    manager.clear_auth()



