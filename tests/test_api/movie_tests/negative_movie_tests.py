import pytest
import requests

class TestNegativeMoviesAPI:
    def test_05_post_public_forbidden(self, api_manager, movie_data):
        """
        Негатив | PUBLIC | Недостаточно прав
        ДАННЫЕ: movie_data()
        ОЖИДАЕМО: 401/403
        """
        response = api_manager.movies_api.create_movie(movie_data, expected_status=401)
        # Проверки
        assert response.status_code in [401, 403]

    def test_06_get_nonexistent_id(self, api_manager):
        """
        Негатив | PUBLIC | Не существует
        ДАННЫЕ: movie_id=999999
        ОЖИДАЕМО: 404
        """
        movie_id = 999999
        response = api_manager.movies_api.get_single_movie(movie_id, expected_status=404)
        assert response.status_code == 404

    def test_08_delete_public_forbidden(self, api_manager):
        """
        Негатив | PUBLIC | Недостаточно прав
        ДАННЫЕ: movie_id=1500
        ОЖИДАЕМО: 401/403
        """
        movie_id=1500
        response = api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        assert response.status_code in [401, 403]

    def test_09_post_duplicate(self, authorized_admin):
        """
        Негатив | SUPER_ADMIN | Неполные данные
        ДАННЫЕ: {title, locations} без required полей
        ОЖИДАЕМО: 400/422
        """
        response = authorized_admin.movies_api.create_movie({"title": "Дубль", "locations": ["MSK"]}, expected_status=400)
        assert response.status_code in [400, 422]

    def test_12_post_invalid_data(self, authorized_admin, invalid_movie_data):
        """
        Негатив | SUPER_ADMIN | Невалидные данные (типы/границы)
        ДАННЫЕ: invalid_movies_data() x6
        ОЖИДАЕМО: 400/422 для каждого
        """
        for bad_data in invalid_movie_data:
            response = authorized_admin.movies_api.create_movie(bad_data, expected_status=400)
            assert response.status_code in [400, 422]