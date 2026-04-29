import pytest
from _pytest.fixtures import FixtureRequest
from testsam.types.parametrized_constants import (ROLE_TO_FIXTURE,
                                    CREATE_MOVIE_SUCCESS_BY_ROLE,
                                    CREATE_MOVIE_SUCCESS_BY_ROLE_IDS,
                                    CREATE_MOVIE_FORBIDDEN_BY_ROLE,
                                    CREATE_MOVIE_FORBIDDEN_BY_ROLE_IDS,
                                    GET_MOVIES_LIST_BY_ROLE,
                                    GET_MOVIES_LIST_BY_ROLE_IDS,
                                    DELETE_MOVIE_SUCCESS_BY_ROLE,
                                    DELETE_MOVIE_SUCCESS_BY_ROLE_IDS,
                                    DELETE_MOVIE_FORBIDDEN_BY_ROLE,
                                    DELETE_MOVIE_FORBIDDEN_BY_ROLE_IDS
)
from roles import Roles
from models.models import MovieResponseModel, ErrorResponseModel, MovieListResponseModel

class TestActionByRoles:
    @pytest.mark.parametrize(
        "role, expected_status",
        CREATE_MOVIE_SUCCESS_BY_ROLE,
        ids=CREATE_MOVIE_SUCCESS_BY_ROLE_IDS,
    )
    def test_superadmin_can_create_movie(
            self,
            request: FixtureRequest,
            movie_data: dict,
            role: Roles,
            expected_status: int,
    ):
        """
        SUPER_ADMIN → 201 при создании фильма.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        response = client.movies_api.create_movie(movie_data, expected_status=expected_status)
        data = response.json()

        movie = MovieResponseModel(**data)
        assert movie.name == movie_data["name"]
        assert movie.price == movie_data["price"]

        client.movies_api.clean_up_movie(movie.id)

    @pytest.mark.parametrize(
        "role, expected_status",
        CREATE_MOVIE_FORBIDDEN_BY_ROLE,
        ids=CREATE_MOVIE_FORBIDDEN_BY_ROLE_IDS,
    )
    def test_non_superadmin_cannot_create_movie(
            self,
            request: FixtureRequest,
            movie_data: dict,
            role: Roles,
            expected_status: int,
    ):
        """
        PUBLIC → 401, USER → 403 при создании фильма.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        response = client.movies_api.create_movie(movie_data, expected_status=expected_status)
        data = response.json()

        error_response = ErrorResponseModel(**data)
        assert "Unauthorized" in str(error_response.error) or "Forbidden resource" in str(error_response.error)

    @pytest.mark.parametrize(
        "role",
        GET_MOVIES_LIST_BY_ROLE,
        GET_MOVIES_LIST_BY_ROLE_IDS)
    def test_get_movies_list_by_role(self, request: FixtureRequest, role: Roles, expected_status: int):
        """
        Три теста: PUBLIC, USER и SUPER_ADMIN могут получить список фильмов.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        response = client.movies_api.get_movies_list(
            {"pageSize": 5, "page": 1},
            expected_status=200,
        )
        data = response.json()
        movie_list = MovieListResponseModel(**data)
        assert movie_list.pageSize == 5

    @pytest.mark.parametrize(
        "role, expected_status",
        DELETE_MOVIE_SUCCESS_BY_ROLE,
        ids=DELETE_MOVIE_SUCCESS_BY_ROLE_IDS,
    )
    def test_superadmin_can_delete_movie(
            self,
            created_movie: dict,
            request: FixtureRequest,
            role: Roles,
            expected_status: int,
    ):
        """
        SUPER_ADMIN → 200 (фильм удалён).
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        movie_id = created_movie["id"]

        delete_response = client.movies_api.delete_movie(movie_id, expected_status=expected_status)
        delete_data = delete_response.json()

        deleted = MovieResponseModel(**delete_data)
        assert deleted.id == movie_id

        get_response = client.movies_api.get_single_movie(movie_id, expected_status=404)
        error_response = ErrorResponseModel(**get_response.json())
        assert "Not Found" in str(error_response.error)

    @pytest.mark.parametrize(
        "role, expected_status",
        DELETE_MOVIE_FORBIDDEN_BY_ROLE,
        ids=DELETE_MOVIE_FORBIDDEN_BY_ROLE_IDS,
    )
    def test_non_superadmin_cannot_delete_movie(
            self,
            created_movie: dict,
            request: FixtureRequest,
            role: Roles,
            expected_status: int,
    ):
        """
        PUBLIC → 401, USER → 403 (фильм остаётся).
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])
        movie_id = created_movie["id"]

        delete_response = client.movies_api.delete_movie(movie_id, expected_status=expected_status)
        delete_data = delete_response.json()

        error_response = ErrorResponseModel(**delete_data)
        assert "Unauthorized" in str(error_response.message) or "Forbidden resource" in str(error_response.message)

        get_response = client.movies_api.get_single_movie(movie_id, expected_status=200)
        remaining = MovieResponseModel(**get_response.json())
        assert remaining.id == movie_id