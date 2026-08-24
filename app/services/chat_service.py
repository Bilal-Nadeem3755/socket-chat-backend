from app.repositories.message_repository import MessageRepository
from app.mappers.message_mapper import MessageMapper


class ChatService:

    @staticmethod
    async def send_message(
        sender_id: str,
        room_id: str,
        message: str,
    ):

        created_message = await MessageRepository.create_message(
            sender_id=sender_id, # type: ignore
            room_id=room_id, # type: ignore
            message=message,
        )

        return MessageMapper.to_response(
            created_message
        )

    @staticmethod
    async def get_room_messages(
        room_id: str,
    ):

        messages = await MessageRepository.get_room_messages(
            room_id
        )

        return [
            MessageMapper.to_response(message)
            for message in messages
        ]