from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File

from app.app_config import current_user
from app.dependency import get_image_upload_service
from app.image_upload.models import ImageUploadModel
from app.image_upload.schemas import ImageCreateBase
from app.image_upload.service import ImageService
from app.users.auth.models import User

router = APIRouter(prefix="/image_upload", tags=["image_upload"])


@router.post(
    "/image_upload",
)
async def upload_image(
        image_service: Annotated[ImageService, Depends(get_image_upload_service)],
        image: UploadFile = File(...),
        user: User = Depends(current_user),

):
    await image_service.upload_image(image, user.id)
    return {"message": f"Image: {image.filename} added succesfully"}


@router.get(
    "/image_get/{image_id}",
    response_model=ImageCreateBase,
)
async def get_uploaded_image(
        image_id: int,
        image_service: Annotated[ImageService, Depends(get_image_upload_service)],
        user: User = Depends(current_user),
) -> ImageUploadModel:
    return await image_service.get_image_by_id(image_id)


@router.delete(
    "/image_delete/{image_id}",
    response_model=None,
)
async def delete_uploaded_image(
        image_id: int,
        image_service: Annotated[ImageService, Depends(get_image_upload_service)],
        user: User = Depends(current_user),
):
    return await image_service.delete_image_by_id(image_id, user.id)
