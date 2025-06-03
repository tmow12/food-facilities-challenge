import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from src.main import app
from src.api.routes.routes import get_data_service


@pytest.fixture
def mock_data_service():
    mock = MagicMock()
    app.dependency_overrides[get_data_service] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def client():
    return TestClient(app)


class TestPermitRoutes:
    def test_get_permits(self, client, mock_data_service):
        mock_data_service.get_permits.return_value = [
            {"Applicant": "Taco Truck", "Status": "Approved"},
            {"Applicant": "Coffee Cart", "Status": "Approved"},
            {"Applicant": "Burger Bus", "Status": "Requested"},
            {"Applicant": "Noodle Van", "Status": "Expired"},
            {"Applicant": "Taco Truck", "Status": "Expired"},
        ]
        response = client.get("/api/v1/permits")
        assert response.status_code == 200
        assert len(response.json()) == 5
        mock_data_service.get_permits.assert_called_once()

    def test_search_applicant_and_status_expired(self, client, mock_data_service):
        mock_data_service.get_permits.return_value = [
            {"Applicant": "Taco Truck", "Status": "Expired"}
        ]
        response = client.get("/api/v1/permits?applicant=taco&status=expired")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["Status"] == "Expired"
        mock_data_service.get_permits.assert_called_once()

    def test_search_partial_address(self, client, mock_data_service):
        mock_data_service.get_permits.return_value = [
            {"Applicant": "Coffee Cart", "Address": "123 Market St", "Status": "Approved"}
        ]
        response = client.get("/api/v1/permits?address=market")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "market" in data[0]["Address"].lower()

    def test_search_by_lat_and_long(self, client, mock_data_service):
        mock_data_service.get_permits.return_value = [
            {"Applicant": "Taco Truck", "Latitude": 37.77, "Longitude": -122.42, "Status": "Approved"},
            {"Applicant": "Coffee Cart", "Latitude": 37.76, "Longitude": -122.41, "Status": "Approved"},
        ]
        response = client.get("/api/v1/permits?latitude=37.7749&longitude=-122.4194")
        assert response.status_code == 200
        assert len(response.json()) == 2
        mock_data_service.get_permits.assert_called_once()
