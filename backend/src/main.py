from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pandas as pd
import logging

from src.services.permit_data_service import PermitDataService
from src.api.routes.routes import router as routes

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        path = "src/data/Mobile_Food_Facility_Permit.csv"
        df = pd.read_csv(path)
        df = df.replace({float("nan"): None})
        logger.info("dataframe is loaded once on app startup")
        app.state.permit_data_service = PermitDataService(df)
    except Exception as e:
        logger.error(f"Failed to load CSV at {path}: {e}")
        raise
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)   