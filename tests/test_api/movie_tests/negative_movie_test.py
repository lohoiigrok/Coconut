class TestNegativeMoviesAPI:
    def test_post_movie_by_public_role_forbidden(self, api_manager, movie_data):
        """
        Тестируем, что публичный пользователь не может создать фильм.
        """
        response = api_manager.movies_api.create_movie(movie_data, expected_status=401)
        response_data = response.json()

        assert "message" in response_data
        assert "Unauthorized" in response_data["message"]
        assert "id" not in response_data


    def test_get_nonexistent_movie_id_by_public_role(self, api_manager):
        """
        Тестируем, что нельзя получить несуществующий фильм.
        """
        movie_id = -10
        response = api_manager.movies_api.get_single_movie(movie_id, expected_status=404)
        response_data = response.json()

        assert "message" in response_data
        assert "Фильм не найден" in response_data["message"]
        assert "error" in response_data
        assert "Not Found" in response_data["error"]
        assert "id" not in response_data


    def test_delete_movie_with_public_role_forbidden(self, created_movie, api_manager):
        """
        Тестируем, что публичный пользователь не может удалить фильм.
        """
        movie_id = created_movie['id']
        get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data, "В ответе отсутствует id фильма"
        assert get_data["id"] == movie_id
        assert get_data["price"] == created_movie["price"]
        assert get_data["genreId"] == created_movie["genreId"]
        assert get_data["name"] == created_movie["name"]
        assert get_data["description"] == created_movie["description"]
        assert get_data["location"] == created_movie["location"]
        assert get_data["published"] == created_movie["published"]
        
        delete_response = api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        delete_data = delete_response.json()

        assert "message" in delete_data
        assert "Unauthorized" in delete_data["message"]
        assert "id" not in delete_data

        get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data
        assert get_data["id"] == movie_id

    def test_post_movie_duplicate_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем возможность создать дубликат фильма на админской роли.
        """
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        create_data = create_response.json()

        assert "id" in create_data, "В ответе на создание фильма отсутствует id"
        movie_id = create_data['id']

        get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data, "В ответе отсутствует id фильма"
        assert get_data["id"] == movie_id
        assert get_data["price"] == create_data["price"]
        assert get_data["genreId"] == create_data["genreId"]
        assert get_data["name"] == create_data["name"]
        assert get_data["description"] == create_data["description"]
        assert get_data["location"] == create_data["location"]
        assert get_data["published"] == create_data["published"]
        
        duplicate_response = authorized_admin.movies_api.create_movie(movie_data, expected_status=409)
        duplicate_data = duplicate_response.json()

        assert "error" in duplicate_data
        assert "Conflict" in duplicate_data["error"]
        assert "id" not in duplicate_data
        
        authorized_admin.movies_api.clean_up_movie(movie_id)

    def test_post_movie_with_invalid_data_by_superadmin(self, authorized_admin, invalid_movie_data):
        """
        Тестируем создание фильма из невалидных данных. (несколько разных параметров)
        """
        for bad_data in invalid_movie_data:
            response = authorized_admin.movies_api.create_movie(bad_data, expected_status=400)
            response_data = response.json()

            assert "error" in response_data
            assert "Bad Request" in response_data["error"]
            assert "id" not in response_data

    def test_post_movie_with_invalid_genre_by_superadmin(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма с невалидным жанром.
        """
        bad_data = movie_data.copy()
        bad_data["genreId"] = 999999
        response = authorized_admin.movies_api.create_movie(bad_data,expected_status=400)
        response_data = response.json()

        assert "error" in response_data
        assert "Bad Request" in response_data["error"]
        assert "id" not in response_data

    def test_post_movie_empty_data_by_superadmin(self, authorized_admin):
        """
        Тестируем создание фильма из пустых данных на админской роли.
        """
        response = authorized_admin.movies_api.create_movie({}, expected_status=400)
        response_data = response.json()

        assert "error" in response_data
        assert "Bad Request" in response_data["error"]
        assert "id" not in response_data
