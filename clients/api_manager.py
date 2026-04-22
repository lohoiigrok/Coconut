from requests import Session
from clients.auth_api_client import AuthApi
from clients.user_api_client import UserApi
from clients.movie_api_client import MoviesApi

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.auth_api: AuthApi = AuthApi(session)
        self.user_api: UserApi = UserApi(session)
        self.movies_api: MoviesApi = MoviesApi(session)

    def clear_auth(self) -> None:
        self.session.headers.pop("Authorization", None)