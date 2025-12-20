from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.service import Service


# service created? 
def test_service_creation():
    service = Service(
        service_id=1,
        service_name="Home Care",
        type="Medical",
        price=150.0,
        description="Daily home care service",
        is_available=True
    )
    assert service.service_id == 1
    assert service.service_name == "Home Care"
    assert service.price == 150.0


# service available?
def test_service_is_available():
    service = Service(1, "Care", "Medical", 100.0, "Desc", True)
    assert service.is_available == True


# service not available? 
def test_service_not_available():
    service = Service(1, "Care", "Medical", 100.0, "Desc", False)
    assert service.is_available == False


# test service type validation 
def test_service_type():
    service = Service(1, "Nursing Care", "Nursing", 200.0, "Physical therapy", True)
    assert service.type == "Nursing"


# mocking database                                 
@patch("app.models.service.get_db_connection")
def test_get_all_services(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # create fake some row like object
    mock_row1 = MagicMock()
    mock_row1.service_id = 1
    mock_row1.service_name = "Service 1"
    mock_row1.type = "Medical"
    mock_row1.price = 100.0
    mock_row1.description = "Desc 1"
    mock_row1.is_available = True
    mock_row1.created_at = None
    mock_row1.updated_at = None

    mock_row2 = MagicMock()
    mock_row2.service_id = 2
    mock_row2.service_name = "Service 2"
    mock_row2.type = "Nursing"
    mock_row2.price = 200.0
    mock_row2.description = "Desc 2"
    mock_row2.is_available = True
    mock_row2.created_at = None
    mock_row2.updated_at = None

    mock_cursor.fetchall.return_value = [mock_row1, mock_row2]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    services = Service.get_all()
    assert len(services) == 2
    assert services[0].service_name == "Service 1"


# get service by id                                
@patch("app.models.service.get_db_connection")
def test_get_service_by_id(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # create fake some row like object
    mock_row = MagicMock()
    mock_row.service_id = 1
    mock_row.service_name = "Home Care"
    mock_row.type = "Medical"
    mock_row.price = 150.0
    mock_row.description = "Daily care"
    mock_row.is_available = True
    mock_row.created_at = None
    mock_row.updated_at = None

    mock_cursor.fetchone.return_value = mock_row
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    service = Service.get_by_id(1)
    assert service is not None
    assert service.service_name == "Home Care"


# test service not found                                     
@patch("app.models.service.get_db_connection")
def test_get_service_not_found(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    service = Service.get_by_id(999)
    assert service is None