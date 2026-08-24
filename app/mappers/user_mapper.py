from app.schemas.user_schema import UserResponse


class UserMapper:

    @staticmethod
    def to_response(user):

        return UserResponse(

            id=str(user["_id"]),

            full_name=user["full_name"],

            username=user["username"],

            email=user["email"],

            is_online=user["is_online"],

            profile_picture=user.get("profile_picture"),
        )