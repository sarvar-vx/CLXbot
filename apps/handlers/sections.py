from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from apps.buttons.inline import force_channels
from apps.buttons.reply import main_menu, programs_menu, games_menu, torrent_menu
from apps.handlers.forcefollow import check_subscription
from apps.getenv import ENV
from database.requests import add_user, get_products_by_type
from services.forwarder import forward_product
from apps.states import FeedbackState


section_router = Router()


# Start handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    await add_user(session, message.from_user.id, message.from_user.username, message.from_user.full_name)
    unsubscribed = await check_subscription(bot, message.from_user.id, session)

    if not unsubscribed:
        await message.answer(
            text=f"Xush kelibsiz, {message.from_user.first_name}!\nBotdan bemalol foydalanishingiz mumkin.",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            text="Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling!",
            reply_markup=force_channels(unsubscribed)
        )


# Check subscription callback
# ----------------------------------------------------------------------------------------------------------------------
@section_router.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: CallbackQuery, bot: Bot, session: AsyncSession) -> None:
    unsubscribed = await check_subscription(bot, callback.from_user.id, session)

    if not unsubscribed:
        await callback.message.delete()
        await callback.message.answer(
            text=f"Tabriklaymiz, {callback.from_user.first_name}!\nEndi botdan bemalol foydalanishingiz mumkin. ✅",
            reply_markup=main_menu()
        )
    else:
        await callback.answer(
            text="Hali barcha kanallarga a'zo bo'lmadingiz! ❌",
            show_alert=True
        )


# Programs handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "💻 Dasturlar")
async def programs_handler(message: Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    products = await get_products_by_type(session, "software")
    await message.answer("Dasturlar:", reply_markup=await programs_menu(products))


# Games handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "🎮 O'yinlar")
async def games_handler(message: Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    products = await get_products_by_type(session, "game")
    await message.answer("O'yinlar:", reply_markup=await games_menu(products))


# Torrent handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "🧲 Torrent")
async def torrent_handler(message: Message, session: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    products = await get_products_by_type(session, "torrent")
    await message.answer("Torrentlar:", reply_markup=await torrent_menu(products))


# Download Guide handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "📑 Qo'llanma")
async def guide_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    message_ids = [1214, 1215, 1216, 1217, 1218, 1219, 1147]
    user_id = message.from_user.id

    for message_id in message_ids:
        await bot.forward_message(
            chat_id=user_id,
            from_chat_id=ENV.bot.CHANNEL_ID,
            message_id=message_id
        )


# About handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "ℹ️ Bot haqida")
async def about_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "🤖 <b>CLX Bot</b>\n\n"
        "📦 Bu bot orqali siz eng yangi:\n"
        "💻 Dasturlar\n"
        "🎮 O'yinlar\n"
        "🧲 Torrent fayllarini yuklab olishingiz mumkin!\n\n"
        "⚡️ Tez, qulay va bepul!\n\n"
        "👨‍💻 <b>Dasturchi:</b> @sarvar_vx\n"
        "📢 <b>Kanal:</b> @CLXlive\n"
        "📅 <b>Versiya:</b> 1.2.1\n\n"
        "<i>Powered by CLX Studio ⚡️</i>",
        parse_mode="HTML"
    )


# Contact admin handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "👨‍💻 Admin bilan bog'lanish")
async def contact_admin_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "👨‍💻 <b>Admin bilan bog'lanish</b>\n\n"
        "Har qanday savol, taklif yoki muammolar uchun "
        "quyidagi admin bilan bog'laning:\n\n"
        "👤 <b>Admin:</b> @sarvar_vx\n\n"
        "📝 Xabaringizni qoldiring, tez orada javob beramiz!"
    )


# Back handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message((F.text == "🔙 Orqaga") | (F.text == "/menu"))
async def back_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=main_menu())


# Feedback handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text == "💬 Fikrizni qoldiring!")
async def feedback_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("💬 Bot yoki boshqa mavzuda o'z fikrizni qoldiring...", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FeedbackState.feedback_message)

@section_router.message(FeedbackState.feedback_message, F.text)
async def get_feedback_handler(message: Message, state: FSMContext):
    await message.forward(chat_id=ENV.bot.FEEDBACK_CHANNEL)
    await message.answer("Raxmat, fikriz biz uchun muhim 🙌", reply_markup=main_menu())
    await state.clear()


# Product handler
# ----------------------------------------------------------------------------------------------------------------------
@section_router.message(F.text)
async def product_handler(message: Message, bot: Bot, session: AsyncSession) -> None:
    skip_texts = [
        "💻 Dasturlar", "🎮 O'yinlar", "🧲 Torrent",
        "ℹ️ Bot haqida", "👨‍💻 Admin bilan bog'lanish", "🔙 Orqaga",
        "💬 Fikrizni qoldiring!", "📑 Qo'llanma"
    ]
    if message.text in skip_texts:
        return

    success = await forward_product(bot, message.from_user.id, message.from_user.username, message.text, ENV.bot.CHANNEL_ID, session)
    if not success:
        await message.answer("❌ Bunaqa dastur topilmadi!")