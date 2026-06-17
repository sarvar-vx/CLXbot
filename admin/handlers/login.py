import bcrypt
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin.states import Login
from apps.buttons.reply import admin_menu, main_menu
from apps.getenv import ENV
login_router = Router()


# /login command
# ----------------------------------------------------------------------------------------------------------------------
@login_router.message(Command("login"))
async def login_handler(message: Message, state: FSMContext) -> None:
    await message.answer("🔐 Parolni kiriting:")
    await state.set_state(Login.password)


# Check password
# ----------------------------------------------------------------------------------------------------------------------
@login_router.message(Login.password, F.text)
async def check_password_handler(message: Message, state: FSMContext) -> None:
    await message.delete()
    if bcrypt.checkpw(message.text.encode(), ENV.admin.ADMIN_PASS_HASH.encode()):
        await state.set_state(None)
        await message.answer("✅ Xush kelibsiz, Admin!", reply_markup=admin_menu())
    else:
        await state.set_state(None)
        await message.answer("❌ Parol noto'g'ri!")


# Exit admin panel
# ----------------------------------------------------------------------------------------------------------------------
@login_router.message(F.text == "⬅️ Chiqish")
async def logout_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("👋 Chiqildi!", reply_markup=main_menu())