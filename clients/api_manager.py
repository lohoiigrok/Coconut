from testsam.clients.new_api_client import AuthAPI
from testsam.clients.new_user_API import UserAPI
from testsam.clients.movie_api_client import MoviesApi

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия,
        используемая всеми API-классами
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesApi(self.session) # Добавляю MovieAPI