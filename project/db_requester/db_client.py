from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.resources.db_creds import MovieDbCreds

USERNAME = MovieDbCreds.USERNAME
PASSWORD = MovieDbCreds.PASSWORD
HOST = MovieDbCreds.HOST
PORT = MovieDbCreds.PORT
DATABASE_NAME = MovieDbCreds.DATABASE_NAME

# Движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False # Установить True для отладки SQL запросов
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()