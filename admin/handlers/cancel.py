from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from apps.buttons.reply import main_menu


cancel_router = Router()


@cancel_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Bekor qilish uchun hech narsa yo'q!")
        return
    await state.clear()
    await message.answer("🚫 Bekor qilindi!", reply_markup=main_menu())