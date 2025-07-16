from datetime import datetime
from typing import Optional
from uuid import UUID
import logging

from motor.motor_asyncio import AsyncIOMotorCollection

from app.mongo.schemas import UserLog
from app.exceptions import UserLogException

logger = logging.getLogger(__name__)


class UserLogService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
        self.logger = logger

    async def log_endpoint_call(self, endpoint: str, user_id: Optional[UUID]) -> None:
        try:
            log_data = UserLog(timestamp=datetime.utcnow(),
                               endpoint=endpoint, user_id=user_id)
            await self.collection.insert_one(log_data.dict())
            logger.info("data added successfully")
        except UserLogException as e:
            # we are not raise exception right here,
            # because we do not want to destroy our crud operation, if logs failed
            self.logger.error(
                "Error while recording log data: {}".format(e),
            )
