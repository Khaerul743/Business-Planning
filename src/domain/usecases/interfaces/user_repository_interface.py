from abc import ABC, abstractmethod

from src.domain.models import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_by_context_user(self) -> User | None:
        pass

    @abstractmethod
    async def create_user(
        self,
        name: str,
        email: str,
        hashed_password: str,
    ) -> User | None:
        pass
