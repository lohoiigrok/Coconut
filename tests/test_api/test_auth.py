import pytest
from test_super_duper.utils.data_generator import DataGenerator
import requests

class TestMoviesAPI:

    def test_01_get_movies_public(self, public_requester):
        """
        Позитив | PUBLIC | GET список фильмов
        ДАННЫЕ: pageSize=10, pageNumber=1
        ОЖИДАЕМО: 200 + {"movies": [...]}
        """
        response = public_requester.get_movies({"pageSize": 10, "pageNumber": 1})
        assert response.get("statusCode", 200) == 200
        assert "movies" in response

    def test_02_post_movie_auth(self, auth_requester, movie_data):
        """
        Позитив | SUPER_ADMIN | POST валидные данные
        ДАННЫЕ: movie_data() → name, description, price, location, genreId
        ОЖИДАЕМО: 201 + {"id": UUID, name, description...}
        """
        response = auth_requester.post_movie(movie_data)
        if "statusCode" in response:  # Ошибка
            print(f"ERROR: {response}")  # Debug
            pytest.fail(f"POST failed: {response}")
        assert "id" in response

    def test_03_post_movie_auth(self, auth_requester, movie_data):
        """
        Позитив | SUPER_ADMIN | Дублированный POST
        ДАННЫЕ: movie_data() повторно
        ОЖИДАЕМО: 201 + новый фильм
        """
        response = auth_requester.post_movie(movie_data)
        assert "id" in response

    def test_04_patch_movie_auth(self, auth_requester, movie_data):
        """
        Позитив | SUPER_ADMIN | PATCH динамического фильма
        ДАННЫЕ: movie_data
        ОЖИДАЕМО:
        - 200 + {id, name, price...} (обновлен)
        - 404/405 (read-only/метод отключен)
        """
        # Создаем фильм сначала
        create_response = auth_requester.post_movie(movie_data)
        movie_id = create_response["id"]

        # PATCH на только что созданный
        response = auth_requester.patch_movie(movie_id, movie_data)

        if "statusCode" in response:
            # Ошибка API
            status = response["statusCode"]
            assert status in [404, 405], f"PATCH failed: {status}"
            print(f"PATCH {status} OK: {response['message']}")
        else:
            # Успех = возвращает обновленный объект
            assert "id" in response
            assert response["id"] == movie_id, "ID не изменился"

    def test_05_post_public_forbidden(self, public_requester, movie_data):
        """
        Негатив | PUBLIC | Недостаточно прав
        ДАННЫЕ: movie_data()
        ОЖИДАЕМО: 401/403
        """
        response = public_requester.post_movie(movie_data)
        assert response.get("statusCode") in [401, 403]

    def test_06_get_nonexistent_id(self, public_requester):
        """
        Негатив | PUBLIC | Не существует
        ДАННЫЕ: movie_id=999999
        ОЖИДАЕМО: 404
        """
        movie_id = 999999
        response = public_requester.get_movie(movie_id)
        assert response.get("statusCode") == 404

    def test_07_delete_movie_auth(self, auth_requester, movie_data):
        """
        Позитив | SUPER_ADMIN | DELETE динамического фильма
        ДАННЫЕ: movie_data
        ОЖИДАЕМО: 200/204 + {message: "Movie deleted"}
        """
        # Создаем → удаляем
        create_response = auth_requester.post_movie(movie_data)
        movie_id = create_response["id"]

        # Удаляю
        auth_requester.delete_movie(movie_id)

        # ЧЕкаем удалился ли фильм по настоящему
        response = auth_requester.get_movie(movie_id)
        assert response.get("statusCode") == 404, "Movie not deleted!"

    def test_08_delete_public_forbidden(self, public_requester):
        """
        Негатив | PUBLIC | Недостаточно прав
        ДАННЫЕ: movie_id=1500
        ОЖИДАЕМО: 401/403
        """
        response = public_requester.delete_movie(1500)
        assert response.get("statusCode") in [401, 403]

    def test_09_post_duplicate(self, auth_requester):
        """
        Негатив | SUPER_ADMIN | Неполные данные
        ДАННЫЕ: {title, locations} без required полей
        ОЖИДАЕМО: 400/422
        """
        response = auth_requester.post_movie({"title": "Дубль", "locations": ["MSK"]})
        assert response.get("statusCode") in [400, 422]

    def test_10_get_filter_location(self, public_requester):
        """
        Позитив | PUBLIC | Фильтр по локации
        ДАННЫЕ: locations=MSK
        ОЖИДАЕМО: 200 + {"movies": [...], count}
        """
        response = public_requester.get_movies({"locations": "MSK"})
        assert response.get("statusCode", 200) == 200
        assert "movies" in response

    def test_11_pagination_auth(self, auth_requester):
        """
        Позитив | SUPER_ADMIN | Пагинация
        ДАННЫЕ: pageSize=5, pageNumber=1/2
        ОЖИДАЕМО: 200 + разные страницы
        """
        resp1 = auth_requester.get_movies({"pageSize": 5, "pageNumber": 1})
        resp2 = auth_requester.get_movies({"pageSize": 5, "pageNumber": 2})
        assert "movies" in resp1 and "movies" in resp2

    def test_12_post_invalid_data(self, auth_requester, invalid_movies_data):
        """
        Негатив | SUPER_ADMIN | Невалидные данные (типы/границы)
        ДАННЫЕ: invalid_movies_data() x6
        ОЖИДАЕМО: 400/422 для каждого
        """
        for bad_data in invalid_movies_data:
            resp = auth_requester.post_movie(bad_data)
            assert resp.get("statusCode") in [400, 422]

    def test_13_complex_query(self, auth_requester, movie_query):
        """
        Позитив | SUPER_ADMIN | Сложный фильтр
        ДАННЫЕ: movie_query_params()
        ОЖИДАЕМО: 200 + фильтрованный список
        """
        response = auth_requester.get_movies(movie_query)
        assert "movies" in response

    # Дополнительные тесты

    def test_14_post_boundary_values(self, auth_requester, movie_data):
        """
        Позитив | SUPER_ADMIN | Граничные валидные значения
        ДАННЫЕ: price=50(min)/1000(max), name=1/255 символов
        ОЖИДАЕМО: 201
        """
        boundary_data = movie_data.copy()
        boundary_data["price"] = 50  # min
        boundary_data["genreId"] = 1  # min
        response = auth_requester.post_movie(boundary_data)
        assert "id" in response

    @pytest.mark.parametrize("bad_case", [
        pytest.param(DataGenerator.invalid_movie_data()[0], id="no_name"),
        pytest.param({"name": "Test", "price": -1}, id="negative_price"),
        pytest.param({"name": "Test", "price": 1001}, id="price_too_big"),
        pytest.param({"name": "Test", "genreId": "abc"}, id="wrong_type")
    ])
    def test_15_post_negative_types(self, auth_requester, bad_case):
        """Негативные типы/границы"""
        response = auth_requester.post_movie(bad_case)
        assert response.get("statusCode") in [400, 422]

    # @pytest.mark.parametrize("expected_status", [404, 405])
    def test_16_patch_genre_auth(self, auth_requester, genre_data):
        """
        Позитив | SUPER_ADMIN | PATCH динамического жанра
        ДАННЫЕ: genre_data
        ОЖИДАЕМО:
        - 200 + {id, name} (обновлен)
        - 404/405 (read-only for PUBLIC ROLE)
        """
        # Создаем жанр сначала
        genre_id = requests.post(
            f"{auth_requester.base_url}/genres",
            json=genre_data,
            headers=auth_requester.headers
        ).json()["id"]

        # PATCH
        response = auth_requester.patch_genre(genre_id, genre_data)

        if "statusCode" in response:
            assert response["statusCode"] in [404, 405], f"PATCH genre failed"
        else:
            assert "id" in response
            assert response["id"] == genre_id, "Genre ID не изменился"
