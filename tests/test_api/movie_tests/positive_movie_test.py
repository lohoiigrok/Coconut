class TestPositiveMoviesAPI:
    def test_get_movies_list_by_public_role(self, api_manager):
        """
        Получаем тестовый список фильмов на публичной роли
        """
        params = {"pageSize": 10, "page": 1}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        data = response.json()

        assert 'movies' in data
        assert data["pageSize"] == params["pageSize"]
        assert data["page"] == params["page"]
        assert isinstance(data['movies'], list)


    def test_post_movie_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма на админской роли
        """
        response = authorized_admin.movies_api.create_movie(movie_data, expected_status=201)
        response_data = response.json()
        
        assert "id" in response_data
        movie_id = response_data["id"]
        
        assert isinstance(movie_id, int)
        assert response_data["price"] == movie_data["price"]
        assert response_data["genreId"] == movie_data["genreId"]
        assert response_data["name"] == movie_data["name"]
        assert response_data["description"] == movie_data["description"] 
        assert response_data["location"] == movie_data["location"]
        assert response_data["published"] == movie_data["published"]
        
        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data, "В ответе отсутствует id фильма"
        assert get_data["id"] == movie_id
        assert get_data["price"] == movie_data["price"]
        assert get_data["genreId"] == movie_data["genreId"]
        assert get_data["name"] == movie_data["name"]
        assert get_data["description"] == movie_data["description"] 
        assert get_data["location"] == movie_data["location"]
        assert get_data["published"] == movie_data["published"]
        
        authorized_admin.movies_api.clean_up_movie(response_data["id"])

    def test_patch_movie_by_superadmin(self,created_movie, authorized_admin, movie_data):
        """
        Проверяем возможность изменения данных в созданном фильме на админской роли.
        """
        movie_id = created_movie["id"]
        get_response_for_create_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data_for_create_movie = get_response_for_create_movie.json()

        assert "id" in get_data_for_create_movie, "В ответе отсутствует id фильма"
        assert get_data_for_create_movie["id"] == movie_id
        assert get_data_for_create_movie["price"] == movie_data["price"]
        assert get_data_for_create_movie["genreId"] == movie_data["genreId"]
        assert get_data_for_create_movie["name"] == movie_data["name"]
        assert get_data_for_create_movie["description"] == movie_data["description"] 
        assert get_data_for_create_movie["location"] == movie_data["location"]
        assert get_data_for_create_movie["published"] == movie_data["published"]
        
        updated_data = movie_data.copy()
        updated_data['price'] = 999
        update_response = authorized_admin.movies_api.update_movie(movie_id, updated_data, expected_status=200)
        update_data = update_response.json()
        
        assert "id" in update_data, "В ответе отсутствует id фильма"
        assert update_data["id"] == movie_id
        assert update_data["name"] == updated_data["name"]
        assert update_data["price"] == 999
        
        get_response_for_update_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data_for_update_movie = get_response_for_update_movie.json()

        assert "id" in get_data_for_update_movie, "В ответе отсутствует id фильма"
        assert get_data_for_update_movie["id"] == movie_id
        assert get_data_for_update_movie["price"] == 999

    def test_delete_movie_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем удаления фильма на админской роли.
        """
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        data = create_response.json()
        
        assert "id" in data
        movie_id = data["id"]

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data, "В ответе отсутствует id фильма"
        assert get_data["id"] == movie_id
        assert get_data["price"] == movie_data["price"]
        assert get_data["genreId"] == movie_data["genreId"]
        assert get_data["name"] == movie_data["name"]
        assert get_data["description"] == movie_data["description"] 
        assert get_data["location"] == movie_data["location"]
        assert get_data["published"] == movie_data["published"]
        
        delete_response = authorized_admin.movies_api.delete_movie(movie_id, expected_status=200)
        delete_data = delete_response.json()

        assert "id" in delete_data
        assert delete_data["id"] == movie_id

        response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=404)
        response_data = response.json()

        assert "message" in response_data
        assert "Фильм не найден" in response_data["message"]
        assert "error" in response_data
        assert "Not Found" in response_data["error"]

    def test_get_filter_movies_by_location(self, api_manager):
        """
        Тестируем фильтр по локации на подборке фильма, публичная роль.
        """
        params = {"locations": "MSK"}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        movie_data = response.json()
        movies = movie_data['movies']
        
        assert 'movies' in movie_data
        assert isinstance(movies, list)
        for movie in movies:
            assert movie["location"] == "MSK"

    def test_pagination_list_for_movies(self, authorized_admin):
        """
        Проверяем пагинацию на админской роли.
        """
        resp1 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 1}, expected_status=200)
        resp2 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 2}, expected_status=200)
        movies1 = resp1.json()['movies']
        ids1 = [movie["id"] for movie in movies1]
        movies2 = resp2.json()['movies']
        ids2 = [movie["id"] for movie in movies2]

        assert len(movies1) == 5
        assert len(movies2) <= 5
        assert set(ids1).isdisjoint(set(ids2))

    def test_complex_filter_for_movies_list(self, authorized_admin, movie_query_params):
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

    def test_post_movie_with_left_boundary_values(self, authorized_admin, movie_data):
        """
        Проверяем левые (минимальные) граничные значения при создании фильма.
        """
        boundary_data = movie_data.copy()
        boundary_data["name"] = "Y"
        boundary_data["price"] = 1
        boundary_data["genreId"] = 1
        boundary_data["description"] = ""
        boundary_data["location"] = "MSK"
        boundary_data["published"] = True

        response = authorized_admin.movies_api.create_movie(boundary_data, expected_status=201)
        data = response.json()

        assert "id" in data
        movie_id = data["id"]

        assert data["price"] == boundary_data["price"]
        assert data["genreId"] == boundary_data["genreId"]
        assert data["name"] == boundary_data["name"]
        assert data["description"] == boundary_data["description"]
        assert data["location"] == boundary_data["location"]
        assert data["published"] == boundary_data["published"]

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data, "В ответе отсутствует id фильма"
        assert get_data["id"] == movie_id
        assert get_data["price"] == boundary_data["price"]
        assert get_data["genreId"] == boundary_data["genreId"]
        assert get_data["name"] == boundary_data["name"]
        assert get_data["description"] == boundary_data["description"] 
        assert get_data["location"] == boundary_data["location"]
        assert get_data["published"] == boundary_data["published"]

        authorized_admin.movies_api.clean_up_movie(data["id"])

    def test_post_movie_with_right_boundary_values(self, authorized_admin, movie_data):
        """
        Проверяем правые (максимальные) граничные значения при создании фильма.
        """
        boundary_data = movie_data.copy()
        boundary_data["price"] = 999999999
        boundary_data["genreId"] = 10
        boundary_data["location"] = "SPB"
        boundary_data["published"] = False

        response = authorized_admin.movies_api.create_movie(boundary_data, expected_status=201)
        data = response.json()

        assert "id" in data
        movie_id = data["id"]
        
        assert data["name"] == boundary_data["name"]
        assert data["price"] == boundary_data["price"]
        assert data["genreId"] == boundary_data["genreId"]
        assert data["location"] == boundary_data["location"]
        assert data["published"] == boundary_data["published"]

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data, "В ответе отсутствует id фильма"
        assert get_data["id"] == movie_id
        assert get_data["price"] == boundary_data["price"]
        assert get_data["genreId"] == boundary_data["genreId"]
        assert get_data["name"] == boundary_data["name"]
        assert get_data["description"] == boundary_data["description"] 
        assert get_data["location"] == boundary_data["location"]
        assert get_data["published"] == boundary_data["published"]
        
        authorized_admin.movies_api.clean_up_movie(data["id"])
