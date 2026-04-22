import pytest
from _pytest.fixtures import FixtureRequest

from roles import Roles
from models.models import MovieResponseModel, ErrorResponseModel, MovieListResponseModel


ROLE_TO_FIXTURE = {
    Roles.PUBLIC: "api_manager",
    Roles.USER: "authorized_user",
    Roles.SUPER_ADMIN: "authorized_admin",
}


class TestActionByRoles:
    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Roles.PUBLIC, 401),
            (Roles.USER, 403),
            (Roles.SUPER_ADMIN, 201),
        ], ids=["public_cannot_create", "user_cannot_create", "superadmin_can_create"],)
    def test_create_movie_by_role(self, request: FixtureRequest, movie_data: dict, role: Roles, expected_status: int):
        """
        PUBLIC → 401, USER → 403, SUPER_ADMIN → 201 при создании фильма.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        response = client.movies_api.create_movie(movie_data, expected_status=expected_status)
        data = response.json()

        if expected_status == 201:
            movie = MovieResponseModel(**data)
            assert movie.name == movie_data["name"]
            assert movie.price == movie_data["price"]
            client.movies_api.clean_up_movie(movie.id)
        else:
            error_response = ErrorResponseModel(**data)
            assert "Unauthorized" in str(error_response.error) or "Forbidden resource" in str(error_response.error)


    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Roles.PUBLIC, 200),
            (Roles.USER, 200),
            (Roles.SUPER_ADMIN, 200),
        ], ids=["public_can_get", "user_can_get", "superadmin_can_get"],)
    def test_get_movies_list_by_role(self, request: FixtureRequest, role: Roles, expected_status: int):
        """
        Три теста: PUBLIC, USER и SUPER_ADMIN могут получить список фильмов.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        response = client.movies_api.get_movies_list(
            {"pageSize": 5, "page": 1},
            expected_status=expected_status,
        )
        data = response.json()
        movie_list = MovieListResponseModel(**data)
        assert movie_list.pageSize == 5

    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Roles.PUBLIC, 401),
            (Roles.USER, 403),
            (Roles.SUPER_ADMIN, 200),
        ], ids=["public_cannot_delete", "user_cannot_delete", "superadmin_can_delete"],)
    def test_delete_movie_by_role(self, created_movie: dict, request: FixtureRequest, role: Roles, expected_status: int):
        """
        PUBLIC → 401 (фильм остаётся), USER → 403 (фильм остается),  SUPER_ADMIN → 200 (фильм удалён).
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        movie_id = created_movie["id"]

        delete_response = client.movies_api.delete_movie(movie_id, expected_status=expected_status)
        delete_data = delete_response.json()

        if expected_status == 200:
            deleted = MovieResponseModel(**delete_data)
            assert deleted.id == movie_id

            get_response = client.movies_api.get_single_movie(movie_id, expected_status=404)
            error_response = ErrorResponseModel(**get_response.json())
            assert "Not Found" in str(error_response.error)
        else:
            error_response = ErrorResponseModel(**delete_data)
            assert "Unauthorized" in str(error_response.message) or "Forbidden resource" in str(error_response.message)

            get_response = client.movies_api.get_single_movie(movie_id, expected_status=200)
            remaining = MovieResponseModel(**get_response.json())
            assert remaining.id == movie_id