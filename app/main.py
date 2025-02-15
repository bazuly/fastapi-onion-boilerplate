from fastapi import FastAPI

from app.applications.handlers import router as applications_router
from app.image_upload.handlers import router as image_upload_router

app = FastAPI()

app.include_router(applications_router)
app.include_router(image_upload_router)
