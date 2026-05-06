from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from admin.states import Broadcast
from apps.buttons.reply import admin_menu
from database.requests import get_all_users

broadcast_router = Router()


# Statistics
# ----------------------------------------------------------------------------------------------------------------------
@broadcast_router.message(F.text == "📊 Statistika")
async def stats_handler(message: Message, session: AsyncSession) -> None:
    users = await get_all_users(session)
    await message.answer(
        f"📊 <b>Statistika</b>\n\n"
        f"👥 Foydalanuvchilar soni: <b>{len(users)}</b>"
    )


# Send Ad
# ----------------------------------------------------------------------------------------------------------------------
@broadcast_router.message(F.text == "📢 E'lon yuborish")
async def broadcast_handler(message: Message, state: FSMContext) -> None:
    await message.answer("📢 E'lon xabarini yuboring (matn, rasm, video — istalgan):")
    await state.set_state(Broadcast.message)


@broadcast_router.message(Broadcast.message)
async def broadcast_message_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    users = await get_all_users(session)
    success, failed = 0, 0

    for user in users:
        try:
            await message.copy_to(user.id)
            success += 1
        except Exception:
            failed += 1

    await state.clear()
    await message.answer(
        f"✅ E'lon yuborildi!\n\n"
        f"✔️ Muvaffaqiyatli: <b>{success}</b>\n"
        f"❌ Yuborilmadi: <b>{failed}</b>",
        reply_markup=admin_menu()
    )