class MessageMapper:

    @staticmethod
    def to_response(message: dict):

        return {
            "id": str(message["_id"]),
            "sender_id": message["sender_id"],
            "username": message["username"],
            "room_id": message["room_id"],
            "message": message["message"],
            "created_at": message["created_at"].isoformat(),
        }