import pytest
import pandas as pd
from src.services.permit_data_service import PermitDataService
from src.api.models.search_query import SearchQuery


@pytest.fixture
def sample_dataframe():
    # Sample DataFrame to mock loaded CSV
    data = {
        "Applicant": ["Tasty Truck", "Yummy Meals", "Tasty Truck", "Old Truck"],
        "Status": ["APPROVED", "EXPIRED", "APPROVED", "APPROVED"],
        "Address": ["123 Market St", "456 Castro St", "789 Mission St", "123 Market St"],
        "Latitude": [37.7749, 37.7749, None, 37.7810],
        "Longitude": [-122.4194, -122.4194, -122.4194, -122.4100]
    }
    return pd.DataFrame(data)


class TestPermitDataService:
    def test_loads_and_defaults_to_approved(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery()
        results = service.get_permits(query)

        assert len(results) == 3  # Only APPROVED
        assert all(r["Status"] == "APPROVED" for r in results)

    def test_filter_by_applicant(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery(applicant="Tasty")
        results = service.get_permits(query)

        assert len(results) == 2
        assert all("Tasty Truck" in r["Applicant"] for r in results)

    def test_filter_by_status(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery(status="expired")
        results = service.get_permits(query)

        assert len(results) == 1
        assert results[0]["Status"] == "EXPIRED"

    def test_filter_by_address(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery(address="Castro", status="EXPIRED")
        results = service.get_permits(query)

        assert len(results) == 1
        assert "Castro" in results[0]["Address"]

    def test_nearest_location_filtering(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery(latitude=37.7750, longitude=-122.4195)
        results = service.get_permits(query)

        assert len(results) <= 5
        assert all("Latitude" in r and "Longitude" in r for r in results)
        assert all(r["Status"] == "APPROVED" for r in results)

    def test_empty_results_when_no_match(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery(applicant="Nonexistent")
        results = service.get_permits(query)

        assert results == []

    def test_ignore_invalid_coordinates_for_distance(self, sample_dataframe):
        service = PermitDataService(sample_dataframe)
        query = SearchQuery(latitude=37.7749, longitude=-122.4194)
        results = service.get_permits(query)

        assert len(results) <= 5
        assert all(r["Latitude"] is not None and r["Longitude"] is not None for r in results)
