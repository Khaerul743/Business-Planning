from abc import ABC, abstractmethod
from src.infrastructure.queue.job_models import BaseJob


class BaseJobHandler(ABC):
    @abstractmethod
    async def handle(self, job: BaseJob) -> None:
        pass
