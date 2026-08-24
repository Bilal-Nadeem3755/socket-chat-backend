from app.database.database import database
from bson import ObjectId


messages_collection = database["messages"]


class MessageRepository:

    @staticmethod
    async def create_message(message: dict):

        result = await messages_collection.insert_one(message)

        message["_id"] = result.inserted_id

        return message


    @staticmethod
    async def get_room_messages(
        room_id: str,
        limit: int = 50,
    ):

        cursor = (
            messages_collection
            .find(
                {
                    "room_id": room_id
                }
            )
            .sort(
                "created_at",
                -1
            )
            .limit(limit)
        )

        messages = await cursor.to_list(
            length=limit
        )

        messages.reverse()

        return messages


    # ==========================================
    # Mark Message As Delivered
    # ==========================================

    @staticmethod
    async def mark_as_delivered(
        message_id: str,
    ):

        try:

            object_id = ObjectId(message_id)

        except Exception:

            return False


        result = await messages_collection.update_one(
            {
                "_id": object_id,

                # Don't change an already-read
                # message back to delivered.
                "status": {
                    "$ne": "read"
                },
            },
            {
                "$set": {
                    "status": "delivered"
                }
            },
        )

        return result.modified_count > 0


    # ==========================================
    # Mark Message As Read
    # ==========================================

    @staticmethod
    async def mark_as_read(
        message_id: str,
        room_id: str,
        user_id: str,
    ):

        try:

            object_id = ObjectId(message_id)

        except Exception:

            return False


        # ------------------------------------------
        # Only the RECEIVER can mark the message
        # as read.
        #
        # sender_id != current user
        #
        # room_id must match current room
        # ------------------------------------------

        result = await messages_collection.update_one(
            {
                "_id": object_id,

                "room_id": room_id,

                "sender_id": {
                    "$ne": user_id
                },

                "status": {
                    "$ne": "read"
                },
            },
            {
                "$set": {
                    "status": "read"
                }
            },
        )

        return result.modified_count > 0


    # ==========================================
    # Get Unread Messages
    # ==========================================

    @staticmethod
    async def get_unread_messages(
        room_id: str,
        user_id: str,
    ):

        cursor = messages_collection.find(
            {
                "room_id": room_id,

                "sender_id": {
                    "$ne": user_id
                },

                "status": {
                    "$ne": "read"
                },
            }
        )

        return await cursor.to_list(
            length=None
        )