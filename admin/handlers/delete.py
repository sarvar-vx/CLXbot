from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from admin.states import DeleteProduct, DeleteChannel
from apps.buttons.reply import delete_menu, admin_menu
from database.requests import get_product_by_name, get_product_by_id, delete_product, get_all_channels, delete_channel


delete_router = Router()


# Delete menu
# ----------------------------------------------------------------------------------------------------------------------
@delete_router.message(F.text == "🗑 O'chirish")
async def delete_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Nima o'chiramiz?", reply_markup=delete_menu())
    await state.set_state(DeleteProduct.search)


# Change category
# ----------------------------------------------------------------------------------------------------------------------
@delete_router.message(DeleteProduct.search, F.text.in_(["💻 Dastur", "🎮 O'yin", "🧲 Torrent"]))
async def delete_type_handler(message: Message, state: FSMContext) -> None:
    type_map = {
        "💻 Dastur": "software",
        "🎮 O'yin": "game",
        "🧲 Torrent": "torrent"
    }
    await state.update_data(type=type_map[message.text])
    await message.answer("Mahsulot nomini yoki ID sini kiriting:")
    await state.set_state(DeleteProduct.confirm)


# Product delete
# ----------------------------------------------------------------------------------------------------------------------
@delete_router.message(DeleteProduct.confirm, F.text)
async def delete_confirm_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if message.text.isdigit():
        product = await get_product_by_id(session, int(message.text))
    else:
        product = await get_product_by_name(session, message.text)

    if not product:
        await message.answer("❌ Mahsulot topilmadi!")
        return

    await delete_product(session, product.id)
    await state.clear()
    await message.answer(
        f"✅ <b>{product.name}</b> muvaffaqiyatli o'chirildi!",
        reply_markup=admin_menu()
    )


# Delete channel
# ----------------------------------------------------------------------------------------------------------------------
@delete_router.message(DeleteProduct.search, F.text == "📢 Kanal")
async def delete_channel_type_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    channels = await get_all_channels(session)
    if not channels:
        await message.answer("❌ Kanallar mavjud emas!")
        return
    channels_list = "\n".join([f"{ch.id}. {ch.name} — {ch.username}" for ch in channels])
    await message.answer(f"Mavjud kanallar:\n{channels_list}\n\nKanal ID sini kiriting:")
    await state.set_state(DeleteChannel.search)


@delete_router.message(DeleteChannel.search, F.text)
async def delete_channel_confirm_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not message.text.isdigit():
        await message.answer("❌ Faqat ID kiriting!")
        return

    await delete_channel(session, int(message.text))
    await state.clear()
    await message.answer("✅ Kanal muvaffaqiyatli o'chirildi!", reply_markup=admin_menu())


# Back
# ----------------------------------------------------------------------------------------------------------------------
@delete_router.message(DeleteProduct.search, F.text == "⬅️ Orqaga")
async def delete_back_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Admin menyu:", reply_markup=admin_menu())