from datetime import datetime, timezone


class NotificationModel:

    @staticmethod
    def create(
        receiver_id: str,
        sender_id: str,
        sender_username: str,
        message_id: str,
        room_id: str,
        message: str,
    ):

        return {
            "receiver_id": receiver_id,
            "sender_id": sender_id,
            "sender_username": sender_username,
            "message_id": message_id,
            "room_id": room_id,
            "message": message,

            "status": "unread",

            "created_at": datetime.now(timezone.utc),
        }