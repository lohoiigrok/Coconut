import pytest
import requests
from constants import AUTH_BASE_URL, BASE_URL, HEADERS, LOGIN_ENDPOINT, SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD
from test_super_duper.utils.data_generator import DataGenerator

class APIMoviesClient:
    def __init__(self, token=None):
        self.base_url = BASE_URL
        self.headers = HEADERS.copy()
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_movies(self, params=None):
        response = requests.get(f"{self.base_url}/movies", headers=self.headers, params=params or {})
        return self._safe_response(response)

    def get_movie(self, movie_id):
        response = requests.get(f"{self.base_url}/movies/{movie_id}", headers=self.headers)
        return self._safe_response(response)

    def post_movie(self, data):
        response = requests.post(f"{self.base_url}/movies", json=data, headers=self.headers)
        return self._safe_response(response)

    def patch_movie(self, movie_id, data):
        response = requests.patch(f"{self.base_url}/movies/{movie_id}", json=data, headers=self.headers)
        return self._safe_response(response)

    def delete_movie(self, movie_id):
        response = requests.delete(f"{self.base_url}/movies/{movie_id}", headers=self.headers)
        return self._safe_response(response)

    def patch_genre(self, genre_id, data):
        """PATCH /genres/{id}"""
        response = requests.patch(
            f"{self.base_url}/genres/{genre_id}",
            json=data,
            headers=self.headers
        )
        return self._safe_response(response)

    @staticmethod
    def _safe_response(response):
        """Парсер ответов"""
        try:
            return response.json()
        except:
            return {"statusCode": response.status_code, "message": response.text}


# Попробовал через scope
@pytest.fixture(scope="session")
def login_token():
    """SUPER_ADMIN токен"""
    response = requests.post(
        f"{AUTH_BASE_URL}{LOGIN_ENDPOINT}",
        json={"email": SUPER_ADMIN_EMAIL, "password": SUPER_ADMIN_PASSWORD}
    )
    assert response.status_code == 200
    return response.json()["accessToken"]

@pytest.fixture
def auth_requester(login_token):
    """SUPER_ADMIN клиент"""
    return APIMoviesClient(token=login_token)

@pytest.fixture
def public_requester():
    """PUBLIC клиент"""
    return APIMoviesClient()

# Фикстуры по данным фильма (после класса APIMoviesClient)
@pytest.fixture
def movie_data():
    """ Валидный фильм"""
    return DataGenerator.movie_data()

@pytest.fixture
def invalid_movies_data():
    """ Невалидные фильмы"""
    return DataGenerator.invalid_movie_data()

@pytest.fixture
def movie_query():
    """ Query параметры"""
    return DataGenerator.movie_query_params()

@pytest.fixture
def genre_data():
    return DataGenerator.genre_data() # Использую такую реализацию, чтобы спрятать внутрянку генератора

