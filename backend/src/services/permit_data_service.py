from geopy.distance import distance
import pandas as pd
from typing import List
from src.api.models.permit import Permit
from src.api.models.search_query import SearchQuery
import logging

logger = logging.getLogger(__name__)

class PermitDataService:

    def __init__(self, csv_path: str = "src/data/Mobile_Food_Facility_Permit.csv"):
        """
        Initialize the data service with mobile food facility permit data.
        Loads the CSV once and replaces NaNs with None.
        """
        # loading the data from the CSV file everytime the service is initialized is not efficient,
        # but it is done here for simplicity. In a production environment, you might want to cache this data,
        # or load it once and keep it in memory, or use a database if the dataset is large and query the db
        self.df = self._load_data(csv_path)

    def _load_data(self, csv_path: str) -> pd.DataFrame:
        """
        Load and clean the permit data from a CSV file.
        Replaces NaN with None to be compatible with Pydantic models.
        Pydantic will intrept that as null when returning the API response
        """
        try:
            df = pd.read_csv(csv_path)
            return df.replace({float('nan'): None})
        except Exception as e:
            logger.error(f"Failed to load CSV at {csv_path}: {e}")
            raise

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
        distance (in kilometers) from the provided location to each food truck.
        Returns the 5 closest trucks.

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
                    # Convert latitude and longitude to float and calculate distance
                    truck_location = (float(row["Latitude"]), float(row["Longitude"]))
                    # Calculate the distance in kilometers
                    return distance(user_location, truck_location).km
                except (ValueError, TypeError) as e:
                    logger.warning(
                        f"Skipping row due to invalid coordinates: Latitude={row.get('Latitude')}, "
                        f"Longitude={row.get('Longitude')}. Error: {e}"
                    )
                    # Skip invalid rows
                    return float("inf") 

            #  Note df.apply(..., axis=1) is slow for large datasets since this is for-loop under the hood 
            #  For large data it could be better to use geopy.distance in batches
            df_filtered = df_filtered.copy()
            df_filtered["distance"] = df_filtered.apply(compute_distance, axis=1)
            df_filtered = df_filtered.sort_values("distance").head(5)
        # Each row is converted to a dictionary, and unpacked into Permit(**row)
        # return [Permit(**row) for row in df_filtered.to_dict(orient="records")]
        return [
            Permit(**row).model_dump(by_alias=True)
            for row in df_filtered.to_dict(orient="records")
        ]



