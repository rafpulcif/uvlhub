import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"

def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page"

    logout(test_client)
    
# unit test for the create_notepad function
def test_create_notepad_post(test_client):
    """
    Tests the creation of a notepad via a POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.post("/notepad/create", data=dict(title="Test Title", body="Test Body"))
    assert response.status_code == 302, "The notepad could not be created."
    
    logout(test_client)


def test_get_notepad_get(test_client):
    """
    Tests access to a notepad via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.get("/notepad/1")
    assert response.status_code == 200, "The notepad could not be accessed."
    assert b"Test Title" in response.data, "The expected content is not present on the page"
    
    logout(test_client)
    
def test_get_notepad_not_found(test_client):
    """
    Tests access to a non-existent notepad via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.get("/notepad/999")
    assert response.status_code == 404, "The notepad was found."
    
    logout(test_client)
    
def test_edit_notepad(test_client):
    """
    Tests the editing of a notepad via a POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.post("/notepad/edit/1", data=dict(title="Test Title Edited", body="Test Body Edited"))
    assert response.status_code == 302, "The notepad could not be edited."
    
    logout(test_client)
    
def test_delete_notepad(test_client):
    """
    Tests the deletion of a notepad via a POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    response = test_client.post("/notepad/delete/1")
    assert response.status_code == 302, "The notepad could not be deleted."
    
    logout(test_client)