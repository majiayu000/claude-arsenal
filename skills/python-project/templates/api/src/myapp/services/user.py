"""User service - business logic layer."""

from uuid import UUID, uuid4

from myapp.core.exceptions import ConflictError, NotFoundError
from myapp.models.user import User, UserCreate, UserUpdate


class UserService:
    """User business logic.

    In a real application, this would use a repository for data access.
    This example uses in-memory storage for simplicity.
    """

    def __init__(self) -> None:
        # In-memory storage (replace with repository in real app)
        self._users: dict[UUID, dict] = {}

    async def get(self, id: UUID) -> User:
        if id not in self._users:
            raise NotFoundError("user", str(id))
        return User(**self._users[id])

    async def create(self, data: UserCreate) -> User:
        # Check email uniqueness
        for user_data in self._users.values():
            if user_data["email"] == data.email:
                raise ConflictError("email already exists")

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        user_id = uuid4()

        user_dict = {
            "id": user_id,
            "email": data.email,
            "name": data.name,
            "created_at": now,
            "updated_at": now,
        }
        self._users[user_id] = user_dict
        return User(**user_dict)

    async def update(self, id: UUID, data: UserUpdate) -> User:
        if id not in self._users:
            raise NotFoundError("user", str(id))

        # Check email uniqueness if updating
        if data.email:
            for uid, user_data in self._users.items():
                if uid != id and user_data["email"] == data.email:
                    raise ConflictError("email already exists")

        from datetime import datetime, timezone

        user_dict = self._users[id]
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            user_dict[field] = value

        user_dict["updated_at"] = datetime.now(timezone.utc)
        return User(**user_dict)

    async def delete(self, id: UUID) -> None:
        if id not in self._users:
            raise NotFoundError("user", str(id))
        del self._users[id]
