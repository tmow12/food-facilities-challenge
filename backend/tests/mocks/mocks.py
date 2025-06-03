from typing import List
from src.api.models.permit import Permit
from src.api.models.search_query import SearchQuery

def filter_permits(data: List[Permit], query: SearchQuery) -> List[dict]:
    filtered = []
    for p in data:
        if query.applicant and query.applicant.lower() not in p.applicant.lower():
            continue
        if query.status and query.status.lower() != p.status.lower():
            continue
        if query.address and query.address.lower() not in p.address.lower():
            continue
        filtered.append(p.model_dump(by_alias=True))
    return filtered

class MockPermitDataService:
    def get_permits(self, query: SearchQuery) -> List[Permit]:
        data = [
            Permit(
                location_id=123,
                applicant="Taco Truck",
                address="123 Market St",
                permit="XYZ123",
                status="Approved",
                latitude=37.77,
                longitude=-122.42
            ),
            Permit(
                location_id=456,
                applicant="Burger Bus",
                address="456 Mission St",
                permit="ABC789",
                status="Requested",
                latitude=37.78,
                longitude=-122.43
            ),
            Permit(
                location_id=789,
                applicant="Coffee Cart",
                address="789 Howard St",
                permit="CFE456",
                status="Approved",
                latitude=37.76,
                longitude=-122.41
            ),
            Permit(
                location_id=101,
                applicant="Noodle Van",
                address="101 King St",
                permit="NDL101",
                status="Expired",
                latitude=37.75,
                longitude=-122.40
            ),
            Permit(
                location_id=202,
                applicant="Taco Truck",
                address="202 Castro St",
                permit="TCO202",
                status="Expired",
                latitude=37.79,
                longitude=-122.39
            )
        ]
        return filter_permits(data, query)
