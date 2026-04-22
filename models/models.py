from pydantic import BaseModel
from typing import Optional

class GenreModel(BaseModel):
    name: str

class MovieResponseModel(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    rating: int
    genreId: int
    createdAt: str
    reviews: Optional[list] = None
    genre: GenreModel

class MovieListResponseModel(BaseModel):
    movies: list[MovieResponseModel]
    count: int
    page: int
    pageSize: int
    pageCount: int

class ErrorResponseModel(BaseModel):
    statusCode: int
    message: str | list[str] | None = None
    error: Optional[str] = None

class UserResponseModel(BaseModel):
    id: int
    statusCode: int
    email: str
    roles: list[str] | str | None