import pytest
import pytest_check as check
from utils.data_generator import DataGenerator
from models.models import ErrorResponseModel, MovieResponseModel

class TestNegativeMoviesAPI:
    def test_post_movie_by_public_role_forbidden(self, api_manager, movie_data):
        """
        Тестируем, что публичный пользователь не может создать фильм.
        """
        response = api_manager.movies_api.create_movie(movie_data, expected_status=401)
        response_data = response.json()
        noncreated_movie = ErrorResponseModel(**response_data)

        check.is_in("Unauthorized", str(noncreated_movie.message))

    def test_get_nonexistent_movie_id_by_public_role(self, api_manager):
        """
        Тестируем, что нельзя получить несуществующий фильм.
        """
        movie_id = -10
        response = api_manager.movies_api.get_single_movie(movie_id, expected_status=404)
        response_data = response.json()
        nonexistent_movie = ErrorResponseModel(**response_data)

        check.is_in("Фильм не найден", str(nonexistent_movie.message))
        check.is_in("Not Found", str(nonexistent_movie.error))

    def test_delete_movie_with_public_role_forbidden(self, created_movie, api_manager):
        """
        Тестируем, что публичный пользователь не может удалить фильм.
        """
        MovieResponseModel(**created_movie)
        movie_id = created_movie['id']

        get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()
        get_movie = MovieResponseModel(**get_data)

        assert get_movie.id == movie_id
        assert get_movie.price == created_movie["price"]
        assert get_movie.genreId == created_movie["genreId"]
        assert get_movie.name == created_movie["name"]
        assert get_movie.description == created_movie["description"]
        assert get_movie.location == created_movie["location"]
        assert get_movie.published == created_movie["published"]

        delete_response = api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        delete_data = delete_response.json()
        delete_movie = ErrorResponseModel(**delete_data)

        assert "Unauthorized" in delete_movie.message

        get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()
        get_movie = MovieResponseModel(**get_data)

        assert get_movie.id == movie_id

    def test_post_movie_duplicate_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем возможность создать дубликат фильма на админской роли.
        """
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        create_data = create_response.json()
        create_movie = MovieResponseModel(**create_data)

        movie_id = create_movie.id

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()
        get_movie = MovieResponseModel(**get_data)

        assert get_movie.id == movie_id
        assert get_movie.price == create_data["price"]
        assert get_movie.genreId == create_data["genreId"]
        assert get_movie.name == create_data["name"]
        assert get_movie.description == create_data["description"]
        assert get_movie.location == create_data["location"]
        assert get_movie.published == create_data["published"]

        duplicate_response = authorized_admin.movies_api.create_movie(movie_data, expected_status=409)
        duplicate_data = duplicate_response.json()
        duplicate_movie = ErrorResponseModel(**duplicate_data)

        assert "Conflict" in duplicate_movie.error

        authorized_admin.movies_api.clean_up_movie(movie_id)

    @pytest.mark.parametrize("bad_data", DataGenerator.invalid_movie_data(), ids=DataGenerator.invalid_movie_data_ids())
    def test_post_invalid_data(self, authorized_admin, bad_data):
        """
        Тестируем создание фильма из невалидных данных. (несколько разных параметров)
        """
        response = authorized_admin.movies_api.create_movie(bad_data, expected_status = 400)
        response_data = response.json()
        noncreated_movie = ErrorResponseModel(**response_data)

        assert "Bad Request" in noncreated_movie.error

    def test_post_movie_with_invalid_genre_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма с невалидным жанром.
        """
        bad_data = movie_data.copy()
        bad_data["genreId"] = 999999
        response = authorized_admin.movies_api.create_movie(bad_data, expected_status=400)
        response_data = response.json()
        noncreated_movie = ErrorResponseModel(**response_data)

        assert "Bad Request" in noncreated_movie.error

    def test_post_movie_empty_data_by_superadmin(self, authorized_admin):
        """
        Тестируем создание фильма из пустых данных на админской роли.
        """
        response = authorized_admin.movies_api.create_movie({}, expected_status=400)
        response_data = response.json()
        noncreated_movie = ErrorResponseModel(**response_data)

        assert "Bad Request" in noncreated_movie.error