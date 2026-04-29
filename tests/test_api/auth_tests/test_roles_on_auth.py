import pytest
from _pytest.fixtures import FixtureRequest
from types.parametrized_constants import (
    ROLE_TO_FIXTURE,
    LOGIN_VALID_BY_ROLE,
    LOGIN_VALID_BY_ROLE_IDS,
    LOGIN_INVALID_PASSWORD_BY_ROLE,
    LOGIN_INVALID_PASSWORD_BY_ROLE_IDS,
    CREATE_USER_SUCCESS_BY_ROLE,
    CREATE_USER_SUCCESS_BY_ROLE_IDS,
    CREATE_USER_FORBIDDEN_BY_ROLE,
    CREATE_USER_FORBIDDEN_BY_ROLE_IDS
)
from roles import Roles
from models.models import ErrorResponseModel

class TestRolesAuth:
    @pytest.mark.parametrize("role, expected_status",
        LOGIN_VALID_BY_ROLE,
        LOGIN_VALID_BY_ROLE_IDS,
    )
    def test_login_with_valid_credentials_by_role(
        self,
        request: FixtureRequest,
        role: Roles,
        expected_status: int,
        registered_user: dict,
    ):
        """
        /auth/login с валидными данными.
        PUBLIC и USER, SUPER_ADMIN всем возращается токен.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])

        login_data = {
                "email": registered_user["email"],
                "password": registered_user["password"],
            }

        response = client.auth_api.login_user(login_data, expected_status=expected_status)
        data = response.json()

        assert "accessToken" in data
        assert isinstance(data["accessToken"], str)
        assert data["accessToken"]

    @pytest.mark.parametrize(
        "role, expected_status",
        LOGIN_INVALID_PASSWORD_BY_ROLE,
        LOGIN_INVALID_PASSWORD_BY_ROLE_IDS
    )
    def test_login_with_invalid_password_by_role(
        self,
        request: FixtureRequest,
        role: Roles,
        expected_status: int,
        registered_user: dict,
    ):
        """
        /auth/login с неверным паролем даёт 401 для любой роли вызвавшего клиента.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])

        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"] + "_wrong",
        }

        response = client.auth_api.login_user(
            login_data,
            expected_status=expected_status,
        )
        data = response.json()
        error_response = ErrorResponseModel(**data)
        assert "Unauthorized" in str(error_response.error)
        assert "accessToken" not in data

    @pytest.mark.parametrize(
        "role, expected_status",
        CREATE_USER_SUCCESS_BY_ROLE,
        ids=CREATE_USER_SUCCESS_BY_ROLE_IDS,
    )
    def test_superadmin_can_create_user(
        self,
        request: FixtureRequest,
        role: Roles,
        expected_status: int,
        admin_user_data: dict,
    ):
        """
        SUPER_ADMIN может создать пользователя через /users (201).
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])

        response = client.user_api.create_user_admin(
            admin_user_data,
            expected_status=expected_status,
        )
        data = response.json()

        assert data["email"] == admin_user_data["email"]
        assert "id" in data
        assert "roles" in data
        assert "USER" in data["roles"]

        client.user_api.clean_up_user(data["id"])

    @pytest.mark.parametrize(
        "role, expected_status",
        CREATE_USER_FORBIDDEN_BY_ROLE,
        ids=CREATE_USER_FORBIDDEN_BY_ROLE_IDS,
    )
    def test_non_superadmin_cannot_create_user(
        self,
        request: FixtureRequest,
        role: Roles,
        expected_status: int,
        admin_user_data: dict,
    ):
        """
        PUBLIC и USER не могут создавать пользователей (401/403).
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])

        response = client.user_api.create_user_admin(
            admin_user_data,
            expected_status=expected_status,
        )
        data = response.json()

        error_response = ErrorResponseModel(**data)
        assert (
            "Unauthorized" in str(error_response.error)
            or "Forbidden resource" in str(error_response.message)
        )