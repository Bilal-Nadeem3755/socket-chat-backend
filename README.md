# Socket Chat App — Backend

A real-time chat backend built with **FastAPI**, **MongoDB**, and **WebSockets**. It provides user registration and login, JWT authentication, room-based live messaging, message history, online presence, typing events, and message delivery/read status.

## Features

- User registration with full name, username, email, and password
- Login using email and password
- JWT access tokens for authenticated users
- Password hashing
- Current-user endpoint
- MongoDB persistence using Motor's asynchronous MongoDB client
- Room-based WebSocket connections
- Real-time message broadcasting
- Online-user presence updates and last-seen timestamps
- Typing indicators
- Message history for chat rooms
- Message statuses: sent, delivered, and read
- Unread-message counts and message ID notifications on connection
- Custom application exception handling
- FastAPI interactive API documentation

## Tech Stack

- Python
- FastAPI
- MongoDB
- Motor (asynchronous MongoDB driver)
- Pydantic and Pydantic Settings
- PyJWT for JWT tokens
- `pwdlib` for password hashing
- Uvicorn
- WebSockets

## Project Structure

```text
backend/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   └── database.py
│   ├── dependencies/
│   │   └── auth_dependency.py
│   ├── exceptions/
│   │   ├── custom_exceptions.py
│   │   └── exception_handler.py
│   ├── mappers/
│   │   ├── message_mapper.py
│   │   └── user_mapper.py
│   ├── models/
│   │   ├── message_model.py
│   │   ├── notification_model.py
│   │   └── user_model.py
│   ├── repositories/
│   │   ├── message_repository.py
│   │   ├── notification_repository.py
│   │   └── user_repository.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── message_schema.py
│   │   └── user_schema.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── chat_service.py
│   ├── websocket/
│   │   ├── connection_manager.py
│   │   └── websocket_router.py
│   └── main.py
├── requirements.txt
└── run.py
```

## Configuration

The application loads settings from a `.env` file using Pydantic Settings. Create the file in the backend working directory (the directory from which you start the app) and provide your own values:

```env
APP_NAME=Socket Chat Backend
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-host>/
DATABASE_NAME=socket_chat
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

These are example values and placeholders. Replace them with your own MongoDB connection string, database name, and a strong random secret. Never commit `.env` or publish credentials. The exact database name and token expiry should match your own deployment configuration.

## Run Locally

### Requirements

- Python 3.10 or a compatible newer Python version
- A MongoDB database (local MongoDB or MongoDB Atlas)
- The frontend running separately for the full chat experience

### 1. Clone the backend repository

```bash
git clone <YOUR_BACKEND_REPOSITORY_URL>
cd backend
```

Replace `<YOUR_BACKEND_REPOSITORY_URL>` with your backend repository URL. Run the following commands from the directory containing `requirements.txt` and `run.py`.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If pip reports an encoding error for `requirements.txt`, open that file in an editor and save it as UTF-8, then retry the command.

### 4. Create the `.env` file

Add the configuration variables shown above. Ensure `MONGODB_URL` points to a reachable MongoDB instance and the credentials are valid.

### 5. Start the server

Using the project's run script:

```bash
python run.py
```

Or start Uvicorn directly:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The local API is available at `http://127.0.0.1:8000`.

## API Documentation

When the backend is running, open:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **Health check:** `http://127.0.0.1:8000/`

## Main API Routes

| Method | Route | Purpose |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Log in and receive an access token |
| `GET` | `/auth/me` | Return the authenticated user's profile |
| `GET` | `/messages/{room_id}` | Retrieve recent messages for a room |
| `WS` | `/ws/{room_id}?token=<JWT>` | Connect to a room using a JWT token |

The WebSocket endpoint validates the token supplied in the `token` query parameter. The client and server must use the same event names and payload formats; refer to the frontend and `app/websocket/websocket_router.py` for the current message protocol.

## MongoDB Collections

The code uses these collections in the configured database:

- `users` — user account details, hashed passwords, online status, and last-seen timestamps
- `messages` — room messages, sender information, timestamps, and message status
- `notifications` — notification records and unread/read status

## Frontend Integration and Deployment

The backend currently allows the local frontend origin `http://localhost:5173` through its CORS configuration. When deploying, add the actual frontend origin to `allow_origins` in `app/main.py`.

For a deployed HTTPS frontend, use a secure WebSocket URL (`wss://`) and configure the frontend to point to the deployed backend. Make sure the hosting platform supports persistent WebSocket connections and that MongoDB is reachable from the deployed service.

## Security Notes

- Never commit `.env`, MongoDB credentials, or JWT secrets.
- Use a long, random `SECRET_KEY` in production.
- Use HTTPS/WSS in production.
- Do not use real users' private information in public demos.
- The WebSocket URL carries the JWT as a query parameter; avoid logging full connection URLs or tokens.
