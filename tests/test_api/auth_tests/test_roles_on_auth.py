import pytest
from _pytest.fixtures import FixtureRequest

from roles import Roles
from models.models import ErrorResponseModel


ROLE_TO_FIXTURE = {
    Roles.PUBLIC: "api_manager",
    Roles.USER: "authorized_user",
    Roles.SUPER_ADMIN: "authorized_admin",
}


class TestRolesAuth:

    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Roles.PUBLIC, 200),
            (Roles.USER, 200),
            (Roles.SUPER_ADMIN, 200),
        ],
        ids=[
            "public_can_login_as_registered_user",
            "user_can_login_as_self",
            "superadmin_can_login_as_admin",
        ],
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
        [
            (Roles.PUBLIC, 401),
            (Roles.USER, 401),
            (Roles.SUPER_ADMIN, 401),
        ],
        ids=[
            "public_login_invalid_password",
            "user_login_invalid_password",
            "superadmin_login_invalid_password",
        ],
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
        [
            (Roles.PUBLIC, 401),
            (Roles.USER, 403),
            (Roles.SUPER_ADMIN, 201),
        ],
        ids=[
            "public_cannot_create_user",
            "user_cannot_create_user",
            "superadmin_can_create_user",
        ],
    )
    def test_create_user_by_role(
        self,
        request: FixtureRequest,
        role: Roles,
        expected_status: int,
        admin_user_data: dict,
    ):
        """
        Создание пользователя через /users:
        только SUPER_ADMIN имеет право создавать пользователей.
        PUBLIC и USER получают 403.
        """
        client = request.getfixturevalue(ROLE_TO_FIXTURE[role])

        response = client.user_api.create_user_admin(
            admin_user_data,
            expected_status=expected_status,
        )
        data = response.json()

        if expected_status == 201:
            assert data["email"] == admin_user_data["email"]
            assert "id" in data
            assert "roles" in data
            assert "USER" in data["roles"]

            client.user_api.clean_up_user(data["id"])
        else:
            error_response = ErrorResponseModel(**data)
            assert "Unauthorized" in str(error_response.error) or "Forbidden resource" in str(error_response.message)