import pytest

@pytest.mark.dbcheck
def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")

    """
    Проверяем, что:
    1. До создания фильма нет в БД,
    2. После создания через API фильм появляется в БД.
    3. После удаления через API фильм исчезает из БД.
    """
@pytest.mark.dbcheck
def test_movie_created_and_deleted_in_db(
        authorized_admin,
        movie_data,
        db_helper
):
    movie_name = movie_data["name"]

    # 1. До теста фильма в БД быть не должно
    movie_before_create = db_helper.get_movie_by_name(movie_name)
    assert movie_before_create is None

    # 2. Создаем фильм через API
    create_response = authorized_admin.movies_api.create_movie(movie_data, expected_status=201)
    create_data = create_response.json()

    assert "id" in create_data
    movie_id = create_data["id"]

    # 3. Проверяем через API, что фильм создался
    get_response = authorized_admin.movies_api.get_single_movie(movie_id, expected_status=200)
    get_data = get_response.json()

    assert get_data["id"] == movie_id
    assert get_data["name"] == movie_name

    # 4. Проверяем, что фильм появился в БД
    movie_in_db = db_helper.get_movie_by_name(movie_name)

    assert movie_in_db is not None
    assert movie_in_db.name == movie_data["name"]
    assert movie_in_db.price == movie_data["price"]
    assert movie_in_db.published == movie_data["published"]
    # если id в БД и API одного типа, можно добавить:
    # assert movie_in_db.id == movie_id

    # 5. Удаляем фильм через API
    deleted_get_response = authorized_admin.movies_api.delete_movie(movie_id, expected_status=200)
    deleted_get_data = deleted_get_response.json()

    assert movie_in_db.name == movie_data["name"]
    assert movie_in_db.price == movie_data["price"]

    # 7. Проверяем, что из БД фильм тоже исчез
    movie_after_delete = db_helper.get_movie_by_name(movie_name)
    assert movie_after_delete is None