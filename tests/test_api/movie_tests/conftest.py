import pytest
from utils.data_generator import DataGenerator
from types.common_types import MovieListData, MovieData


@pytest.fixture
def movie_data() -> MovieData:
    """ Валидные данные для создания фильма """
    return DataGenerator.movie_data()


@pytest.fixture
def min_boundary_movie_data() -> MovieData:
    """ Минимальные граничные данные для создания фильма """
    return DataGenerator.min_boundary_movie_data()


@pytest.fixture
def max_boundary_movie_data() -> MovieData:
    """ Максимальные граничные данные для создания фильма """
    return DataGenerator.max_boundary_movie_data()


@pytest.fixture
def invalid_movie_data() -> MovieListData:
    """ Невалидные данные для создания фильма """
    return DataGenerator.invalid_movie_data()


@pytest.fixture
def movie_query_params() -> MovieData:
    """ Параметры выборки для GET-запроса """
    return DataGenerator.movie_query_params()


@pytest.fixture(scope="function")
def created_movie(authorized_admin, movie_data) -> MovieData:
    response = authorized_admin.movies_api.create_movie(movie_data)
    data = response.json()
    return data


@pytest.fixture(scope="function")
def created_movie_with_delete(authorized_admin, created_movie) -> MovieData:
    yield created_movie
    authorized_admin.movies_api.clean_up_movie(created_movie["id"])






