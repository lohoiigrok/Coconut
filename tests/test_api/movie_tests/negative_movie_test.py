import pytest
import allure
import pytest_check as check

from testsam.utils.data_generator import DataGenerator
from testsam.models.models import ErrorResponseModel, MovieResponseModel

@allure.epic("Movies API")
@allure.feature("Negative scenarios")
class TestNegativeMoviesAPI:

    @allure.story("Create movie forbidden for public")
    @pytest.mark.negative
    @pytest.mark.public
    def test_post_movie_by_public_role_forbidden(self, api_manager, movie_data):
        """
        Тестируем, что публичный пользователь не может создать фильм.
        """
        with allure.step("Отправляем POST /movies от публичной роли"):
            response = api_manager.movies_api.create_movie(movie_data, expected_status=401)
            response_data = response.json()
            noncreated_movie = ErrorResponseModel(**response_data)

        with allure.step("Проверяем поля ошибки"):
            check.is_in("Unauthorized", str(noncreated_movie.message))

    @allure.story("Get nonexistent movie as PUBLIC")
    @pytest.mark.negative
    @pytest.mark.public
    def test_get_nonexistent_movie_id_by_public_role(self, api_manager):
        """
        Тестируем, что нельзя получить несуществующий фильм.
        """
        movie_id = -10

        with allure.step(f"Отправляем GET /movies/{movie_id}"):
            response = api_manager.movies_api.get_single_movie(movie_id, expected_status=404)
            response_data = response.json()
            nonexistent_movie = ErrorResponseModel(**response_data)

        with allure.step("Проверяем поля ошибки"):
            check.is_in("Фильм не найден", str(nonexistent_movie.message))
            check.is_in("Not Found", str(nonexistent_movie.error))

    @allure.story("Delete movie forbidden for PUBLIC")
    @pytest.mark.negative
    @pytest.mark.public
    def test_delete_movie_with_public_role_forbidden(self, created_movie, api_manager):
        """
        Тестируем, что публичный пользователь не может удалить фильм.
        """
        MovieResponseModel(**created_movie)
        movie_id = created_movie['id']

        with allure.step("Проверяем, что фильм существует до попытки удалить его"):
            get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
            get_data = get_response.json()

        with allure.step("Проверяем id фильма и поля ошибки"):
            get_movie = MovieResponseModel(**get_data)
            assert get_movie.id == movie_id
            check.is_in(get_movie.price, created_movie["price"])
            check.is_in(get_movie.genreId, created_movie["genreId"])
            check.is_in(get_movie.name, created_movie["name"])
            check.is_in(get_movie.description, created_movie["description"])
            check.is_in(get_movie.location, created_movie["location"])
            check.is_in(get_movie.published, created_movie["published"])

        with allure.step("Удаляем фильм"):
            delete_response = api_manager.movies_api.delete_movie(movie_id, expected_status=401)
            delete_data = delete_response.json()

        with allure.step("Проверяем поля ошибки"):
            delete_movie = ErrorResponseModel(**delete_data)
            check.is_in("Unauthorized", delete_movie.message)

        with allure.step("Достаем созданный фильм из бд для проверок."):
            get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
            get_data = get_response.json()

        get_movie = MovieResponseModel(**get_data)
        assert get_movie.id == movie_id

    @allure.story("Create duplicate movie as SUPER_ADMIN")
    @pytest.mark.negative
    @pytest.mark.superadmin
    def test_post_movie_duplicate_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем возможность создать дубликат фильма на админской роли.
        """
        with allure.step("Создаем фильм для теста и проверяем его поля."):
            create_response = authorized_admin.movies_api.create_movie(movie_data)
            create_data = create_response.json()
            create_movie = MovieResponseModel(**create_data)
            movie_id = create_movie.id

        with allure.step("Достаем созданный фильм из бд для проверок."):
            get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
            get_data = get_response.json()

        with allure.step("Проверяем id фильма и поля ошибки"):
            get_movie = MovieResponseModel(**get_data)
            assert get_movie.id == movie_id
            check.is_in(get_movie.price, create_data["price"])
            check.is_in(get_movie.genreId, create_data["genreId"])
            check.is_in(get_movie.name, create_data["name"])
            check.is_in(get_movie.description, create_data["description"])
            check.is_in(get_movie.location, create_data["location"])
            check.is_in(get_movie.published, create_data["published"])

        with allure.step("Пробуем создать дубликат фильма для теста"):
            duplicate_response = authorized_admin.movies_api.create_movie(movie_data, expected_status=409)
            duplicate_data = duplicate_response.json()

        with allure.step("Проверяем поля ошибки"):
            duplicate_movie = ErrorResponseModel(**duplicate_data)
            check.is_in("Conflict", duplicate_movie.error)

        with allure.step("Чистим фильм из БД"):
          authorized_admin.movies_api.clean_up_movie(movie_id)

    @allure.story("Create movie with invalid body as SUPER_ADMIN")
    @pytest.mark.negative
    @pytest.mark.superadmin
    @pytest.mark.parametrize("bad_data", DataGenerator.invalid_movie_data(), ids=DataGenerator.invalid_movie_data_ids())
    def test_post_invalid_data(self, authorized_admin, bad_data):
        """
        Тестируем создание фильма из невалидных данных. (несколько разных параметров)
        """
        with allure.step("Пробуем создать фильм с невалидными данными"):
            response = authorized_admin.movies_api.create_movie(bad_data, expected_status = 400)
            response_data = response.json()

        with allure.step("Проверяем поля ошибки"):
            noncreated_movie = ErrorResponseModel(**response_data)
            check.is_in("Bad Request", str(noncreated_movie.error))

    @allure.story("Create movie with invalid genre as SUPER_ADMIN")
    @pytest.mark.negative
    @pytest.mark.superadmin
    def test_post_movie_with_invalid_genre_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма с невалидным жанром.
        """
        bad_data = movie_data.copy()
        bad_data["genreId"] = 999999

        with allure.step("Пробуем создать фильм с неправильными жанром"):
            response = authorized_admin.movies_api.create_movie(bad_data, expected_status=400)
            response_data = response.json()

        with allure.step("Проверяем поля ошибки"):
            noncreated_movie = ErrorResponseModel(**response_data)
            check.is_in("Bad Request", str(noncreated_movie.error))

    @allure.story("Create movie with empty body as SUPER_ADMIN")
    @pytest.mark.negative
    @pytest.mark.superadmin
    def test_post_movie_empty_data_by_superadmin(self, authorized_admin):
        """
        Тестируем создание фильма из пустых данных на админской роли.
        """
        with allure.step("Пробуем создать фильм с пустыми данными"):
            response = authorized_admin.movies_api.create_movie({}, expected_status=400)
            response_data = response.json()

        with allure.step("Проверяем поля ошибки"):
            noncreated_movie = ErrorResponseModel(**response_data)
            check.is_in("Bad Request", str(noncreated_movie.error))