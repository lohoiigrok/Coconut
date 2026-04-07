from testsam.constants import MOVIES_ENDPOINT, MOVIE_BASE_URL
from testsam.customer_requester.custom_requester import CustomRequester

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIE_BASE_URL)
        self.session = session

    def create_movie(self, movie_data, expected_status=201):
        """"
        Создание нового фильма
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )


    def get_movies_list(self, data=None):
        """
        Получение списка фильмов
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            data=data
        )

    def get_single_movie(self, movie_id, expected_status=200):
        """
        Получение отдельного фильма по ID
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def update_movie(self, movie_id, movie_data):
        """
        Обновление фильма.
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=movie_data,
        )

    def delete_movie(self, movie_id, expected_status=204):
        """
        Удаление фильмаю
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def clean_up_movie(self, movie_id):
        """Очистка фильма ПОСЛЕ теста (без проверки статуса)."""
        self.delete_movie(movie_id, expected_status=None)


    def patch_genre(self, genre_id, data, expected_status):
        """PATCH /genres/{id}"""
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/genres/{genre_id}",
            data=data,
            expected_status=expected_status
        )