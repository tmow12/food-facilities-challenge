from typing import List
from fastapi import APIRouter, Depends, Request

from src.api.models.permit import Permit
from src.api.models.search_query import SearchQuery
from src.services.permit_data_service import PermitDataService

router = APIRouter(prefix="/api/v1", tags=["Permit Data API"])


def get_data_service(request: Request) -> PermitDataService:
    """
    Retrieve the initialized PermitDataService instance from the FastAPI app state.
    Ensures the service and data are loaded only once at app startup.
    """
    return request.app.state.permit_data_service


@router.get(
    "/permits",
    response_model=List[Permit],
    summary="Get San Francisco mobile food facility permits data",
    description="""
        Filter mobile food facility permits using optional query parameters.

        - `applicant`: Case-insensitive partial match.
        - `status`: Case-insensitive exact match (defaults to "Approved").
        - `address`: Case-insensitive partial match.
        - `latitude` + `longitude`: Return the 5 closest vendors.

        Invalid coordinates are skipped.
    """
)
async def get_permits(
    query: SearchQuery = Depends(),
    data_service: PermitDataService = Depends(get_data_service)
):
    return data_service.get_permits(query)
