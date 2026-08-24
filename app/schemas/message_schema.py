from pydantic import BaseModel


class MessageResponse(BaseModel):

    id: str

    sender_id: str

    username: str

    room_id: str

    message: str
    status: str

    created_at: str