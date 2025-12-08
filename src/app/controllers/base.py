from src.core.utils import get_logger


class BaseController:
    def __init__(self, name):
        self._logger = get_logger(name)
