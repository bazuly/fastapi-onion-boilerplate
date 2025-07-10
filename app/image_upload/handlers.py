"""
    This FastAPI router defines endpoints for uploading, getting, and deleting images with user
    authentication and dependency injection.
    
    :param image_service: The `image_service` parameter in the FastAPI endpoints is an instance of the
    `ImageService` class, which is obtained using the `Depends(get_image_upload_service)` dependency.
    This dependency is responsible for providing the `ImageService` instance to the endpoint functions
    :type image_service: Annotated[ImageService, Depends(get_image_upload_service)]
    :param image: The `image` parameter in the `upload_image` function is of type `UploadFile` and is
    used to receive the uploaded image file from the client. This parameter is required (`...` indicates
    required) and is used to pass the image file to the `upload_image` function for processing and
    :type image: UploadFile
    :param user: The `user` parameter in the functions `upload_image`, `get_uploaded_image`, and
    `delete_uploaded_image` is of type `User`. It is obtained using the `current_user` dependency, which
    likely retrieves the current authenticated user making the request. This user object is then used in
    the functions
    :type user: User
    :return: The code provided defines an API router with endpoints for uploading, getting, and deleting
    images.
"""

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
    return await image_service.upload_image(image, user.id)


@router.get(
    "/image_get/{image_id}",
    response_model=ImageCreateBase,
)
async def get_uploaded_image(
    image_id: int,
    image_service: Annotated[ImageService, Depends(get_image_upload_service)],
    user: User = Depends(current_user),
) -> ImageUploadModel | None:
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
