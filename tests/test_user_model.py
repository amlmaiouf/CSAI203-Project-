from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User


# test user creation 
def test_user_creation():
    user = User(
        user_id=1,
        name="Ahmed",
        email="ahmed@test.com",
        password="password123",
        role="Elderly",
        phone_number="01012345678",
        address="Cairo, Egypt"
    )
    assert user.user_id == 1
    assert user.name == "Ahmed"
    assert user.email == "ahmed@test.com"


# test if the user credentials if really admin 
def test_user_is_admin():
    user = User(1, "Admin User", "admin@test.com", "pass", "Admin", "123", "Cairo")
    assert user.is_admin() == True


# test if the user credentials if not admin
def test_user_is_not_admin():
    user = User(1, "Regular User", "user@test.com", "pass", "Elderly", "123", "Cairo")
    assert user.is_admin() == False


# test if user is an employee
def test_user_is_employee():
    user = User(1, "Staff Member", "emp@test.com", "pass", "Staff", "123", "Cairo")
    assert user.is_employee() == True


# test if user not an employee
def test_user_is_not_employee():
    user = User(1, "Regular", "user@test.com", "pass", "Elderly", "123", "Cairo")
    assert user.is_employee() == False


# test get user by id 
@patch("app.models.user.get_db_connection")
def test_get_user_by_id(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # create fake some row like object
    mock_row = MagicMock()
    mock_row.user_id = 1
    mock_row.name = "Test"
    mock_row.email = "test@test.com"
    mock_row.password = "pass"
    mock_row.role = "Elderly"
    mock_row.phone_number = "123"
    mock_row.address = "Cairo"
    mock_row.profile = None
    mock_row.created_at = None
    mock_row.updated_at = None

    mock_cursor.fetchone.return_value = mock_row
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    user = User.get_by_id(1)
    assert user is not None
    assert user.name == "Test"


# test get usr by id is not found  
@patch("app.models.user.get_db_connection")
def test_get_user_by_id_not_found(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    user = User.get_by_id(999)
    assert user is None