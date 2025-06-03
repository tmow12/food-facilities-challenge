
from fastapi.testclient import TestClient
from src.main import app
from src.tests.mocks.mocks import MockPermitDataService
from src.api.routes.routes import get_data_service

class TestPermitRoutes:
    @classmethod
    def setup_class(cls):
        app.dependency_overrides[get_data_service] = lambda: MockPermitDataService()
        cls.client = TestClient(app)

    @classmethod
    def teardown_class(cls):
        app.dependency_overrides = {}

    def test_get_permits(self):
        response = self.client.get("/api/v1/permits")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_search_applicant_and_status_expired(self):
        response = self.client.get("/api/v1/permits?applicant=taco&status=expired")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["Status"] == "Expired"

    def test_search_partial_address(self):
        response = self.client.get("/api/v1/permits?address=market")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_search_by_lat_and_long(self):
        response = self.client.get("/api/v1/permits?latitude=37.7749&longitude=-122.4194")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5