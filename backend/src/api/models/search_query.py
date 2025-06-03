from typing import Optional
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    """
    Represents a search query for mobile food facilities in San Francisco.
    """
    applicant: Optional[str] = Field(None, description="Name or partial name of the applicant")
    address: Optional[str] = Field(None, description="Address name or partial address name")
    status: Optional[str] = Field(None, description="Status filter (e.g., APPROVED, EXPIRED)")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
