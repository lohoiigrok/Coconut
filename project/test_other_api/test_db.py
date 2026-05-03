import pytest
import pytest_check as check

@pytest.mark.dbcheck
def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")

@pytest.mark.dbcheck
def test_movie_created_and_deleted_in_db(
        authorized_admin,
        movie_data,
        db_helper
):
    movie_name = movie_data["name"]

    assert db_helper.get_movie_by_name(movie_name) is None

    create_response = authorized_admin.movies_api.create_movie(movie_data, expected_status=201)
    create_data = create_response.json()

    assert "id" in create_data
    movie_id = create_data["id"]

    movie_in_db = db_helper.get_movie_by_name(movie_name)

    assert movie_in_db is not None
    check.equal(movie_in_db.name, create_data["name"])
    check.equal(movie_in_db.price, create_data["price"])
    check.equal(movie_in_db.description, create_data["description"])
    check.equal(movie_in_db.image_url, create_data["imageUrl"])
    check.equal(movie_in_db.location, create_data["location"])
    check.equal(movie_in_db.published, create_data["published"])
    check.equal(movie_in_db.rating, create_data["rating"])
    check.equal(movie_in_db.genre_id, create_data["genreId"])

    authorized_admin.movies_api.delete_movie(movie_id, expected_status=200)

    assert db_helper.get_movie_by_name(movie_name) is None