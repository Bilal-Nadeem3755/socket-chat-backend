from fastapi import APIRouter

from app.repositories.message_repository import (
    MessageRepository,
)

from app.mappers.message_mapper import (
    MessageMapper,
)

from app.schemas.message_schema import (
    MessageResponse,
)


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get(
    "/{room_id}",
    response_model=list[MessageResponse],
)
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