
# Food Facilities Challenge

This app allows users to search for mobile food facilities and mobile food facility permits.
Users can search by vendor name, location, type of food sold, and permit status.

# Runbook 

To run frontend react app
1. `cd frontend`
2. `npm install`
3. `npm start` 
4. The React app should now be running on http://localhost:3000


To run backend server
1. `curl -sSL https://install.python-poetry.org | python3 -` Install poetry globally 
2. `cd backend`
3. `poetry install` Installs backend dependencies and starts virutal env to run python project
4. `poetry run uvicorn src.main:app --reload` 
5. This will start the uvicorn server at http://localhost:8000 with hot reloading

To run tests
1. `cd backend`
2. `poetry run pytest `


# Tech Stack

Frontend:
- React
- Javascript

Backend:
- FastAPI
- Python
- Uvicorn
- Pandas
- Pydantic
- Geopy
- PyTest
- Poetry

# API documention

http://localhost:8000/docs#/ 


# Problem

The problem is to build a backend service which will allow the user to seach mobilie food facilities permit data in San Francisco. This data is given in the format of a small .csv file. 

Requirements for MVP
1. As a user, I should be able to search food facility permits by applicant name. Even if type in a partial applicant name. 
2. As a user, I should be able to search food facility permits by street name. Even if type in a partial address. 
3. Given a valid latitude and longitude the user should be able search for the 5 nearest food trcks with status "Approved"
4. The search results will always default to food facilities with status "Approved" unless it is explicity set by the user

Bonus: Having a UI

# Solution

The solution is to build a simple backend service with FastAPI that with a REST API (GET) to support this search functionality. I also created simple UI in React to allow the user to interact with this backend service.

# Design/Implementation 

Frontend: 
This will be a simple frontend with 5 input fields "Applicant name, Status, Address, Longtitude, and Latitude", and a "Search" button that allow the user to make the GET request to backend. Results will be displayed in a table, containing the Applicant name, Address, and Status. These are the only displayed supported for now. Note: the "Search" buttom is disabled until the the user enters a valid input

Backend:
Before the app is started we leverage the @asynccontextmanager decorator which allows to run some logic before the FastAPI server starts. Here it will load the csv file as Pandas DataFrame and create an instance of the PermitDataService and store it in app.state. Making the DataService and DataFrame accesible through out the app and avoiding having to reload/re-parse the csv file on every request. Since the data will be stored in memory, this solution is only suitable for smaller datasets. However there are some limitations to consider with this design, but these issues will be considered out of scope for the MVP of this project

1. Not scalable if the dataset grows
2. If we expect the data to be updated frequently, and need to use the freshest data, any update would require a full app reload
3. RAM limitation

I then define a a GET API endpoint a "/api/v1/permits" which allows the user to search for search for mobile food facility permits using optional query parameters "applicant name, status, address, longtitude, and latitude". These parameters are passed from frontend, I create a "SearchQuery" pydantic model to define and validate these paramters. The route also utlizes dependency injection to access the PermitDataService that was added to the app.data during start up. This ensure that the service is only initalized once, used for every request.

The DataPermitService contains all the main search logic for filtering and returning mobile food facility permit data. 
Filtering options:
        - `applicant`: Case-insensitive partial match on the applicant name.
        - `status`: Case-insensitive exact match on permit status (defaults to "Approved").
        - `address`: Case-insensitive partial match on the facility address.
        - `latitude` and `longitude`: If both values are provided, calculates geodesic
        distance (in kilometers) from the provided location to each food vendor, and returns the 5 closest food vendors.


Given the assumption that is a simple app, with a small csv file dataset this design/implementation is sufficient

Flow:
User -> React FE -> Rest API (GET) -> PermitDataService -> Data


# Critique

### What would you have done differently with more time?
- Implement a database instead of using csv file
- Completed a data sanitization before interacting with data
- Have a more efficient implementation for calculating the closest food vendors
- Create a better UI, would be nice to use TypeScript instead of JavaScript
- Made "Status" input field a drop down, because there are only a few options to choose from
(ex: approved, pending, requested, suspended, expired) and would create a better user experience 
- Made it clear in UI that if "Status" is not explicitly set, then the search will by default only return results with "Approved" status
- Write tests for frontend react app

### What are the trade-offs you might have made?
- **CSV vs Database**: 
  Using the csv was easier to reach MVP but this doesn't scale. A database supports larger datasets, optimized queries, and better persistence.  
  The `PermitDataService` could be refactored to query a database instead of reading from memory. This would take more effort and time, but would be a better and scalable design if the app and dataset size were to grow. A SQL or NoSQL database could work here, but there aoms pros and cons with each

  **SQL Pros:**
  - Structured, efficient, and validated data
  - Joins and complex filters
  - Strong geospatial support (PostGIS)

  **SQL Cons:**
  - Requires schema design and setup

  **NoSQL Pros:**
  - Flexible schema
  - Fast, horizontally scalable
  - Easier to store nested documents

  **NoSQL Cons:**
  - Weaker query features
  - No joins
  - Harder to enforce data integrity

- **Data Formatting**:
  Completed a data sanitization before hand, the current csv file headers are not uniformed, when validating the data with the Pydantic model, I am returning the JSON fields with those headers as is to frontend. If frontend was expecting a uniform format, that could cause confusion/errors. It is also best practice to be consistient with field names in general.   

- **Distance Calculation**:
  Have a more scalable and efficient implementation for calculating the distance. The current implemntation is leverages .apply() which under the hood is a for loop that goes over each record in the dataset, converts the lat/long to floats and calculates the geodesic distance from user's passed in cooridnates, then stores the result in a new "distance" column, sorts it, and takes the 5 closest. This is inefficient, because as the dataset grows, this operation will become slower. A possible solution I was reading into was using a haversine formula and NumPy to calculate all the distances at once, which under hood runs compiled c code. A girst flance, this would be much faster, and more performant even if the dataset grew in size. But it also seems slightly trickier to implement and would need more time to research


### What are the things you left out?
 - API Authentication/Authorization
 - Throttling
 - Pagination
 - Data santization
 - Hook up a database instead of reading from CSV file 
 - Allow user to search by other columns
 - Increased logging, error handling, and error monitoring 
 - Building out the UI
 - Create a docker file 
