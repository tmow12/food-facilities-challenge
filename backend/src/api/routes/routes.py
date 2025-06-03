from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import List
from src.api.models.permit import Permit
from src.api.models.search_query import SearchQuery
from src.services.permit_data_service import PermitDataService

# todo fix route name to @tmow
router = APIRouter(prefix="/api/v1", tags=["Permit Data API"])

@lru_cache()
def get_data_service():
    """
    Returns the PermitDataService instance.
    This function is used to ensure that the data service is initialized only once.
    """
    return PermitDataService()

@router.get("/permits", response_model=List[Permit])
async def get_all_permits(
    data_service: PermitDataService = Depends(get_data_service),
    query: SearchQuery = Depends()
):
    return data_service.get_all_permits(query)
