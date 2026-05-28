from .handler.base import BaseJobHandler
from .job_models import BaseJob


class JobDispatcher:
    def __init__(self):
        self._handlers: dict[str, BaseJobHandler] = {}

    def register(self, job_type: str, handler: BaseJobHandler):
        self._handlers[job_type] = handler

    async def dispatch(self, job: BaseJob):
        handler = self._handlers.get(job.type)

        if not handler:
            raise ValueError(f"No handler registered for job type: {job.type}")

        return await handler.handle(job)
