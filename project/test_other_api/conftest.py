from sqlalchemy.orm import Session
from project.db_requester.db_client import get_db_session
from project.db_requester.db_helpers import DBHelper
from utils.data_generator import DataGenerator
from types.common_types import MovieData
import pytest

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию
    для работы с базой данных.
    После завершения теста сессия автоматически закрывается.
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture
def movie_data() -> MovieData:
    """ Валидные данные для создания фильма """
    return DataGenerator.movie_data()