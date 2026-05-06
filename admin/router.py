from aiogram import Router
from apps.getenv import ENV

admin_router = Router()


async def is_admin(password: str) -> bool:
    return password == ENV.admin.ADMIN_PASS

from admin.handlers.login import login_router
from admin.handlers.add import add_router
from admin.handlers.edit import edit_router
from admin.handlers.delete import delete_router
from admin.handlers.broadcast import broadcast_router
from admin.handlers.cancel import cancel_router

admin_router.include_router(cancel_router)
admin_router.include_router(login_router)
admin_router.include_router(broadcast_router)
admin_router.include_router(add_router)
admin_router.include_router(edit_router)
admin_router.include_router(delete_router)