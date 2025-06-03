from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class Permit(BaseModel):
    """
    Represents a mobile food facility permit in San Francisco
    """
    location_id: Optional[int] = Field(None, alias="locationid", description="Location id of facility")
    applicant: Optional[str] = Field(None, alias="Applicant", description="Name of permit holder")
    facility_type: Optional[str] = Field(None, alias="FacilityType", description="Type of facility permitted: truck or push cart")
    cnn: Optional[int] = Field(None, alias="cnn", description="CNN of street segment or intersection location")
    location_description: Optional[str] = Field(None, alias="LocationDescription", description="Description of street segment or intersection location")
    address: Optional[str] = Field(None, alias="Address", description="Address")
    blocklot: Optional[str] = Field(None, alias="blocklot", description="Block lot (parcel) number")
    block: Optional[str] = Field(None, alias="block", description="Block number")
    lot: Optional[str] = Field(None, alias="lot", description="Lot number")
    permit: Optional[str] = Field(None, alias="permit", description="Permit number")
    status: Optional[str] = Field(None, alias="Status", description="Status of permit: Approved or Requested")
    food_items: Optional[str] = Field(None, alias="FoodItems", description="A description of food items sold")
    x: Optional[float] = Field(None, alias="X", description="CA State Plane III")
    y: Optional[float] = Field(None, alias="Y", description="CA State Plane III")
    latitude: Optional[float] = Field(None, alias="Latitude", description="WGS84, latitude")
    longitude: Optional[float] = Field(None, alias="Longitude", description="WGS84, longitude")
    schedule: Optional[str] = Field(None, alias="Schedule", description="URL link to Schedule for facility")
    days_hours: Optional[str] = Field(None, alias="dayshours", description="abbreviated text of schedule")
    noi_sent: Optional[datetime] = Field(None, alias="NOISent", description="Date notice of intent sent")
    approved: Optional[str] = Field(None, alias="Approved", description="Date permit approved by DPW")
    received: Optional[int] = Field(None, alias="Received", description="Date permit application received from applicant")
    prior_permit: Optional[int] = Field(None, alias="PriorPermit", description="Prior existing permit with SFFD")
    expiration_date: Optional[str] = Field(None, alias="ExpirationDate", description="Date permit expires")
    location: Optional[str] = Field(None, alias="Location", description="Location formatted for mapping")
    fire_prevention_districts: Optional[int] = Field(None, alias="Fire Prevention Districts", description="Fire Prevention Districts")
    police_districts: Optional[int] = Field(None, alias="Police Districts", description="Police Districts")
    supervisor_districts: Optional[int] = Field(None, alias="Supervisor Districts", description="Supervisor Districts")
    zip_codes: Optional[int] = Field(None, alias="Zip Codes", description="Zip Codes")
    neighborhoods_old: Optional[int] = Field(None, alias="Neighborhoods (old)", description="Neighborhoods (old)")


    @field_validator("noi_sent", mode="before")
    def parse_noi_sent(cls, value):
        """
        Custom validator for the NOISent field to parse the date string into a datetime object.
        Since the date format (MM/DD/YYYY hh:mm:ss AM/PM) isn't natively supported by datetime.fromisoformat() or pydantic's auto-parser
        If the date format is not valid, it raises a ValueError with a descriptive message
        """ 
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
            except ValueError:
                raise ValueError(f"Invalid date format for NOISent: {value}")
        return value
    

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        # This tells Pydantic to ignore any extra fields passed into the model that are not explicitly defined
        extra = 'ignore'   
        # No additional code is needed here. The industry standard way to convert snake_case to camelCase for Pydantic models is to use an alias_generator function (like to_camel) in the Config class, as you have done above. This approach is widely used and recommended in the Pydantic documentation.
