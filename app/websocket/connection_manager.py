from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        # room_id -> list of WebSockets
        self.active_connections = {}


    # ==========================================
    # Connect
    # ==========================================

    async def connect(
        self,
        websocket: WebSocket,
        room_id: str,
    ):

        await websocket.accept()

        if room_id not in self.active_connections:

            self.active_connections[room_id] = []

        self.active_connections[room_id].append(
            websocket
        )


    # ==========================================
    # Disconnect
    # ==========================================

    def disconnect(
        self,
        websocket: WebSocket,
        room_id: str,
    ):

        if room_id not in self.active_connections:

            return


        if websocket in self.active_connections[room_id]:

            self.active_connections[room_id].remove(
                websocket
            )


        if len(
            self.active_connections[room_id]
        ) == 0:

            del self.active_connections[
                room_id
            ]


    # ==========================================
    # Get Existing Users
    # ==========================================

    def get_room_users(
        self,
        room_id: str,
        exclude_websocket: WebSocket = None, # type: ignore
    ):

        users = []


        if room_id not in self.active_connections:

            return users


        seen_user_ids = set()


        for connection in self.active_connections[
            room_id
        ]:

            if (
                exclude_websocket is not None
                and connection == exclude_websocket
            ):

                continue


            user_id = getattr(
                connection,
                "user_id",
                None,
            )

            username = getattr(
                connection,
                "username",
                None,
            )


            if not user_id or not username:

                continue


            # Prevent duplicate users
            # if the same user has multiple tabs.
            if user_id in seen_user_ids:

                continue


            seen_user_ids.add(
                user_id
            )


            users.append(
                {
                    "user_id": user_id,
                    "username": username,
                }
            )


        return users


    # ==========================================
    # Send Personal Message
    # ==========================================

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):

        await websocket.send_json(
            message
        )


    # ==========================================
    # Broadcast
    # ==========================================

    async def broadcast(
        self,
        room_id: str,
        message: dict,
    ):

        if room_id not in self.active_connections:

            return


        for connection in self.active_connections[
            room_id
        ]:

            await connection.send_json(
                message
            )


    # ==========================================
    # Broadcast Except Sender
    # ==========================================

    async def broadcast_except_sender(
        self,
        room_id: str,
        message: dict,
        sender: WebSocket,
    ):

        if room_id not in self.active_connections:

            return


        for connection in self.active_connections[
            room_id
        ]:

            if connection == sender:

                continue


            await connection.send_json(
                message
            )