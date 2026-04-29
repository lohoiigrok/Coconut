import pytest
from models.models import MovieListResponseModel, MovieResponseModel, ErrorResponseModel
import pytest_check as check

class TestPositiveMoviesAPI:
    def test_get_movies_list_by_public_role(self, api_manager):
        """
        Получаем тестовый список фильмов на публичной роли
        """
        params = {"pageSize": 10, "page": 1}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        data = response.json()
        movie_list = MovieListResponseModel(**data)

        assert movie_list.pageSize == params["pageSize"]
        assert movie_list.page == params["page"]

    def test_post_movie_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма на админской роли
        """
        response = authorized_admin.movies_api.create_movie(movie_data, expected_status=201)
        response_data = response.json()

        movie = MovieResponseModel(**response_data)
        movie_id = response_data["id"]

        check.equal(movie.price, movie_data["price"])
        check.equal(movie.genreId, movie_data["genreId"])
        check.equal(movie.name, movie_data["name"])
        check.equal(movie.description, movie_data["description"])
        check.equal(movie.location, movie_data["location"])
        check.equal(movie.published, movie_data["published"])

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        get_movie = MovieResponseModel(**get_data)

        check.equal(get_movie.price, movie_data["price"])
        check.equal(get_movie.genreId, movie_data["genreId"])
        check.equal(get_movie.name, movie_data["name"])
        check.equal(get_movie.description, movie_data["description"])
        check.equal(get_movie.location, movie_data["location"])
        check.equal(get_movie.published, movie_data["published"])

        authorized_admin.movies_api.clean_up_movie(response_data["id"])


    def test_patch_movie_by_superadmin(self, created_movie_with_delete, authorized_admin, movie_data):
        """
        Проверяем возможность изменения данных в созданном фильме на админской роли.
        """
        movie_id = created_movie_with_delete["id"]
        updated_data = movie_data.copy()
        updated_data['price'] = 999
        update_response = authorized_admin.movies_api.update_movie(movie_id, updated_data, expected_status=200)
        update_data = update_response.json()

        update_movie = MovieResponseModel(**update_data)

        assert update_movie.id == movie_id
        assert update_movie.name == updated_data["name"]
        assert update_movie.price == 999

        get_response_for_update_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data_for_update_movie = get_response_for_update_movie.json()

        get_update_movie = MovieResponseModel(**get_data_for_update_movie)

        assert get_update_movie.id == movie_id
        assert get_update_movie.price == 999

    def test_delete_movie_by_superadmin(self, created_movie, authorized_admin):
        """
        Тестируем удаление фильма на админской роли.
        """
        movie_id = created_movie["id"]
        delete_response = authorized_admin.movies_api.delete_movie(movie_id, expected_status=200)
        delete_data = delete_response.json()
        delete_movie = MovieResponseModel(**delete_data)

        assert delete_movie.id == movie_id

        get_response_delete_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=404)
        get_data_delete_movie = get_response_delete_movie.json()
        get_delete_movie = ErrorResponseModel(**get_data_delete_movie)

        assert "Фильм не найден" in get_delete_movie.message
        assert "Not Found" in get_delete_movie.error

    @pytest.mark.parametrize("location", ["MSK", "SPB"])
    def test_get_filter_movies_by_location(self, api_manager, location):
        """
        Тестируем фильтр по локации на подборке фильма, публичная роль.
        """
        params = {"locations": location}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        movie_data = response.json()

        movie_list = MovieListResponseModel(**movie_data)

        for movie in movie_list.movies:
            assert movie.location == location

    def test_pagination_list_for_movies(self, authorized_admin):
        """
        Проверяем пагинацию на админской роли.
        """
        resp1 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 1}, expected_status=200)
        resp2 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 2}, expected_status=200)
        movie_page1 = resp1.json()
        movie_list_page1 = MovieListResponseModel(**movie_page1)
        ids1 = [movie.id for movie in movie_list_page1.movies]
        movie_page2 = resp2.json()
        movie_list_page2 = MovieListResponseModel(**movie_page2)
        ids2 = [movie.id for movie in movie_list_page2.movies]

        assert len(movie_list_page1.movies) == 5
        assert len(movie_list_page2.movies) <= 5
        assert set(ids1).isdisjoint(set(ids2))

    def test_complex_filter_for_movies_list(self, authorized_admin, movie_query_params):
        """
        Тестируем работу различных параметров в запросе на валидных данных query params.
        """
        test_params = movie_query_params
        response = authorized_admin.movies_api.get_movies_list(test_params)
        data = response.json()
        movie_list = MovieListResponseModel(**data)

        assert movie_list.pageSize == test_params["pageSize"]
        for movie in movie_list.movies:
            assert movie.location == movie_query_params["locations"]
            assert movie.genreId == movie_query_params["genreId"]

    def test_post_movie_with_left_boundary_values(self, authorized_admin, min_boundary_movie_data):
        """
        Проверяем левые (минимальные) граничные значения при создании фильма.
        """
        response = authorized_admin.movies_api.create_movie(min_boundary_movie_data, expected_status=201)
        data = response.json()
        create_movie = MovieResponseModel(**data)
        movie_id = create_movie.id

        assert create_movie.price == min_boundary_movie_data["price"]
        assert create_movie.genreId == min_boundary_movie_data["genreId"]
        assert create_movie.name == min_boundary_movie_data["name"]
        assert create_movie.description == min_boundary_movie_data["description"]
        assert create_movie.location == min_boundary_movie_data["location"]
        assert create_movie.published == min_boundary_movie_data["published"]

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()
        get_movie = MovieResponseModel(**get_data)

        assert get_movie.id == movie_id
        assert get_movie.price == min_boundary_movie_data["price"]
        assert get_movie.genreId == min_boundary_movie_data["genreId"]
        assert get_movie.name == min_boundary_movie_data["name"]
        assert get_movie.description == min_boundary_movie_data["description"]
        assert get_movie.location == min_boundary_movie_data["location"]
        assert get_movie.published == min_boundary_movie_data["published"]

        authorized_admin.movies_api.clean_up_movie(data["id"])

    def test_post_movie_with_right_boundary_values(self, authorized_admin, max_boundary_movie_data):
        """
        Проверяем правые (максимальные) граничные значения при создании фильма.
        """
        response = authorized_admin.movies_api.create_movie(max_boundary_movie_data, expected_status=201)
        data = response.json()
        create_movie = MovieResponseModel(**data)
        movie_id = create_movie.id

        assert create_movie.name == max_boundary_movie_data["name"]
        assert create_movie.price == max_boundary_movie_data["price"]
        assert create_movie.genreId == max_boundary_movie_data["genreId"]
        assert create_movie.location == max_boundary_movie_data["location"]
        assert create_movie.published == max_boundary_movie_data["published"]

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()
        get_movie = MovieResponseModel(**get_data)

        assert get_movie.id == movie_id
        assert get_movie.price == max_boundary_movie_data["price"]
        assert get_movie.genreId == max_boundary_movie_data["genreId"]
        assert get_movie.name == max_boundary_movie_data["name"]
        assert get_movie.description == max_boundary_movie_data["description"]
        assert get_movie.location == max_boundary_movie_data["location"]
        assert get_movie.published == max_boundary_movie_data["published"]

        authorized_admin.movies_api.clean_up_movie(data["id"])
