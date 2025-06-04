
# Food Facilities Challenge

This app allows users to search for mobile food facilities and mobile food facility permits.
Users can search by vendor name, location, type of food sold, and permit status.

# Runbook 

to run frontend react app
1. cd frontend
2. npm install
3. npm start - The React app should now be running on http://localhost:3000


to run backend fastapi server
2. python --version
3. pyenv install 3.10.8
   pyenv local 3.10.8
4. curl -sSL https://install.python-poetry.org | python3 -
1. cd backend
5. poetry install
6. poetry shell
7. poetry run uvicorn src.main:app --reload (http://localhost:8000)


To run test
1. cd backend
2. poetry run pytest 


# Tech Stack
Frontend:
React
Javascript

Backend:
FastAPI
Python
uvicorn
pandas
pydantic
geopy
PyTest
Poetry

# API documention
http://localhost:8000/docs#/ 

# Requirement 
- As a user, I should be able to search food facility permits by applicant name. Even if type in a partial applicant name. 
- As a user, I should be able to search food facility permits by street name. Even if type in a partial address. 
- Given a valid latitude and longitude the user should be able search for the 5 nearest food trcks with status "Approved"
- The search results will always default to food facilities with status "Approved" unless it is explicity set by the user


# Design 
In this app 

# Critique
Improvements
 - build out the UI
 - API Authentication/Authorization
 - Pagination
 - Data santization
 - Expand search 
 - 

