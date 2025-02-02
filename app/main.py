from fastapi import FastAPI

from app.applications.handlers import router as applications_router

app = FastAPI()

app.include_router(applications_router)
