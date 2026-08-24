from datetime import datetime, timezone


class MessageModel:

    @staticmethod
    def create(
        sender_id: str,
        username: str,
        room_id: str,
        message: str,
    ):

        return {
            "sender_id": sender_id,
            "username": username,
            "room_id": room_id,
            "message": message,

            "status": "sent",

            "created_at": datetime.now(timezone.utc),
        }