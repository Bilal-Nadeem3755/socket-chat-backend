from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.repositories.user_repository import UserRepository
from app.models.message_model import MessageModel
from app.repositories.message_repository import MessageRepository
from app.websocket.connection_manager import ConnectionManager
from app.core.security import verify_access_token


router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
):

    # ==========================================
    # Get Token
    # ==========================================

    token = websocket.query_params.get(
        "token"
    )


    if not token:

        await websocket.close(
            code=1008
        )

        return


    # ==========================================
    # Verify JWT
    # ==========================================

    try:

        payload = verify_access_token(
            token
        )

    except Exception:

        await websocket.close(
            code=1008
        )

        return


    # ==========================================
    # Get User Identity
    # ==========================================

    user_id = payload.get(
        "user_id"
    )

    username = payload.get(
        "username"
    )


    if not user_id or not username:

        await websocket.close(
            code=1008
        )

        return


    # ==========================================
    # Connect User
    # ==========================================

    await manager.connect(
        websocket,
        room_id,
    )


    # Attach user information BEFORE
    # sending presence information.

    websocket.user_id = user_id  # type: ignore
    websocket.username = username  # type: ignore
    websocket.room_id = room_id  # type: ignore


    # ==========================================
    # Get Existing Online Users
    # ==========================================

    existing_users = manager.get_room_users(
        room_id,
        exclude_websocket=websocket,
    )


    # ==========================================
    # Send Existing Users To Newly Connected User
    # ==========================================

    for existing_user in existing_users:

        await manager.send_personal_message(
            {
                "type": "user_online",

                "user_id":
                    existing_user[
                        "user_id"
                    ],

                "username":
                    existing_user[
                        "username"
                    ],
            },
            websocket,
        )


    # ==========================================
    # Update Database Online Status
    # ==========================================

    await UserRepository.update_online_status(
        user_id,
        True,
    )


    # ==========================================
    # Notify Everyone About New User
    # ==========================================

    await manager.broadcast(
        room_id,
        {
            "type": "user_online",

            "user_id":
                user_id,

            "username":
                username,
        },
    )


    print(
        f"🟢 {username} connected "
        f"(user_id={user_id}, room={room_id})"
    )


    # ==========================================
    # Get Unread Messages
    # ==========================================

    unread_messages = (
        await MessageRepository.get_unread_messages(
            room_id,
            user_id,
        )
    )


    print(
        "🔍 UNREAD DEBUG:",
        [
            {
                "id": str(
                    message["_id"]
                ),

                "sender_id":
                    message[
                        "sender_id"
                    ],

                "status":
                    message.get(
                        "status"
                    ),

                "message":
                    message[
                        "message"
                    ],
            }

            for message in unread_messages
        ],
    )


    # ==========================================
    # Send Unread Messages
    # ==========================================

    if unread_messages:

        await manager.send_personal_message(
            {
                "type":
                    "unread_messages",

                "count":
                    len(
                        unread_messages
                    ),

                "message_ids": [

                    str(
                        message["_id"]
                    )

                    for message in unread_messages

                ],
            },
            websocket,
        )


    # ==========================================
    # Send Message History
    # ==========================================

    messages = (
        await MessageRepository.get_room_messages(
            room_id
        )
    )


    for message in messages:

        await manager.send_personal_message(
            {
                "type":
                    "message_history",

                "id":
                    str(
                        message["_id"]
                    ),

                "sender_id":
                    message[
                        "sender_id"
                    ],

                "username":
                    message[
                        "username"
                    ],

                "room_id":
                    message[
                        "room_id"
                    ],

                "message":
                    message[
                        "message"
                    ],

                "status":
                    message.get(
                        "status",
                        "sent",
                    ),

                "created_at":
                    message[
                        "created_at"
                    ].isoformat(),
            },

            websocket,
        )


    # ==========================================
    # WebSocket Events
    # ==========================================

    try:

        while True:

            data = (
                await websocket.receive_json()
            )

            event_type = data.get(
                "type"
            )


            # ======================================
            # Typing
            # ======================================

            if event_type == "typing":

                await manager.broadcast_except_sender(
                    room_id,

                    {
                        "type":
                            "user_typing",

                        "user_id":
                            user_id,

                        "username":
                            username,
                    },

                    websocket,
                )

                continue


            # ======================================
            # Stop Typing
            # ======================================

            if event_type == "stop_typing":

                await manager.broadcast_except_sender(
                    room_id,

                    {
                        "type":
                            "user_stop_typing",

                        "user_id":
                            user_id,

                        "username":
                            username,
                    },

                    websocket,
                )

                continue


            # ======================================
            # Message Delivered
            # ======================================

            if event_type == "message_delivered":

                message_id = data.get(
                    "message_id"
                )


                if not message_id:

                    continue


                updated = (
                    await MessageRepository.mark_as_delivered(
                        message_id
                    )
                )


                if updated:

                    await manager.broadcast(
                        room_id,

                        {
                            "type":
                                "message_delivered",

                            "message_id":
                                message_id,
                        },
                    )


                continue


            # ======================================
            # Message Read
            # ======================================

            if event_type == "message_read":

                message_id = data.get(
                    "message_id"
                )


                if not message_id:

                    continue


                updated = (
                    await MessageRepository.mark_as_read(
                        message_id=message_id,

                        room_id=room_id,

                        user_id=user_id,
                    )
                )


                if updated:

                    print(
                        f"📖 Message marked as read: "
                        f"{message_id} "
                        f"by {username}"
                    )


                    await manager.broadcast(
                        room_id,

                        {
                            "type":
                                "message_read",

                            "message_id":
                                message_id,
                        },
                    )


                continue


            # ======================================
            # Normal Message
            # ======================================

            if event_type != "message":

                continue


            message_text = data.get(
                "message"
            )


            if (
                not message_text
                or not message_text.strip()
            ):

                continue


            # ======================================
            # Create Message Document
            # ======================================

            message_document = (
                MessageModel.create(
                    sender_id=user_id,

                    username=username,

                    room_id=room_id,

                    message=message_text.strip(),
                )
            )


            # ======================================
            # Save To MongoDB
            # ======================================

            saved_message = (
                await MessageRepository.create_message(
                    message_document
                )
            )


            message_id = str(
                saved_message["_id"]
            )


            # ======================================
            # Broadcast Message
            # ======================================

            await manager.broadcast(
                room_id,

                {
                    "type":
                        "message",

                    "id":
                        message_id,

                    "sender_id":
                        saved_message[
                            "sender_id"
                        ],

                    "username":
                        saved_message[
                            "username"
                        ],

                    "room_id":
                        saved_message[
                            "room_id"
                        ],

                    "message":
                        saved_message[
                            "message"
                        ],

                    "status":
                        saved_message.get(
                            "status",
                            "sent",
                        ),

                    "created_at":
                        saved_message[
                            "created_at"
                        ].isoformat(),
                },
            )


            # ======================================
            # New Message Notification
            # ======================================

            await manager.broadcast_except_sender(
                room_id,

                {
                    "type":
                        "new_message_notification",

                    "message_id":
                        message_id,

                    "sender_id":
                        user_id,

                    "sender_username":
                        username,

                    "message":
                        saved_message[
                            "message"
                        ],

                    "room_id":
                        room_id,
                },

                websocket,
            )


            print(
                f"🔔 Notification sent for "
                f"message {message_id} "
                f"from {username}"
            )


    # ==========================================
    # User Disconnected
    # ==========================================

    except WebSocketDisconnect:

        manager.disconnect(
            websocket,
            room_id,
        )


        # ======================================
        # Check If User Has Another Connection
        # ======================================

        remaining_user_connections = (
            manager.get_room_users(
                room_id
            )
        )


        user_still_online = any(
            user["user_id"] == user_id
            for user in remaining_user_connections
        )


        # ======================================
        # Only Mark Offline If No Other Tab
        # Is Connected
        # ======================================

        if not user_still_online:

            await UserRepository.update_online_status(
                user_id,
                False,
            )


            await manager.broadcast(
                room_id,

                {
                    "type":
                        "user_offline",

                    "user_id":
                        user_id,

                    "username":
                        username,
                },
            )


        print(
            f"🔴 {username} disconnected "
            f"from room {room_id}"
        )