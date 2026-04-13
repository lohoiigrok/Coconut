import pytest

class TestNegativeMoviesAPI:
    def test_post_public_forbidden(self, api_manager, movie_data):
        """
    | PUBLIC | Create movie -> 401 (forbidden) |
        """
        api_manager.movies_api.create_movie(movie_data, expected_status=401)

    def test_get_nonexistent_id(self, api_manager):
        """
        | PUBLIC | GET non-existing movie -> 404
        """
        movie_id = 999999
        api_manager.movies_api.get_single_movie(movie_id, expected_status=404)

    def test_delete_public_forbidden(self, api_manager):
        """
        | PUBLIC | Delete movie -> forbidden access
        """
        movie_id=1500
        api_manager.movies_api.delete_movie(movie_id, expected_status=401)

    def test_post_duplicate(self, authorized_admin, movie_data):
        """
        | SUPER_ADMIN | Duplicate POST movie
        """
        movie = movie_data
        response = authorized_admin.movies_api.create_movie(movie)
        movie_id = response.json()['id']
        authorized_admin.movies_api.create_movie(movie, expected_status=409)

        authorized_admin.movies_api.clean_up_movie(movie_id)

    def test_post_invalid_data(self, authorized_admin, invalid_movie_data):
        """
        | SUPER_ADMIN | Invalid data -> 400/422
        """
        for bad_data in invalid_movie_data:
            authorized_admin.movies_api.create_movie(bad_data, expected_status=400)

    def test_post_invalid_genre(self, authorized_admin, movie_data):
        bad_data = movie_data.copy()
        bad_data["genreId"] = 999999
        authorized_admin.movies_api.create_movie(bad_data,expected_status=400)

    def test_post_empty_body(self, authorized_admin):
        authorized_admin.movies_api.create_movie({}, expected_status=400)