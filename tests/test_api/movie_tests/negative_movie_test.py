class TestNegativeMoviesAPI:
    def test_post_film_public_forbidden(self, api_manager, movie_data):
        """
        Тестируем, что публичный пользователь не может создать фильм.
        """
        response = api_manager.movies_api.create_movie(movie_data, expected_status=401)
        response_data = response.json()

        assert "message" in response_data
        assert "id" not in response_data


    def test_get_nonexistent_id(self, api_manager):
        """
        Тестируем, что нельзя получить несуществующий фильм.
        """
        movie_id = -10
        response = api_manager.movies_api.get_single_movie(movie_id, expected_status=404)
        response_data = response.json()

        assert "message" in response_data
        assert "id" not in response_data


    def test_delete_public_forbidden(self, created_movie, api_manager):
        """
        Тестируем, что публичный пользователь не может удалить фильм.
        """
        movie_id = created_movie['id']
        delete_response = api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        delete_data = delete_response.json()

        assert "message" in delete_data
        assert "id" not in delete_data

        get_response = api_manager.movies_api.get_single_movie(movie_id, expected_status=200)
        get_data = get_response.json()

        assert "id" in get_data
        assert get_data["id"] == movie_id

    def test_post_duplicate(self, authorized_admin, movie_data):
        """
        Тестируем возможность создать дубликат фильма на админской роли.
        """
        response1 = authorized_admin.movies_api.create_movie(movie_data)
        response_data1 = response1.json()

        assert "id" in response_data1, "В ответе на создание фильма отсутствует id"
        movie_id = response_data1['id']

        response2 = authorized_admin.movies_api.create_movie(movie_data, expected_status=409)
        response_data2 = response2.json()

        assert "message" in response_data2
        assert "id" not in response_data2
        authorized_admin.movies_api.clean_up_movie(movie_id)

    def test_post_invalid_data(self, authorized_admin, invalid_movie_data):
        """
        Тестируем создание фильма из невалидных данных. (несколько разных параметров)
        """
        for bad_data in invalid_movie_data:
            response = authorized_admin.movies_api.create_movie(bad_data, expected_status=400)
            response_data = response.json()

            assert "message" in response_data
            assert "id" not in response_data

    def test_post_invalid_genre(self, authorized_admin, movie_data):
        """
        Тестируем создание фильма с невалидным жанром.
        """
        bad_data = movie_data.copy()
        bad_data["genreId"] = 999999
        response = authorized_admin.movies_api.create_movie(bad_data,expected_status=400)
        response_data = response.json()

        assert "message" in response_data
        assert "Bad request" in response_data
        assert "id" not in response_data


    def test_post_empty_body(self, authorized_admin):
        """
        Тестируем создание фильма из пустых данных на админской роли.
        """
        response = authorized_admin.movies_api.create_movie({}, expected_status=400)
        response_data = response.json()

        assert "message" in response_data
        assert "Bad request" in response_data['error"]
        assert "id" not in response_data
