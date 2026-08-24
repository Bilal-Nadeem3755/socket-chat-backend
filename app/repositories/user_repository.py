from bson import ObjectId
from datetime import datetime

from app.database.database import database
from app.models.user_model import UserModel


users_collection = database["users"]


class UserRepository:

    @staticmethod
    async def create_user(
        full_name: str,
        username: str,
        email: str,
        hashed_password: str,
    ):

        user = UserModel.create(
            full_name,
            username,
            email,
            hashed_password,
        )

        result = await users_collection.insert_one(user)

        user["_id"] = result.inserted_id

        return user

    @staticmethod
    async def get_user_by_email(email: str):

        return await users_collection.find_one(
            {
                "email": email.lower()
            }
        )

    @staticmethod
    async def get_user_by_username(username: str):

        return await users_collection.find_one(
            {
                "username": username.lower()
            }
        )

    @staticmethod
    async def get_user_by_id(user_id: str):

        return await users_collection.find_one(
            {
                "_id": ObjectId(user_id)
            }
        )

    @staticmethod
    async def update_online_status(
        user_id: str,
        status: bool,
    ):

        await users_collection.update_one(
            {
                "_id": ObjectId(user_id)
            },
            {
                "$set": {
                    "is_online": status,
                    "last_seen": datetime.utcnow(),
                }
            },
        )