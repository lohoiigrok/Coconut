class TestPositiveMoviesAPI:
    def test_01_get_movies_public(self, api_manager):
        """
        Позитив | PUBLIC | GET список фильмов
        ДАННЫЕ: pageSize=10, pageNumber=1
        ОЖИДАЕМО: 200 + {"movies": [...]}
        """
        params = {"pageSize": 10, "pageNumber": 1}
        response = api_manager.movies_api.get_movies_list(params)

        # Проверки
        assert response.status_code == 200

        # Cмотрим JSON
        movie_data = response.json()
        assert "movies" in movie_data

    def test_02_post_movie_auth(self, authorized_admin, movie_data):
        """
        Позитив | SUPER_ADMIN | POST валидные данные
        ДАННЫЕ: movie_data() → name, description, price, location, genreId
        ОЖИДАЕМО: 201 + {"id": UUID, name, description...}
        """
        response = authorized_admin.movies_api.create_movie(movie_data)
        assert response.status_code == 201, "Хьюстон, у нас проблемы."

    def test_04_patch_movie_auth(self, authorized_admin, movie_data):
        """
        Позитив | SUPER_ADMIN | PATCH динамического фильма
        ДАННЫЕ: movie_data
        ОЖИДАЕМО:
        - 200 + {id, name, price...} (обновлен)
        - 404/405 (read-only/метод отключен)
        """
        # Создаем фильм сначала
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        # PATCH на только что созданный
        response = authorized_admin.movies_api.update_movie(movie_id, movie_data)
        data = response.json()

        if response.status_code in [200, 201]:
            data = response.json()
            assert data["id"] == movie_id
        else:
            assert response.status_code in [404, 405]

    def test_07_delete_movie_auth(self, authorized_admin, movie_data):
        """
        Позитив | SUPER_ADMIN | DELETE динамического фильма
        ДАННЫЕ: movie_data
        ОЖИДАЕМО: 200/204 + {message: "Movie deleted"}
        """
        # Создаем → удаляем
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]

        # Удаляю
        authorized_admin.movies_api.delete_movie(movie_id)

        # Чекаем удалился ли фильм по настоящему
        response = authorized_admin.movies_api.get_single_movie(movie_id)
        assert response.status_code == 404, "Movie not deleted!"

    def test_10_get_filter_location(self, api_manager):
        """
        Позитив | PUBLIC | Фильтр по локации
        ДАННЫЕ: locations=MSK
        ОЖИДАЕМО: 200 + {"movies": [...], count}
        """
        params = {"location": "MSK"}
        response = api_manager.movies_api.get_movies_list(params)

        # Проверки
        assert response.status_code == 200

        # Cмотрим и проверяем JSON на наличие "movies"
        movie_data = response.json()
        assert "movies" in movie_data

    def test_11_pagination_auth(self, authorized_admin):
        """
        Позитив | SUPER_ADMIN | Пагинация
        ДАННЫЕ: pageSize=5, pageNumber=1/2
        ОЖИДАЕМО: 200 + разные страницы
        """
        params = {"location": "MSK"}
        response = authorized_admin.movies_api.get_movies_list(params)

        resp1 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "pageNumber": 1})
        resp2 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "pageNumber": 2})
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        assert resp1.json()["movies"] != resp2.json()["movies"], "Хьюстон у нас проблемы"

    def test_13_complex_query(self, authorized_admin, movie_query_params):
        """
        Позитив | SUPER_ADMIN | Сложный фильтр
        ДАННЫЕ: movie_query_params()
        ОЖИДАЕМО: 200 + фильтрованный список
        """
        response = authorized_admin.movies_api.get_movies_list(movie_query_params)
        assert "movies" in response.json()

    # Дополнительные тесты

    def test_14_post_boundary_values(self, authorized_admin, movie_data):
        """
        Позитив | SUPER_ADMIN | Граничные валидные значения
        ДАННЫЕ: price=50(min)/1000(max), name=1/255 символов
        ОЖИДАЕМО: 201
        """
        boundary_data = movie_data.copy()
        boundary_data["price"] = 50  # min
        boundary_data["genreId"] = 1  # min
        response = authorized_admin.movies_api.create_movie(boundary_data)
        assert "id" in response.json()

    # @pytest.mark.parametrize("expected_status", [404, 405])
    def test_16_patch_genre_auth(self, authorized_admin, genre_data):
        """
        Позитив | SUPER_ADMIN | PATCH динамического жанра
        ДАННЫЕ: genre_data
        ОЖИДАЕМО:
        - 200 + {id, name} (обновлен)
        - 404/405 (read-only for PUBLIC ROLE)
        """
        # PATCH
        genre_id = 2
        response = authorized_admin.movies_api.patch_genre(genre_id, genre_data, expected_status=None)
        data = response.json()
        if "statusCode" in data:
            assert data["statusCode"] in [404, 405], "PATCH genre failed"
        else:
            assert "id" in data
            assert data["id"] == genre_id, "Genre ID не изменился"
