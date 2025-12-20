from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.feedback import Feedback


# test feedback creation
def test_feedback_creation():
    feedback = Feedback(
        feedback_id=1,
        user_id=1,
        service_id=1,
        rating=5,
        comment="Excellent service!"
    )
    assert feedback.feedback_id == 1
    assert feedback.rating == 5
    assert feedback.comment == "Excellent service!"


# test feedback rating is valid
def test_feedback_valid_rating():
    feedback = Feedback(1, 1, 1, None, None, 4, "Good")
    assert feedback.rating >= 1 and feedback.rating <= 5


# test feedback with minimum rate 
def test_feedback_min_rating():
    feedback = Feedback(1, 1, 1, None, None, 1, "Poor service")
    assert feedback.rating == 1


# test feedback with maximum rate
def test_feedback_max_rating():
    feedback = Feedback(1, 1, 1, None, None, 5, "Amazing!")
    assert feedback.rating == 5


# mock test for get feedback by service
@patch("app.models.feedback.get_db_connection")
def test_get_feedback_by_service(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # create fake data like what in the model 
    mock_row1 = MagicMock()
    mock_row1.feedback_id = 1
    mock_row1.user_id = 1
    mock_row1.service_id = 1
    mock_row1.order_id = None
    mock_row1.date = None
    mock_row1.rating = 5
    mock_row1.comment = "Great!"
    mock_row1.created_at = "2024-01-01"
    mock_row1.user_name = "User1"
    mock_row1.service_name = "Service1"

    mock_row2 = MagicMock()
    mock_row2.feedback_id = 2
    mock_row2.user_id = 2
    mock_row2.service_id = 1
    mock_row2.order_id = None
    mock_row2.date = None
    mock_row2.rating = 4
    mock_row2.comment = "Good"
    mock_row2.created_at = "2024-01-02"
    mock_row2.user_name = "User2"
    mock_row2.service_name = "Service1"

    mock_cursor.fetchall.return_value = [mock_row1, mock_row2]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    feedbacks = Feedback.get_filtered(service_id=1)
    assert len(feedbacks) == 2


# get feedback by user
@patch("app.models.feedback.get_db_connection")
def test_get_feedback_by_user(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # create fake some row like object
    mock_row = MagicMock()
    mock_row.feedback_id = 1
    mock_row.user_id = 1
    mock_row.service_id = 1
    mock_row.order_id = None
    mock_row.date = None
    mock_row.rating = 5
    mock_row.comment = "Excellent"
    mock_row.created_at = "2024-01-01"
    mock_row.user_name = "User1"
    mock_row.service_name = "Service1"

    mock_cursor.fetchall.return_value = [mock_row]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    feedbacks = Feedback.get_by_user_id(1)
    assert len(feedbacks) == 1
    assert feedbacks[0].rating == 5