from aiogram import Bot
from database.requests import get_product_by_name
from services.logger import log_request, log_error


async def forward_product(bot: Bot, user_id: int, username: str, product_name: str, channel_id: str, session) -> bool:
    product = await get_product_by_name(session, product_name)

    if not product:
        return False

    try:
        for message_id in product.message_ids:
            await bot.forward_message(
                chat_id=user_id,
                from_chat_id=channel_id,
                message_id=message_id
            )
        await log_request(bot, user_id, username, product.type, product_name)
        return True
    except Exception as e:
        await log_error(bot, user_id, username, product_name, str(e))
        return False