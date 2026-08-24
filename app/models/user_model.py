from datetime import datetime

class UserModel:

    @staticmethod
    def create(
        full_name: str,
        username: str,
        email: str,
        hashed_password: str,
    ):

        return {
            "full_name": full_name,
            "username": username.lower(),
            "email": email.lower(),
            "hashed_password": hashed_password,

            "profile_picture": None,
            "bio": "",

            "is_online": False,
            "last_seen": None,

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }