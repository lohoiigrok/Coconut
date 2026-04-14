class TestPositiveMoviesAPI:
    def test_get_movies_public(self, api_manager):
        """
        Получаем тестовый список фильмов на публичной роли
        """
        params = {"pageSize": 10, "page": 1}
        response = api_manager.movies_api.get_movies_list(params, expected_status = 200)
        data = response.json()

        assert 'movies' in data
        assert data["pageSize"] == params["pageSize"]
        assert data["page"] == params["page"]
        assert isinstance(data['movies'], list)


    def test_post_movie_auth(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма на админской роли
        """
        response = authorized_admin.movies_api.create_movie(movie_data, expected_status = 201)
        response_data = response.json()

        assert "id" in response_data
        assert isinstance(response_data["id"], int)
        assert movie_data["price"] == response_data["price"]
        assert movie_data["genreId"] == response_data["genreId"]
        assert movie_data["name"] == response_data["name"]
        assert movie_data["description"] == response_data["description"]
        assert movie_data["location"] == response_data["location"]
        assert movie_data["published"] == response_data["published"]

        authorized_admin.movies_api.clean_up_movie(response_data["id"])

    def test_patch_movie_auth(self,created_movie, authorized_admin, movie_data):
        """
        Проверяем возможность изменения в созданном фильме на админской роли.
        """
        movie_id = created_movie["id"]
        updated_data = movie_data.copy()
        updated_data['price'] = 999
        authorized_admin.movies_api.update_movie(movie_id, updated_data, expected_status = 200)
        response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status = 200)
        data = response.json()

        assert "id" in data, "В ответе на создание фильма отсутствует id"
        assert data["id"] == movie_id
        assert data["price"] == 999

    def test_delete_movie_auth(self, authorized_admin, movie_data):
        """
        Тестируем удаления фильма на админской роли.
        """
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        data = create_response.json()

        assert "id" in data
        movie_id = data["id"]

        delete_response = authorized_admin.movies_api.delete_movie(movie_id, expected_status = 200)
        delete_data = delete_response.json()

        assert "id" in delete_data
        assert delete_data["id"] == movie_id

        response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status = 404)
        response_data = response.json()

        assert "message" in response_data
        assert "error" in response_data

    def test_get_filter_location(self, api_manager):
        """
        Тестируем фильтр по локации на подборке фильма, публичная роль.
        """
        params = {"locations": "MSK"}
        response = api_manager.movies_api.get_movies_list(params, expected_status = 200)
        movie_data = response.json()
        movies = movie_data['movies']
        
        assert 'movies' in movie_data
        assert isinstance(movies, list)
        for movie in movies:
            assert movie["location"] == "MSK"

    def test_pagination(self, authorized_admin):
        """
        Проверяем пагинацию на админской роли.
        """
        resp1 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 1}, expected_status = 200)
        resp2 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 2}, expected_status = 200)
        movies1 = resp1.json()['movies']
        ids1 = [movie["id"] for movie in movies1]
        movies2 = resp2.json()['movies']
        ids2 = [movie["id"] for movie in movies2]

        assert len(movies1) == 5
        assert len(movies2) <= 5
        assert set(ids1).isdisjoint(set(ids2))

    def test_complex_filter(self, authorized_admin, movie_query_params):
        """
        Тестируем работу различных параметров в запросе на валидных данных query params.
        """
        test_params = movie_query_params
        response = authorized_admin.movies_api.get_movies_list(test_params)
        data = response.json()

        assert "movies" in data
        assert "page" in data
        assert "pageSize" in data
        assert "pageCount" in data
        assert isinstance(data["movies"], list)
        assert data["pageSize"] == test_params["pageSize"]
        for movie in data["movies"]:
            assert movie["location"] == movie_query_params["locations"]
            assert movie["genreId"] == movie_query_params["genreId"]

    def test_post_left_boundary_values(self, authorized_admin, movie_data):
        """
        Проверяем левые (минимальные) граничные значения при создании фильма.
        """
        boundary_data = movie_data.copy()
        boundary_data["name"] = "Y"
        boundary_data["price"] = 1  # min
        boundary_data["genreId"] = 1  # min
        boundary_data["description"] = ""
        boundary_data["location"] = "MSK"
        boundary_data["published"] = True

        response = authorized_admin.movies_api.create_movie(boundary_data, expected_status = 201)
        data = response.json()

        assert "id" in data
        assert data["price"] == boundary_data["price"]
        assert data["genreId"] == boundary_data["genreId"]
        assert data["name"] == boundary_data["name"]
        assert data["description"] == boundary_data["description"]
        assert data["location"] == boundary_data["location"]
        assert data["published"] == boundary_data["published"]

        authorized_admin.movies_api.clean_up_movie(data["id"])

    def test_post_right_boundary_values(self, authorized_admin, movie_data):
        """
        Проверяем правые (максимальные) граничные значения при создании фильма.
        """
        boundary_data = movie_data.copy()
        boundary_data["price"] = 999999999  # max
        boundary_data["genreId"] = 10 # max
        boundary_data["location"] = "SPB"
        boundary_data["published"] = False

        response = authorized_admin.movies_api.create_movie(boundary_data, expected_status=201)
        data = response.json()

        assert "id" in data
        assert data["price"] == boundary_data["price"]
        assert data["genreId"] == boundary_data["genreId"]
        assert data["name"] == boundary_data["name"]
        assert data["location"] == boundary_data["location"]
        assert data["published"] == boundary_data["published"]

        authorized_admin.movies_api.clean_up_movie(data["id"])