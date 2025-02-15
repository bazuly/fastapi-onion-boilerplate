from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, status

from app.dependency import get_image_upload_service
from app.image_upload.schema import ImageResponse, ImageCreateBase
from app.image_upload.models import ImageUploadModel
from app.image_upload.service import ImageService

router = APIRouter(prefix="/image_upload", tags=["image_upload"])


@router.post(
    "/image_upload",
    response_model=ImageResponse,
)
async def upload_image(
        image_service: Annotated[ImageService, Depends(get_image_upload_service)],
        image: UploadFile = File(...),
) -> ImageResponse:
    return await image_service.upload_image(image)


@router.get(
    "/image_get/{image_id}",
    response_model=ImageCreateBase,
)
async def get_uploaded_image(
        image_id: int,
        image_service: Annotated[ImageService, Depends(get_image_upload_service)],
) -> ImageUploadModel:
    return await image_service.get_image_by_id(image_id)


@router.get(
    "/image_delete/{image_id}",
    response_model=None,
)
async def delete_uploaded_image(
        image_id: int,
        image_service: Annotated[ImageService, Depends(get_image_upload_service)],
) -> status.HTTP_204_NO_CONTENT:
    return await image_service.delete_image_by_id(image_id)
