from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import List
from src.api.models.permit import Permit
from src.api.models.search_query import SearchQuery
from src.services.permit_data_service import PermitDataService

router = APIRouter(prefix="/api/v1", tags=["Permit Data API"])

@lru_cache(maxsize=1)
def get_data_service() -> PermitDataService:
    """
    Returns the PermitDataService instance.
    This function is used to ensure that the data service is initialized only once
    """
    return PermitDataService()

@router.get(
    "/permits",
    response_model=List[Permit],
    summary="Search permits",
    description="""
Filter mobile food facility permits using optional query parameters.

- `applicant`: Case-insensitive partial match.
- `status`: Case-insensitive exact match (defaults to "Approved").
- `address`: Case-insensitive partial match.
- `latitude` + `longitude`: Return the 5 closest trucks.

Invalid coordinates are skipped.
"""
)
async def get_permits(
    query: SearchQuery = Depends(),
    data_service: PermitDataService = Depends(get_data_service)
):
    return data_service.get_permits(query)
