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
        create_response = authorized_admin.movies_api.create_movie(movie_data, expected_status=201)
        create_data = create_response.json()
        
        assert "id" in create_data
        movie_id = create_data["id"]
        
        assert isinstance(movie_id, int)
        assert create_data["price"] == movie_data["price"]
        assert create_data["genreId"] == movie_data["genreId"]
        assert create_data["name"] == movie_data["name"]
        assert create_data["description"] == movie_data["description"] 
        assert create_data["location"] == movie_data["location"]
        assert create_data["published"] == movie_data["published"]
        
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
        
        authorized_admin.movies_api.clean_up_movie(create_data["id"])

    def test_patch_movie_by_superadmin(self,created_movie, authorized_admin, movie_data):
        """
        Проверяем возможность изменения данных в созданном фильме на админской роли.
        """
        movie_id = created_movie["id"]
        get_response_create_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data_created_movie = get_response_create_movie.json()

        assert "id" in get_data_created_movie, "В ответе отсутствует id фильма"
        assert get_data_created_movie["id"] == movie_id
        assert get_data_created_movie["price"] == movie_data["price"]
        assert get_data_created_movie["genreId"] == movie_data["genreId"]
        assert get_data_created_movie["name"] == movie_data["name"]
        assert get_data_created_movie["description"] == movie_data["description"] 
        assert get_data_created_movie["location"] == movie_data["location"]
        assert get_data_created_movie["published"] == movie_data["published"]
        
        updated_data = movie_data.copy()
        updated_data['price'] = 999
        update_response = authorized_admin.movies_api.update_movie(movie_id, updated_data, expected_status=200)
        update_data = update_response.json()
        
        assert "id" in update_data, "В ответе отсутствует id фильма"
        assert update_data["id"] == movie_id
        assert update_data["name"] == updated_data["name"]
        assert update_data["price"] == 999
        
        get_response_updated_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data_updated_movie = get_response_updated_movie.json()

        assert "id" in get_data_updated_movie, "В ответе отсутствует id фильма"
        assert get_data_updated_movie["id"] == movie_id
        assert get_data_updated_movie["price"] == 999

    def test_delete_movie_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем удаления фильма на админской роли.
        """
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        data = create_response.json()
        
        assert "id" in data
        movie_id = data["id"]

        get_response_created_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data_created_movie = get_response_created_movie.json()

        assert "id" in get_data_created_movie, "В ответе отсутствует id фильма"
        assert get_data_created_movie["id"] == movie_id
        assert get_data_created_movie["price"] == movie_data["price"]
        assert get_data_created_movie["genreId"] == movie_data["genreId"]
        assert get_data_created_movie["name"] == movie_data["name"]
        assert get_data_created_movie["description"] == movie_data["description"] 
        assert get_data_created_movie["location"] == movie_data["location"]
        assert get_data_created_movie["published"] == movie_data["published"]
        
        delete_response = authorized_admin.movies_api.delete_movie(movie_id, expected_status=200)
        delete_data = delete_response.json()

        assert "id" in delete_data
        assert delete_data["id"] == movie_id

        get_response_deleted_movie = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=404)
        get_data_deleted_movie = get_response_deleted_movie.json()

        assert "message" in get_data_deleted_movie
        assert "Фильм не найден" in get_data_deleted_movie["message"]
        assert "error" in get_data_deleted_movie
        assert "Not Found" in get_data_deleted_movie["error"]

    def test_get_filter_movies_by_location(self, api_manager):
        """
        Тестируем фильтр по локации на подборке фильма, публичная роль.
        """
        params = {"locations": "MSK"}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        movie_data = response.json()

        assert 'movies' in movie_data
        movies = movie_data['movies']
        
        assert isinstance(movies, list)
        for movie in movies:
            assert movie["location"] == "MSK"

    def test_pagination_list_for_movies(self, authorized_admin):
        """
        Проверяем пагинацию на админской роли.
        """
        response_list1 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 1}, expected_status=200)
        response_list2 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 2}, expected_status=200)
        movies_list1 = response_list1.json()['movies']
        ids_list1 = [movie["id"] for movie in movies_list1]
        movies_list2 = response_list2.json()['movies']
        ids_list2 = [movie["id"] for movie in movies_list2]

        assert len(movies_list1) == 5
        assert len(movies_list2) <= 5
        assert set(ids_list1).isdisjoint(set(ids_list2))

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

        create_response = authorized_admin.movies_api.create_movie(boundary_data, expected_status=201)
        create_data = create_response.json()

        assert "id" in create_data
        movie_id = create_data["id"]

        assert create_data["price"] == boundary_data["price"]
        assert create_data["genreId"] == boundary_data["genreId"]
        assert create_data["name"] == boundary_data["name"]
        assert create_data["description"] == boundary_data["description"]
        assert create_data["location"] == boundary_data["location"]
        assert create_data["published"] == boundary_data["published"]

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

        authorized_admin.movies_api.clean_up_movie(create_data["id"])

    def test_post_movie_with_right_boundary_values(self, authorized_admin, movie_data):
        """
        Проверяем правые (максимальные) граничные значения при создании фильма.
        """
        boundary_data = movie_data.copy()
        boundary_data["price"] = 999999999
        boundary_data["genreId"] = 10
        boundary_data["location"] = "SPB"
        boundary_data["published"] = False

        create_response = authorized_admin.movies_api.create_movie(boundary_data, expected_status=201)
        create_data = create_response.json()

        assert "id" in create_data
        movie_id = create_data["id"]
        
        assert create_data["name"] == boundary_data["name"]
        assert create_data["price"] == boundary_data["price"]
        assert create_data["genreId"] == boundary_data["genreId"]
        assert create_data["location"] == boundary_data["location"]
        assert create_data["published"] == boundary_data["published"]

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
        
        authorized_admin.movies_api.clean_up_movie(create_data["id"])
