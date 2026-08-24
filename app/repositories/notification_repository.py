from app.database.database import database
from bson import ObjectId


notifications_collection = database["notifications"]


class NotificationRepository:

    @staticmethod
    async def create_notification(
        notification: dict,
    ):

        result = await notifications_collection.insert_one(
            notification
        )

        notification["_id"] = result.inserted_id

        return notification

    @staticmethod
    async def get_user_notifications(
        user_id: str,
        limit: int = 50,
    ):

        cursor = (
            notifications_collection
            .find(
                {
                    "receiver_id": user_id
                }
            )
            .sort(
                "created_at",
                -1
            )
            .limit(limit)
        )

        return await cursor.to_list(
            length=limit
        )

    @staticmethod
    async def get_unread_notifications(
        user_id: str,
    ):

        cursor = notifications_collection.find(
            {
                "receiver_id": user_id,
                "status": "unread",
            }
        )

        return await cursor.to_list(
            length=None
        )

    @staticmethod
    async def mark_as_read(
        notification_id: str,
    ):

        await notifications_collection.update_one(
            {
                "_id": ObjectId(notification_id)
            },
            {
                "$set": {
                    "status": "read"
                }
            },
        )

    @staticmethod
    async def mark_all_as_read(
        user_id: str,
    ):

        await notifications_collection.update_many(
            {
                "receiver_id": user_id,
                "status": "unread",
            },
            {
                "$set": {
                    "status": "read"
                },
            },
        )