from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"

    # Group Created Unit Test:
def test_delete_order(db_session, mocker):
    # Sample order ID to delete
    order_id = 1

    # Mock the Order object and database to return an order
    mock_order = model.Order(order_id=order_id, customer_name="Jane Doe", description="Sample order")
    mock_query = mocker.Mock()
    mock_query.filter.return_value.first.return_value = mock_order
    mocker.patch.object(db_session, "query", return_value=mock_query)

    # Mock the delete and commit methods
    mock_delete = mocker.patch.object(db_session, "delete", autospec=True)
    mock_commit = mocker.patch.object(db_session, "commit", autospec=True)

    # Call the delete function
    response = controller.delete(db_session, order_id)

    # Assertions 
    assert response.status_code == 204  # No content status code
    mock_query.filter.assert_called_once_with(model.Order.order_id == order_id)
    mock_delete.assert_called_once_with(mock_order)
    mock_commit.assert_called_once()
