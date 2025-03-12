from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.app_config import current_user
from app.applications.schemas import ApplicationCreateSchema, ApplicationSchema, ApplicationResponseSchema
from app.applications.service import ApplicationService
from app.dependency import get_application_service
from app.users.auth.models import User
from settings import DescriptionSettings

router = APIRouter(prefix="/applications", tags=["applications"])
settings = DescriptionSettings()


@router.post(
    "/applications",
    response_model=ApplicationResponseSchema,
)
async def post_application(
        body: ApplicationCreateSchema,
        application_service: Annotated[ApplicationService, Depends(get_application_service)],
        user: User = Depends(current_user),
) -> ApplicationResponseSchema:
    return await application_service.create_application(body, user.id)


@router.get(
    "/applications",
    response_model=List[ApplicationSchema],
)
async def get_all_applications(
        application_service: Annotated[ApplicationService, Depends(get_application_service)],
        page: int = Query(1, ge=1, description=settings.PAGE_DESCRIPTION),
        size: int = Query(10, ge=1, le=100, description=settings.SIZE_DESCRIPTION),
) -> List[ApplicationSchema]:
    return await application_service.get_all_applications(page=page, size=size)


@router.get(
    "/applications/by-title/{title}",
    response_model=List[ApplicationSchema],
)
async def get_application_by_title(
        title: str,
        application_service: Annotated[ApplicationService, Depends(get_application_service)],
) -> List[ApplicationSchema]:
    return await application_service.get_application_by_title(
        title=title
    )


@router.get(
    "/applications/{application_id}",
    response_model=ApplicationSchema,
)
async def get_application_by_id(
        application_id: int,
        application_service: Annotated[ApplicationService, Depends(get_application_service)],
) -> ApplicationSchema:
    return await application_service.get_application_by_id(application_id=application_id)


@router.patch(
    "/applications/{application_id}",
    response_model=ApplicationSchema,
)
async def patch_application(
        application_id: int,
        new_title: str | None = None,
        new_description: str | None = None,
        application_service: ApplicationService = Depends(get_application_service),
        user: User = Depends(current_user),
) -> ApplicationSchema:
    return await application_service.edit_application(
        application_id=application_id,
        user_id=user.id,
        new_title=new_title,
        new_description=new_description,
    )


@router.delete(
    "/applications/{application_id}",
    response_model=None,
    responses={
        200: {"description": "Successfully deleted"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"}
    }
)
async def delete_application(
        application_id: int,
        application_service: ApplicationService = Depends(get_application_service),
        user: User = Depends(current_user),
):
    return await application_service.delete_user_application(
        application_id=application_id,
        user_id=user.id
    )
