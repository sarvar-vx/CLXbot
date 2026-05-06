from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import get_all_channels


async def get_unsubscribed(bot: Bot, user_id: int, channels: list) -> list:
    unsubscribed = []
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel.username, user_id=user_id)
            if member.status in ("left", "kicked"):
                unsubscribed.append(channel.username)
        except Exception:
            unsubscribed.append(channel.username)
    return unsubscribed


async def check_subscription(bot: Bot, user_id: int, session: AsyncSession) -> list:
    channels = await get_all_channels(session)
    return await get_unsubscribed(bot, user_id, channels)