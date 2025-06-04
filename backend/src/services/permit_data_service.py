import logging
from typing import List
import pandas as pd
from geopy.distance import distance

from src.api.models.permit import Permit
from src.api.models.search_query import SearchQuery

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PermitDataService:

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the data service with mobile food facility permit data
        """
        self.df = df


    def get_permits(self, query: SearchQuery) -> List[Permit]:
        """
        Retrieve and filter mobile food facility permits.

        This method filters permits based on query parameters and returns a list
        of matching permits serialized using Pydantic models.

        Filtering options:
        - `applicant`: Case-insensitive partial match on the applicant name.
        - `status`: Case-insensitive exact match on permit status (defaults to "Approved").
        - `address`: Case-insensitive partial match on the facility address.
        - `latitude` and `longitude`: If both are provided, calculates geodesic
        distance (in kilometers) from the provided location to each food vendor, and returns the 5 closest food vendors.

        Notes:
        - If no `status` is provided, it defaults to filtering for "Approved".
        - Permits with invalid or missing coordinates are skipped from distance calculations.
        - Returns the data as a list of dictionaries using Pydantic aliases.        
        """
        df_filtered = self.df
        if query.applicant:
            df_filtered = df_filtered[df_filtered["Applicant"].str.contains(query.applicant, case=False, na=False)]

        if query.status:
            df_filtered = df_filtered[
                df_filtered["Status"].str.lower() == query.status.lower()
            ]

        else:
            df_filtered = df_filtered[
                df_filtered["Status"].str.lower() == "approved"
            ]

        if query.address:
            df_filtered = df_filtered[
                df_filtered["Address"].str.contains(query.address, case=False, na=False)
        ]
            
        if query.latitude is not None and query.longitude is not None:
            user_location = (query.latitude, query.longitude)

            def compute_distance(row):
                try:
                    truck_location = (float(row["Latitude"]), float(row["Longitude"]))
                    return distance(user_location, truck_location).km
                except (ValueError, TypeError) as e:
                    logger.warning(
                        f"Skipping row due to invalid coordinates: Latitude={row.get('Latitude')}, "
                        f"Longitude={row.get('Longitude')}. Error: {e}"
                    )
                    # Mark as invalid coordinates by returning inf
                    return float("inf") 

            #  Note df.apply(..., axis=1) is slow for large datasets since this is for-loop under the hood 
            #  For large data it could be better to use geopy.distance in batches
            df_filtered = df_filtered.copy()
            df_filtered["distance"] = df_filtered.apply(compute_distance, axis=1)
            # Drop rows where distance is inf (invalid coordinates)
            df_filtered = df_filtered[df_filtered["distance"] != float("inf")]
            df_filtered = df_filtered.sort_values("distance").head(5)
        # 1. Each row is converted to a dictionary 
        # 2. then unpacked into Permit model instances
        # 3. and then serializes back to a dictionary with aliases and sent as JSON by FastAPI
        return [
            Permit(**row).model_dump(by_alias=True)
            for row in df_filtered.to_dict(orient="records")
        ]
