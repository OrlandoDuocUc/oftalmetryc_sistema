
from app.domain.models.user import User
from app.domain.use_cases.services.user_service import UserService

class UserRepository:
    def __init__(self):
        self._users = {
            1: User(1, "Juan", "juan@example.com"),
            2: User(2, "Ana", "ana@example.com")
        }

    def get_by_id(self, user_id):
        return self._users.get(user_id)
