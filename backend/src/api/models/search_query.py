from typing import Optional
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    """
    Represents a search query for mobile food facilities in San Francisco.
    """
    applicant: Optional[str] = Field(default=None, description="Name or partial name of the applicant")
    address: Optional[str] = Field(default=None, description="Address name or partial address name")
    status: Optional[str] = Field(default=None, description="Status filter (e.g., APPROVED, EXPIRED)")
    latitude: Optional[float] = Field(default=None, description="Latitude coordinate")
    longitude: Optional[float] = Field(default=None, description="Longitude coordinate")
