from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from admin.states import AddProduct, AddChannel
from apps.buttons.reply import add_menu, admin_menu
from database.requests import add_product, add_channel

add_router = Router()


# Add menu
# ----------------------------------------------------------------------------------------------------------------------
@add_router.message(F.text == "➕ Qo'shish")
async def add_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Nima qo'shamiz?", reply_markup=add_menu())
    await state.set_state(AddProduct.type)


# Change category
# ----------------------------------------------------------------------------------------------------------------------
@add_router.message(AddProduct.type, F.text.in_(["💻 Dastur", "🎮 O'yin", "🧲 Torrent"]))
async def add_type_handler(message: Message, state: FSMContext) -> None:
    type_map = {
        "💻 Dastur": "software",
        "🎮 O'yin": "game",
        "🧲 Torrent": "torrent"
    }
    await state.update_data(type=type_map[message.text])
    await message.answer("Nomini kiriting:")
    await state.set_state(AddProduct.name)


# Enter name
# ----------------------------------------------------------------------------------------------------------------------
@add_router.message(AddProduct.name, F.text)
async def add_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        "Message ID(lar)ini kiriting:\n"
        "Bitta bo'lsa: <code>1234</code>\n"
        "Ko'p bo'lsa: <code>1234 1235 1236</code>"
    )
    await state.set_state(AddProduct.message_ids)


# Enter Message ID
# ----------------------------------------------------------------------------------------------------------------------
@add_router.message(AddProduct.message_ids, F.text)
async def add_message_ids_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        message_ids = list(map(int, message.text.split()))
    except ValueError:
        await message.answer("❌ Noto'g'ri format! Faqat raqamlar kiriting.")
        return

    data = await state.get_data()
    await add_product(session, data["name"], data["type"], message_ids)
    await state.clear()
    await message.answer(
        f"✅ <b>{data['name']}</b> muvaffaqiyatli qo'shildi!",
        reply_markup=admin_menu()
    )


# Add channel
# ----------------------------------------------------------------------------------------------------------------------
@add_router.message(AddProduct.type, F.text == "📢 Kanal")
async def add_channel_type_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Kanal nomini kiriting:")
    await state.set_state(AddChannel.name)


@add_router.message(AddChannel.name, F.text)
async def add_channel_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Kanal username ini kiriting: (@username)")
    await state.set_state(AddChannel.username)


@add_router.message(AddChannel.username, F.text)
async def add_channel_username_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    await add_channel(session, data["name"], message.text)
    await state.clear()
    await message.answer("✅ Kanal muvaffaqiyatli qo'shildi!", reply_markup=admin_menu())


# Back
# ----------------------------------------------------------------------------------------------------------------------
@add_router.message(AddProduct.type, F.text == "⬅️ Orqaga")
async def add_back_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Admin menyu:", reply_markup=admin_menu())