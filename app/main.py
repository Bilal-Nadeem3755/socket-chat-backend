from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.message import router as message_router
from app.exceptions.custom_exceptions import AppException
from app.exceptions.exception_handler import app_exception_handler
from app.websocket.websocket_router import router as websocket_router


app = FastAPI(
    title="Socket Chat Backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://socket-chat-frontend-convospace.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(websocket_router)
app.include_router(message_router)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)


@app.get("/")
async def home():
    return {
        "message": "Backend Running"
    }