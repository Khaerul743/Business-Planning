from fastapi import Depends
from supabase import AsyncClient

from src.config.supabase import get_supabase


def controller_factory(ControllerClass):
    """
    Membuat dependency generator untuk controller apapun.
    Contoh:
        get_auth_controller = controller_factory(AuthController)
    """

    async def _get_controller(db: AsyncClient = Depends(get_supabase)):
        return ControllerClass(db)

    return _get_controller
