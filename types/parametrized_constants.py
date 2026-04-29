from roles import Roles

ROLE_TO_FIXTURE = {
    Roles.PUBLIC: "api_manager",
    Roles.USER: "authorized_user",
    Roles.SUPER_ADMIN: "authorized_admin",
}

CREATE_MOVIE_SUCCESS_BY_ROLE = [
    (Roles.SUPER_ADMIN, 201),
]

CREATE_MOVIE_SUCCESS_BY_ROLE_IDS = ["superadmin_can_create_movie"]

CREATE_MOVIE_FORBIDDEN_BY_ROLE = [
    (Roles.PUBLIC, 401),
    (Roles.USER, 403),
]

CREATE_MOVIE_FORBIDDEN_BY_ROLE_IDS = [
    "public_cannot_create_movie",
    "user_cannot_create_movie",
]

GET_MOVIES_LIST_BY_ROLE = [
    Roles.PUBLIC,
    Roles.USER,
    Roles.SUPER_ADMIN,
]

GET_MOVIES_LIST_BY_ROLE_IDS = [
    "public_can_get",
    "user_can_get",
    "superadmin_can_get"
]

DELETE_MOVIE_SUCCESS_BY_ROLE = [
    (Roles.SUPER_ADMIN, 200),
]

DELETE_MOVIE_SUCCESS_BY_ROLE_IDS = ["superadmin_can_delete_movie"]

DELETE_MOVIE_FORBIDDEN_BY_ROLE = [
    (Roles.PUBLIC, 401),
    (Roles.USER, 403),
]

DELETE_MOVIE_FORBIDDEN_BY_ROLE_IDS = [
    "public_cannot_delete_movie",
    "user_cannot_delete_movie",
]

LOGIN_VALID_BY_ROLE = [
    Roles.PUBLIC,
    Roles.USER,
    Roles.SUPER_ADMIN
]

LOGIN_VALID_BY_ROLE_IDS = [
    "public_can_login_as_registered_user",
    "user_can_login_as_self",
    "superadmin_can_login_as_admin",
]

LOGIN_INVALID_PASSWORD_BY_ROLE = [
    (Roles.PUBLIC, 401),
    (Roles.USER, 401),
    (Roles.SUPER_ADMIN, 401),
]

LOGIN_INVALID_PASSWORD_BY_ROLE_IDS = [
    "public_login_invalid_password",
    "user_login_invalid_password",
    "superadmin_login_invalid_password",
]

CREATE_USER_SUCCESS_BY_ROLE = [
    (Roles.SUPER_ADMIN, 201),
]

CREATE_USER_SUCCESS_BY_ROLE_IDS = [
    "superadmin_can_create_user",
]

CREATE_USER_FORBIDDEN_BY_ROLE = [
    (Roles.PUBLIC, 401),
    (Roles.USER, 403),
]

CREATE_USER_FORBIDDEN_BY_ROLE_IDS = [
    "public_cannot_create_user",
    "user_cannot_create_user",
]

