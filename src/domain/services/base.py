from src.core.utils import get_logger
from src.domain.usecases.base import UseCaseResult


class BaseService:
    def __init__(self, name):
        self.logger = get_logger(name)

    def raise_error_usecase(self, use_case: UseCaseResult):
        exception = use_case.get_exception()
        if exception:
            raise exception
