from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from admin.states import EditProduct
from apps.buttons.reply import edit_menu, admin_menu
from database.requests import get_product_by_name, get_product_by_id, update_product


edit_router = Router()


# Edit menu
# ----------------------------------------------------------------------------------------------------------------------
@edit_router.message(F.text == "✏️ Tahrirlash")
async def edit_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Qaysi kategoriyadan?", reply_markup=edit_menu())
    await state.set_state(EditProduct.search)


# Change category
# ----------------------------------------------------------------------------------------------------------------------
@edit_router.message(EditProduct.search, F.text.in_(["💻 Dastur", "🎮 O'yin", "🧲 Torrent"]))
async def edit_type_handler(message: Message, state: FSMContext) -> None:
    type_map = {
        "💻 Dastur": "software",
        "🎮 O'yin": "game",
        "🧲 Torrent": "torrent"
    }
    await state.update_data(type=type_map[message.text])
    await message.answer("Mahsulot nomini yoki ID sini kiriting:")
    await state.set_state(EditProduct.field)


# Search product
# ----------------------------------------------------------------------------------------------------------------------
@edit_router.message(EditProduct.field, F.text)
async def edit_search_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if message.text.isdigit():
        product = await get_product_by_id(session, int(message.text))
    else:
        product = await get_product_by_name(session, message.text)

    if not product:
        await message.answer("❌ Mahsulot topilmadi!")
        return

    await state.update_data(product_id=product.id)
    await message.answer(
        f"📦 <b>{product.name}</b>\n"
        f"🗂 Turi: {product.type}\n"
        f"🔢 Message IDs: {product.message_ids}\n\n"
        "Nini tahrirlaysiz?\n"
        "/name <b>Yangi nom</b>\n"
        "/ids <b>1234 1235 1236</b>"
    )
    await state.set_state(EditProduct.value)


# Edit name
# ----------------------------------------------------------------------------------------------------------------------
@edit_router.message(EditProduct.value, F.text.startswith("/name"))
async def edit_name_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    new_name = message.text.replace("/name", "").strip()
    if not new_name:
        await message.answer("Yangi nomni kiriting: /name <b>Yangi nom</b>")
        return

    data = await state.get_data()
    await update_product(session, data["product_id"], name=new_name)
    await state.clear()
    await message.answer(f"✅ Nom <b>{new_name}</b> ga o'zgartirildi!", reply_markup=admin_menu())


# Edit Message IDs
# ----------------------------------------------------------------------------------------------------------------------
@edit_router.message(EditProduct.value, F.text.startswith("/ids"))
async def edit_ids_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    new_ids_str = message.text.replace("/ids", "").strip()
    if not new_ids_str:
        await message.answer("Yangi IDlarni kiriting: /ids <b>1234 1235 1236</b>")
        return

    try:
        new_ids = list(map(int, new_ids_str.split()))
    except ValueError:
        await message.answer("❌ Noto'g'ri format! Faqat raqamlar kiriting.")
        return

    data = await state.get_data()
    await update_product(session, data["product_id"], message_ids=new_ids)
    await state.clear()
    await message.answer("✅ Message IDlar yangilandi!", reply_markup=admin_menu())


# Back
# ----------------------------------------------------------------------------------------------------------------------
@edit_router.message(EditProduct.search, F.text == "⬅️ Orqaga")
async def edit_back_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Admin menyu:", reply_markup=admin_menu())