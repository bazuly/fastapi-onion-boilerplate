from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.applications.schema import ApplicationCreateSchema, ApplicationSchema
from app.applications.service import ApplicationService
from app.dependency import get_application_service
from settings import DescriptionSettings

router = APIRouter(prefix="/applications", tags=["applications"])
settings = DescriptionSettings()


@router.post(
    "/applications",
    response_model=ApplicationSchema,
)
async def post_application(
        body: ApplicationCreateSchema,
        application_service: Annotated[ApplicationService, Depends(get_application_service)]

):
    return await application_service.create_application(body)


@router.get(
    "/applications/",
    response_model=List[ApplicationSchema],
)
async def get_all_applications(
        application_service: Annotated[ApplicationService, Depends(get_application_service)],
        page: int = Query(1, ge=1, description=settings.PAGE_DESCRIPTION),
        size: int = Query(10, ge=1, le=100, description=settings.SIZE_DESCRIPTION),
) -> List[ApplicationSchema]:
    return await application_service.get_all_applications(page=page, size=size)


@router.get(
    "/applications/{user_name}",
    response_model=ApplicationSchema | List[ApplicationSchema],
)
async def get_application_by_user_name(
        user_name: str,
        application_service: Annotated[ApplicationService, Depends(get_application_service)],
        page: int = Query(1, ge=1, description=settings.PAGE_DESCRIPTION),
        size: int = Query(10, ge=1, le=100, description=settings.SIZE_DESCRIPTION),

):
    return await application_service.get_application_by_user_name(
        user_name=user_name,
        page=page,
        size=size
    )
