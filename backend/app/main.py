from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

# Initialize FastAPI application
app = FastAPI()

# Configure CORS middleware to allow cross-origin requests
origins = [
    "http://localhost",
    "http://localhost:3000",  # React frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

@app.get("/")
async def read_root():
    """
    Root endpoint to test the API.
    """
    return {"message": "Welcome to the Library Management System API"}

# Include other routes and dependencies here
# Example:
# from backend.app.api import library_routes
# app.include_router(library_routes, prefix="/api/library")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)