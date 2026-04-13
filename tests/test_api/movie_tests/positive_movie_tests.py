import pytest

class TestPositiveMoviesAPI:
    def test_get_movies_public(self, api_manager):
        """
        PUBLIC | GET movies -> movie list
        """
        params = {"pageSize": 10, "page": 1}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        data = response.json()

        assert 'movies' in data
        assert isinstance(data['movies'], list)

    def test_post_movie_auth(self, created_movie):
        """
        SUPER_ADMIN | Post movie -> expected created movie
        """
        data = created_movie
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_patch_movie_auth(self,created_movie, authorized_admin, movie_data):
        """
        SUPER_ADMIN | PATCH movie -> expected updated movie |
        """
        create_response = created_movie
        movie_id = create_response["id"]
        updated_data = movie_data.copy()
        updated_data['price'] = 999
        authorized_admin.movies_api.update_movie(movie_id, updated_data, expected_status=200)
        response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
        data = response.json()

        assert data["id"] == movie_id
        assert data["price"] == 999

    def test_delete_movie_auth(self, authorized_admin, movie_data):
        """
        SUPER_ADMIN | DELETE movie -> movie was deleted
        """
        create_response = authorized_admin.movies_api.create_movie(movie_data)
        movie_id = create_response.json()["id"]
        authorized_admin.movies_api.delete_movie(movie_id, expected_status=200)
        authorized_admin.movies_api.get_single_movie(movie_id, expected_status=404)

    def test_get_filter_location(self, api_manager):
        """
        PUBLIC | Get movies with params -> certain list of movies
        """
        params = {"locations": "MSK"}
        response = api_manager.movies_api.get_movies_list(params, expected_status=200)
        movie_data = response.json()
        movies = movie_data['movies']
        
        assert 'movies' in movie_data
        assert isinstance(movies, list)
        for movie in movies:
            assert movie["location"] == "MSK"

    def test_pagination(self, authorized_admin):
        """
        SUPER_ADMIN | Check pagination
        """
        params = {"location": "MSK"}
        authorized_admin.movies_api.get_movies_list(params)

        resp1 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 1}, expected_status=200)
        resp2 = authorized_admin.movies_api.get_movies_list({"pageSize": 5, "page": 2}, expected_status=200)
        movies1 = resp1.json()['movies']
        movies2 = resp2.json()['movies']

        assert movies1 != movies2 or len(movies2) == 0

    def test_complex_filter(self, authorized_admin, movie_query_params):
        """
        SUPER_ADMIN | Filter with many params
        """
        response = authorized_admin.movies_api.get_movies_list(movie_query_params)
        data = response.json()

        assert 'movies' in data
        assert len(data['movies']) > 0


    def test_post_boundary_values(self, authorized_admin, movie_data):
        """
        | SUPER_ADMIN | Boundary means
        """
        boundary_data = movie_data.copy()
        boundary_data["price"] = 50  # min
        boundary_data["genreId"] = 1  # min

        response = authorized_admin.movies_api.create_movie(boundary_data, expected_status=201)
        data = response.json()
        
        assert "id" in data
        assert data["price"] == 50

        authorized_admin.movies_api.clean_up_movie(data["id"])


    def test_patch_genre(self, authorized_admin, genre_data):
        """
        SUPER_ADMIN | PATCH genre -> updated genre
        """
        genre_id = 2

        response = authorized_admin.movies_api.patch_genre(genre_id, genre_data, expected_status=200)
        data = response.json()

        assert "id" in data
        assert data["id"] == genre_id, "Genre ID не изменился"
