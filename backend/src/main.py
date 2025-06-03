from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.routes import router as routes

app = FastAPI()
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