import requests
from testsam.constants import MOVIES_ENDPOINT, MOVIE_BASE_URL
from testsam.customer_requester.custom_requester import CustomRequester
from typing import Dict, Iterable, Any, Optional, Union

# Типы данных
MovieData = Dict[str, Any]
StatusCode = Union[int, Iterable[int], None]

class MoviesApi(CustomRequester):
    def __init__(self, session: requests.Session) -> None:
        super().__init__(session=session, base_url=MOVIE_BASE_URL)

    def create_movie(self, movie_data: MovieData, expected_status: StatusCode=201) -> requests.Response:
        """"
        Создание нового фильма
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )


    def get_movies_list(self, data: Optional[MovieData]=None, expected_status: StatusCode=200) -> requests.Response:
        """
        Получение списка фильмов
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            data=data,
            expected_status=expected_status
        )

    def get_single_movie(self, movie_id: int, expected_status: StatusCode=200)  -> requests.Response:
        """
        Получение отдельного фильма по ID
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def update_movie(self, movie_id: int, movie_data: MovieData, expected_status: StatusCode =200)  -> requests.Response:
        """
        Обновление фильма.
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id: int, expected_status: StatusCode=200)  -> requests.Response:
        """
        Удаление фильмаю
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def clean_up_movie(self, movie_id: int) -> None:
        """Очистка фильма ПОСЛЕ теста (без проверки статуса)."""
        try:
           self.delete_movie(movie_id, expected_status=200)
        except:
            pass

    def patch_genre(self, genre_id: int, data: MovieData, expected_status: StatusCode) -> requests.Response:
        """PATCH /genres/{id}"""
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/genres/{genre_id}",
            data=data,
            expected_status=expected_status
        )