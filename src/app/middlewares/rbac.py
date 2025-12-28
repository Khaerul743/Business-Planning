from src.core.context.request_context import current_user_role
from src.core.exceptions.auth_exception import ForbiddenException


def require_roles(*allowed_roles: str):
    def dependency():
        role = current_user_role.get()
        if role is None:
            raise ForbiddenException("Role not found")

        if str(role) not in allowed_roles:
            raise ForbiddenException("You do not have permission")

    return dependency
